from typing import List, Optional

import networkx as nx

from preql.constants import logger
from preql.core.constants import CONSTANT_DATASET
from preql.core.enums import Purpose
from preql.core.graph_models import concept_to_node, datasource_to_node
from preql.core.models import (
    Datasource,
    QueryDatasource,
    SourceType,
    Environment,
    Concept,
    Grain,
    Function,
    UnnestJoin,
)
from preql.utility import unique
from preql.core.processing.nodes.base_node import StrategyNode
from preql.core.exceptions import NoDatasourceException


LOGGER_PREFIX = "[CONCEPT DETAIL - SELECT NODE]"


class StaticSelectNode(StrategyNode):
    """Static select nodes."""

    source_type = SourceType.SELECT

    def __init__(
        self,
        input_concepts: List[Concept],
        output_concepts: List[Concept],
        environment: Environment,
        g,
        datasource: QueryDatasource,
        depth: int = 0,
        partial_concepts: List[Concept] | None = None,
    ):
        super().__init__(
            input_concepts=input_concepts,
            output_concepts=output_concepts,
            environment=environment,
            g=g,
            whole_grain=True,
            parents=[],
            depth=depth,
            partial_concepts=partial_concepts,
        )
        self.datasource = datasource

    def _resolve(self):
        if self.datasource.grain == Grain():
            raise NotImplementedError
        return self.datasource


class SelectNode(StrategyNode):
    """Select nodes actually fetch raw data from a table
    Responsible for selecting the cheapest option from which to select.
    """

    source_type = SourceType.SELECT

    def __init__(
        self,
        input_concepts: List[Concept],
        output_concepts: List[Concept],
        environment: Environment,
        g,
        whole_grain: bool = False,
        parents: List["StrategyNode"] | None = None,
        depth: int = 0,
        partial_concepts: List[Concept] | None = None,
    ):
        super().__init__(
            input_concepts=input_concepts,
            output_concepts=output_concepts,
            environment=environment,
            g=g,
            whole_grain=whole_grain,
            parents=parents,
            depth=depth,
            partial_concepts=partial_concepts,
        )

    def resolve_from_raw_datasources(
        self, all_concepts: List[Concept]
    ) -> Optional[QueryDatasource]:
        for datasource in self.environment.datasources.values():
            all_found = True
            for raw_concept in all_concepts:
                # look for connection to abstract grain
                req_concept = raw_concept.with_default_grain()
                try:
                    path = nx.shortest_path(
                        self.g,
                        source=datasource_to_node(datasource),
                        target=concept_to_node(req_concept),
                    )
                except nx.NodeNotFound as e:
                    candidates = [
                        datasource_to_node(datasource),
                        concept_to_node(req_concept),
                    ]
                    for candidate in candidates:
                        try:
                            self.g.nodes[candidate]
                        except KeyError:
                            raise SyntaxError(
                                "Could not find node for {}".format(candidate)
                            )
                    raise e
                except nx.exception.NetworkXNoPath:
                    all_found = False
                    break
                # 2023-10-18 - more strict condition then below
                # if len(path) != 2:
                #     all_found = False
                #     break
                if (
                    len([p for p in path if self.g.nodes[p]["type"] == "datasource"])
                    != 1
                ):
                    all_found = False
                    break
            if all_found:
                partial_concepts = {
                    c.concept.address for c in datasource.columns if not c.is_complete
                }
                if partial_concepts and any(
                    [c.address in partial_concepts for c in all_concepts]
                ):
                    logger.info(
                        f"{self.logging_prefix}{LOGGER_PREFIX} skipping direct select from {datasource.address} for due to partial concepts {[c for c in partial_concepts]}"
                    )
                    continue
                # keep all concepts on the output, until we get to a node which requires reduction

                if any([c.grain != datasource.grain for c in all_concepts]):
                    logger.info(
                        f"{self.logging_prefix}{LOGGER_PREFIX} need to group to select grain"
                    )
                    target_grain = Grain(components=[c for c in all_concepts])
                else:
                    logger.info(
                        f"{self.logging_prefix}{LOGGER_PREFIX} all concepts at desired grain {datasource.grain}, including grain in output"
                    )
                    target_grain = datasource.grain
                    # ensure that if this select needs to merge, the grain components are present
                    all_concepts = all_concepts + datasource.grain.components_copy

                # append in any concepts that are being derived via function at call time

                all_concepts_final: List[Concept] = unique(all_concepts, "address")
                source_map: dict[
                    str, set[Datasource | QueryDatasource | UnnestJoin]
                ] = {concept.address: {datasource} for concept in all_concepts_final}

                derived_concepts = [
                    c
                    for c in datasource.columns
                    if isinstance(c.alias, Function) and c.concept.address in source_map
                ]
                for c in derived_concepts:
                    if not isinstance(c.alias, Function):
                        continue
                    for x in c.alias.concept_arguments:
                        source_map[x.address] = {datasource}
                node = QueryDatasource(
                    input_concepts=all_concepts_final,
                    output_concepts=all_concepts_final,
                    source_map=source_map,
                    datasources=[datasource],
                    grain=target_grain,
                    joins=[],
                    partial_concepts=[
                        c.concept for c in datasource.columns if not c.is_complete
                    ],
                    source_type=SourceType.DIRECT_SELECT,
                )
                logger.info(
                    f"{self.logging_prefix}{LOGGER_PREFIX} found direct select from {datasource.address} for {[str(c) for c in all_concepts]}. Group by required is {node.group_required}"
                    f" grain {target_grain} vs {datasource.grain}"
                )
                return node
        return None

    def resolve_from_constant_datasources(self) -> QueryDatasource:
        datasource = Datasource(
            identifier=CONSTANT_DATASET, address=CONSTANT_DATASET, columns=[]
        )
        return QueryDatasource(
            input_concepts=[],
            output_concepts=unique(self.all_concepts, "address"),
            source_map={concept.address: set() for concept in self.all_concepts},
            datasources=[datasource],
            grain=datasource.grain,
            joins=[],
            partial_concepts=[],
        )

    def _resolve(self) -> QueryDatasource:
        # if we have parent nodes, we do not need to go to a datasource
        if self.parents:
            return super()._resolve()
        resolution: QueryDatasource | None
        if all([c.purpose == Purpose.CONSTANT for c in self.all_concepts]):
            logger.info(
                f"{self.logging_prefix}{LOGGER_PREFIX} have a constant datasource"
            )
            resolution = self.resolve_from_constant_datasources()
            if resolution:
                return resolution
        logger.info(
            f"{self.logging_prefix}{LOGGER_PREFIX} resolving from raw datasources"
        )
        resolution = self.resolve_from_raw_datasources(self.all_concepts)
        if resolution:
            return resolution
        required = [c.address for c in self.all_concepts]
        raise NoDatasourceException(
            f"Could not find any way to associate required concepts {required}"
        )


class ConstantNode(SelectNode):
    """Represents a constant value."""

    pass
