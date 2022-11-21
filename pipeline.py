
import sys
import anyio
import dagger
import os
import re

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
        )
        r = re.compile("^GOODDATA_")
        for k, v in os.environ.items():
            if r.match(k):
                ctr = ctr.with_env_variable(k, v)
        ctr = ctr.exec(["python", "gd.py"])
        result = await ctr.stdout().contents()
        print(result)

if __name__ == "__main__":
    anyio.run(pipeline)
