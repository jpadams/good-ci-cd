
import sys
import anyio
import dagger
import os

host = os.getenv('GOODDATA_HOST')
token = os.getenv('GOODDATA_TOKEN')
staging_workspace_id = os.getenv('GOODDATA_STAGING_WORKSPACE_ID')
production_workspace_id = os.getenv('GOODDATA_PRODUCTION_WORKSPACE_ID')

async def pipeline():
    config = dagger.Config(log_output=sys.stderr)
    async with dagger.Connection(config) as client:

        src_id = await client.host().directory(".", include=["gd.py"]).id()

        ctr = ( 
             client.container()
            .from_("python:alpine")
            .exec(["pip", "install", "gooddata-sdk"])
            .with_mounted_directory("/src", src_id)
            .with_workdir("/src")
            .with_env_variable('GOODDATA_HOST', host)
            .with_env_variable('GOODDATA_TOKEN', token)
            .with_env_variable('GOODDATA_STAGING_WORKSPACE_ID', staging_workspace_id)
            .with_env_variable('GOODDATA_PRODUCTION_WORKSPACE_ID', production_workspace_id)
            .exec(["python", "gd.py"])
        )
        result = await ctr.stdout().contents()
        print(result)

if __name__ == "__main__":
    anyio.run(pipeline)
