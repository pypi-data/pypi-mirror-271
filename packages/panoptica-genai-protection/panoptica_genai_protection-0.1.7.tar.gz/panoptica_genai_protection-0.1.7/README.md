# Project Marvin
Marvin is intended to provide protection for LLM-driven components of software systems.

We do so by inspecting prompts (and in the future LLM responses to these prompts) with NLP techniques to determine if 
they are suspected to malicious activity. 

## Components
* [Marvin SDK](./sdk) - Python SDK to programmatically integrate system with LLM protection
* [Prompt Inspection Server](./prompt_inspection_server) - HTTP server to serve the requests made by Marvin SDK
* [Demo Chat App](./chat_app) - Simple streamlit-based chat app to demo Marvin capabilities

## Code Generation
### Python
We use auto-generated request/response models from OpenAPI spec,
using [datamodel-code-generator](https://koxudaxi.github.io/datamodel-code-generator/). 

The server spec is under [prompt/openapi/openapi.yaml](openapi/prompt_inspection.yaml).
We use its generated artifacts in both the client and the server.

_Note: Currently we only generate model files and not the client/server code utilizing them._

#### Installing `datamodel-code-generator`
```shell
pip install datamodel-code-generator
```
### Go
#### Installing `oapi-codegen`
```shell
go install github.com/deepmap/oapi-codegen/v2/cmd/oapi-codegen@latest
```

### Run UnitTests
```shell
make test
```

### Run Helm Chart Test and Linting
```shell
make helm-test
```

### Generating the `models.py` 
The following snippet would generate the `models.py` file with all the schema objects declared in `openapi.yaml`, 
and copy the generated file to its location in the SDK folder.

```shell
make generate
```

## CODEOWNERS
Please modify this file to include your team and CODEOWNER rules

## Jenkins pipeline
Please refer to the [SRE-Pipeline-Library](https://wwwin-github.cisco.com/pages/eti/sre-pipeline-library/) documentation for further information on how to modify your Jenkinsfile to your needs

### `docker-compose.yaml`
This file will create a system that includes postgres and the backend.
to start follow this steps
```
cd attack-analytics
docker-compose -f docker-compose.yaml up db --build -d
docker-compose -f docker-compose.yaml up migration --build -d
docker-compose -f docker-compose.yaml up forensic --build -d
```

### system tests
If you want to check a test you just added, follow this steps:
1. Let's say you need to add test_flow_name = 'send_complex_prompt', and want to test category = 'dan' 
2. go to .github/workflows/run-system-tests.yaml and add test_flow_name choice: 'send_complex_prompt', add attack_category choice: 'dan'
3. go to .github/workflows/main.yaml and add to run-system-tests strategy matrix under xss_injection. E.g.,
```yaml
        include:
          - test_flow_name: send_prompt
            attack_category: xss_injection
          - test_flow_name: send_complex_prompt
            attack_category: dan 
```

## Python requirements
we use poetry CLI to handle our python packages.
prerequisites: `brew install poetry`
to run poetry cd to a folder containing `pyproject.toml` file. example of poetry handling:
1. poetry install --no-root - install current dependencies into your venv
2. poetry update - update and install latest packages with given constraints from pyproject.toml
3. poetry lock - update and checks dependencies in lock file