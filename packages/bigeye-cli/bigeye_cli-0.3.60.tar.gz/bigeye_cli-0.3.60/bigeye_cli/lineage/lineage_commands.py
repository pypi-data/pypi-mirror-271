from typing import Optional

import typer


from bigeye_cli.exceptions.exceptions import InvalidEntityException
from bigeye_cli.functions import cli_client_factory
from bigeye_cli import global_options
from bigeye_sdk.controller.lineage_controller import LineageController
from bigeye_sdk.model.enums import MatchType
from bigeye_sdk.log import get_logger


log = get_logger(__file__)

app = typer.Typer(no_args_is_help=True, help='Lineage Commands for Bigeye CLI')

"""
File should contain commands relating to lineage calls to the API.
"""


@app.command()
def create_node(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        entity_name: str = typer.Option(
            ...
            , "--entity_name"
            , "-en"
            , help="The fully qualified table name or name of the tableau workbook"
        ),
        integration_name: Optional[str] = typer.Option(
            None
            , "--int_name"
            , "-in"
            , help="The name of the BI connection (required for entities outside of Bigeye)"
        )
):
    """Create a lineage node for an entity"""
    client = cli_client_factory(bigeye_conf, config_file, workspace)
    lineage_controller = LineageController(client)
    node = lineage_controller.create_node_by_name(entity_name=entity_name, integration_name=integration_name)
    log.info(f"Node created:\n\tID: {node.id}\n\tname: {node.node_name}")


@app.command()
def delete_node(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        entity_name: str = typer.Option(
            ...
            , "--entity_name"
            , "-en"
            , help="The fully qualified table name or name of the tableau workbook"
        ),
        integration_name: Optional[str] = typer.Option(
            None
            , "--int_name"
            , "-in"
            , help="The name of the BI connection (required for entities outside of Bigeye)"
        )
):
    """Delete a lineage node for an entity"""
    client = cli_client_factory(bigeye_conf, config_file, workspace)
    lineage_controller = LineageController(client)
    lineage_controller.delete_node_by_name(entity_name=entity_name, integration_name=integration_name)


@app.command()
def create_relation(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        upstream_table_name: str = typer.Option(
            ...
            , "--upstream"
            , "-up"
            , help="The fully qualified table name"
        ),
        downstream_table_name: str = typer.Option(
            ...
            , "--downstream"
            , "-down"
            , help="The fully qualified table name"
        )
):
    """Create a lineage relationship for 2 entities"""
    client = cli_client_factory(bigeye_conf, config_file, workspace)
    lineage_controller = LineageController(client)
    r = lineage_controller.create_relation_from_name(upstream_table_name=upstream_table_name,
                                                     downstream_table_name=downstream_table_name)
    log.info(f"Relationship created:\n\tID: {r.id}\n\tupstream ID: {r.upstream.id}\n\tdownstream ID:{r.downstream.id}")


@app.command()
def delete_relation(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        entity_name: Optional[str] = typer.Option(
            None
            , "--entity_name"
            , "-en"
            , help="The fully qualified table name or name of the tableau workbook"
        ),
        relationship_id: Optional[int] = typer.Option(
            0
            , "--relation_id"
            , "-rid"
            , help="The relationship ID to delete"
        ),
        integration_name: Optional[str] = typer.Option(
            None
            , "--int_name"
            , "-in"
            , help="The name of the BI connection (required for entities outside of Bigeye)"
        )
):
    """Deletes a single relationship based on relation ID or all relationships for a node by name."""
    client = cli_client_factory(bigeye_conf, config_file, workspace)
    lineage_controller = LineageController(client)

    if not entity_name and not relationship_id:
        raise InvalidEntityException("No entity specified to delete.")
    elif relationship_id:
        client.delete_lineage_relationship(relationship_id=relationship_id)
    else:
        lineage_controller.delete_relationships_by_name(entity_name=entity_name, integration_name=integration_name)


@app.command()
def infer_relations(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        upstream_selector: str = typer.Option(
            None
            , "--upstream_selector"
            , "-upstream"
            , help="The pattern of tables in the upstream source to select. Wildcard (*) indicates all tables or all "
                   "schemas, e.g. source_1.*.* would be all schemas in source_1."
        ),
        downstream_selector: str = typer.Option(
            None
            , "--downstream_selector"
            , "-downstream"
            , help="The pattern of tables in the downstream source to select. Wildcard (*) indicates all tables or all "
                   "schemas, e.g. source_2.*.* would be all schemas in source_2."
        ),
        match_type: Optional[MatchType] = typer.Option(
            MatchType.STRICT
            , "--match_type"
            , "-mt"
            , help="How to match tables between the source and target destinations. Strict will only create relations "
                   "if table names match exactly, Fuzzy will attempt to create relations using a fuzzy match."
            , case_sensitive=False
        )
):
    """Given an upstream and downstream path, infers lineage based on table/column names and creates the edges."""
    client = cli_client_factory(bigeye_conf, config_file, workspace)
    lineage_controller = LineageController(client)

    # Get matching tables
    matching_tables = lineage_controller.get_matching_tables_from_selectors(upstream_selector=upstream_selector,
                                                                            downstream_selector=downstream_selector,
                                                                            match_type=match_type)

    log.info(f'Identified {len(matching_tables)} table relationships between upstream and downstream sources.')

    lineage_controller.infer_column_level_lineage_from_tables(matching_tables)
