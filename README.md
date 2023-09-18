<!-- 
[concourse-image]: https://ci.something.net/api/v1/teams/pipelines/xmeligibility/jobs/build-and-store/badge
[concourse-url]: https://ci.something.net/pipelines/something?group=Build%20Version%20and%20Deploy%20Lower%20Env
[version]: readme_resources/badges/version.svg
[pylint-scores]: readme_resources/badges/pylint.svg
[code-cov]: readme_resources/badges/coverage.svg
[code-size]: readme_resources/badges/size.svg 
-->

# FastAPI
*Author:* EJohnston

<!-- [![Build Status][conourse-image]][concourse-url]
![Version][version]
![Code Coverage][code-cov]
![Pylint Scores][pylint-scores] -->

##### Overview

##### Why does this project exist?
-


## Usage example

Link to sample request/response payloads should go here.
Please add links to swagger or documentation sample payload bodies and the location of the endpoints.

<br>

```

```

<img src=https://image-source/README.png height=75px width=75px />

## Development

<!--Describe from start to end how to install, run,
and test the project, even if it seems trivial.-->

### S3 Non Secret Environment Variables
### for now setting `run_local='true'` will handle configurations.

All non-secret environment variables reside in the environment_variables/ directory, separated by file
for each development environment.

WARNING: Be sure to place all secret values in secrets manager, as these files will be
pushed to github and will be exposed to other teams who have access to the Repo_Standard
project.

The environment variables changed in these files will be automatically written to S3 by the
Concourse pipeline upon pushing to Github, should you merge to master, or change your pipeline.yml
file to use your working branch.

#### Run
<!--This section should include code snippets, for configuring the execution of your project-->

```
sh start.sh
```
After startup has initialized you can call localhost:80/health
to ensure the server is up and running.
<br>
OR
<br>
set your environment to debug debug_app.py
and run from there.

#### Test

The intended entrypoint for writing dynamic tests is the `tests/conftest.py` file. Below is an annotated description of each element
of the pytest framework for Repo Standard projects.

The only manual step for configuring tests is creating a configuration object in json file with
key: <secrets_prefix>/<version>/<stage>.json

```python
from tests.testutils import MockContext, patch_metrics_decorators


patch_metrics_decorators()
```
_Each of the non-fixtures needed to configure tests, such as the MockContext object and the patch_metrics_decorators are stored in the `test/testutils.py`
file._

```python
@pytest.fixture(autouse=True, scope="session")
def module_setup_teardown():
    """
    This fixture can be used for basic setup and teardown at the module level.

    autouse=True This fixture will be used by default. Please flip the switch to
    False if you would like to run your unit tests without the setup / teardown, but beware,
    it will remove the patched dependencies.
    """
    ENVS_TO_SET = [
        ("secrets_prefix", "secret-prefix-name"),
        ("stage", "dev"),
        ("version", "0.0.0"),  # TODO: Make sure to set version for each deployed
        ("region", "us-east-2"),
    ]
    for key, value in ENVS_TO_SET:
        os.environ[key] = value

    patch = mock.patch("main.request_handler.Log").start()

    yield
    patch.stop()
```
_Though the docstring speaks for itself, the module setup and teardown fixture is used to configure environment variables and patches that will be
globally set for the entire test session. An opportunity exists to parametrize this fixture to run integration tests against different stages, versions,
and regions._

```python
@pytest.fixture()
def request_handler():
    yield RequestHandler()
```
_The request_handler fixture is used throughout tests to manually instantiate a request handler. This pattern can be duplicated / modified as
the handler/controller models get adapted._

```python

Event = namedtuple(
    "Event",
    "resource httpMethod queryStringParameters body headers exp_status",
    defaults=("/sample", "POST", {}, "", {}, None),
)

configurations = [Event(body=json.dumps({"test": "value"}))]

@pytest.fixture(params=configurations)
def event(base_event, request):
    base_event.update(request.param._asdict())

    yield base_event
```
_Individual Event objects can be configured within the configurations list. Each configuration will be run against each expected passing test
throughout the testing framework. Note how the event fixture inherits a base_event object._

```python
mal_configurations = [
    Event(resource="/invalid", exp_status=404),
    Event(resource="/sample", httpMethod="GET", exp_status=404),
]
...
```
_The same practice can be applied to the mal_configurations list, for events intended to be run against each failing test._

##### Local code coverage
```bash
pytest src/tests --cov main -v -ra --color=yes --cov-config=coverage_config --html=cov_test/test_report.html --cov-report term-missing --cov-report html:cov_test
```

#### Lint
```
 pylint src/
```


### Lessons Learned
<!--Use this section to describe lessons that you have learned
throughout the development process thus far-->

OOPS! Nothing learned here...


### Recommended Tools
<!--Uncomment all that apply -->
    - fly
<!--  - [Vault CLI](https://www.vaultproject.io/docs/commands/)-->
<!--  - `aws_quick_auth`-->
<!--  - Others? -->


## Deployment

##### Concourse:
```
fly -t <team_name> sp -p pipeline-name -c ci/pipeline.yml -l ci/ci-values.yml
```
After setting the pipeline, webhooks will trigger builds from PRs and push to master. If you would like to manually trigger a build, run:

```
fly -t <team_name> up  pipeline-name
```

##### Jenkins: (deprecated)
```

```


<!-- Markdown link & img dfn's -->

<!--Verify that the urls are correct here -->
[concourse-image]: https://ci.something.net/api/v1/teams/<team_name>/pipelines/upsell-service/jobs/build-and-store/badge
[concourse-url]: https://ci.something.net/teams/<team_name>/pipelines/upsell-service?group=Build%20Version%20and%20Deploy%20Lower%20Env


<!--Update to latest version number of the package -->
[version]: readme_resources/badges/version.svg

<!--Verify that the url is correct here -->
[pylint-scores]: readme_resources/badges/pylint.svg

<!--Verify that the url is correct here -->
[code-cov]: readme_resources/badges/coverage.svg

[test-image]: https://github.something.com/<team_name>/ci-images/raw/master/images/README.png

## Release History

Use this as an optional location to dump quick notes about recent major version changes.
A more robust history of of version changes can be found in the changelog

###### Example:
* 0.2.1
    * CHANGE: Update docs (module code remains unchanged)
* 0.2.0
    * CHANGE: Remove `setDefaultXYZ()`
    * ADD: Add `init()`
* 0.1.1
    * FIX: Crash when calling `baz()` (Thanks @GenerousContributorName!)
* 0.1.0
    * The first proper release
    * CHANGE: Rename `foo()` to `bar()`
* 0.0.1
    * Work in progress

