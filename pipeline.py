"""
Execute a command
"""
import anyio
import os
import sys
import dagger
    
host = os.getenv('GOODDATA_HOST')
token = os.getenv('GOODDATA_TOKEN')
staging_workspace_id = os.getenv('GOODDATA_STAGING_WORKSPACE_ID')
production_workspace_id = os.getenv('GOODDATA_PRODUCTION_WORKSPACE_ID')

script="""\
import gooddata_sdk
from gooddata_sdk.catalog.workspace.entity_model.workspace import CatalogWorkspace

sdk = gooddata_sdk.GoodDataSdk.create('{host}', '{token}')
sdk.catalog_workspace.create_or_update(CatalogWorkspace('{production_workspace_id}', '{production_workspace_id}'))

declarative_ldm = sdk.catalog_workspace_content.get_declarative_ldm('{staging_workspace_id}')
declarative_analytics_model = sdk.catalog_workspace_content.get_declarative_analytics_model('{staging_workspace_id}')

sdk.catalog_workspace_content.put_declarative_ldm('{production_workspace_id}', declarative_ldm)
foo = sdk.catalog_workspace_content.put_declarative_analytics_model('{production_workspace_id}', declarative_analytics_model)
print(foo)
print("done")\
""".format(host=host, token=token, staging_workspace_id=staging_workspace_id, production_workspace_id=production_workspace_id)


async def pipeline():
    config = dagger.Config(log_output=sys.stderr)
    async with dagger.Connection(config) as client:
        ctr = ( 
             client.container()
            .from_("python:alpine")
            .exec(["pip", "install", "gooddata-sdk"])
            .exec(["echo", script, ">", "gd.py"])
            .exec(["python", "gd.py"])
        )
        result = await ctr.stdout().contents()
        print(result)

if __name__ == "__main__":
    anyio.run(pipeline)
