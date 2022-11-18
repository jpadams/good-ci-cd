# Good CI/CD

## Overview

An example of data analytics automation using CI/CD.

Two main tools:

- [Dagger](https://dagger.io/) - Dagger is agnostic to pipeline vendors, it means you can build your pipeline locally and then push to GitLab, GitHub, etc.
- [GoodData](https://www.gooddata.com/?utm_medium=example&utm_source=github.com&utm_campaign=gooddata_dagger&utm_content=autor_patrik) - GoodData allows you to create consistent metrics and dashboards and access them using [GoodData Python SDK](https://www.gooddata.com/developers/cloud-native/doc/cloud/api-and-sdk/python-sdk/).

## Getting started

### Setup virtual environment

Set up a virtual environment:

**Create virtual environment**:

```bash
$ virtualenv venv
```

**Activate virtual environment**:

```bash
$ source venv/bin/activate
```

You should see a `(venv)` appear at the beginning of your terminal prompt indicating that you are working inside the `virtualenv`.

**Leave virtual environment run**:

```bash
$ deactivate
```

### Setup env variable in virtual environments

```bash
export GOODDATA_HOST=<gooddata-uri>
export GOODDATA_TOKEN=<gooddata-api-token>
export GOODDATA_STAGING_WORKSPACE_ID=<staging-workspace-id>
export GOODDATA_PRODUCTION_WORKSPACE_ID=<production-workspace-id>
```

### Install dependencies

```bash
$ pip install dagger-io
$ pip install gooddata-sdk
```

### Run pipeline

If you want to run pipeline locally, just run:

```bash
$ python pipeline.py
```
