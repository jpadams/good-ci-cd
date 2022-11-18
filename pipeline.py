"""
Execute a command
"""

import sys
import anyio
import dagger
import gooddata_sdk
from gooddata_sdk.catalog.workspace.entity_model.workspace import CatalogWorkspace
import os


async def pipeline():
    config = dagger.Config(log_output=sys.stderr)

    async with dagger.Connection(config):
        host = os.getenv('GOODDATA_HOST')
        token = os.getenv('GOODDATA_TOKEN')
        staging_workspace_id = os.getenv('GOODDATA_STAGING_WORKSPACE_ID')
        production_workspace_id = os.getenv('GOODDATA_PRODUCTION_WORKSPACE_ID')

        sdk = gooddata_sdk.GoodDataSdk.create(host, token)

        sdk.catalog_workspace.create_or_update(
            CatalogWorkspace(production_workspace_id, production_workspace_id)
        )

        declarative_ldm = sdk.catalog_workspace_content.get_declarative_ldm(staging_workspace_id)
        declarative_analytics_model = sdk.catalog_workspace_content.get_declarative_analytics_model(
            staging_workspace_id
        )

        sdk.catalog_workspace_content.put_declarative_ldm(
            production_workspace_id,
            declarative_ldm
        )
        sdk.catalog_workspace_content.put_declarative_analytics_model(
            production_workspace_id,
            declarative_analytics_model
        )

        print("done")


if __name__ == "__main__":
    anyio.run(pipeline)
