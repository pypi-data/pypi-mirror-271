`icsystemutils` is a Python package with some low-level utilities for interacting with real system resources (cpu, gpu, network etc).

It is maintained by the Irish Centre for High End Computing (ICHEC), mostly as a dependency of high-level packages and tools used to support ICHEC research and workflows.

It is made public in support of Open Science - however it is primarily intended as an internal tool to support our activities. 

The project aims to:

* Build a common set of low-level utilities for interacting with system resources for ICHEC activities
* Keep dependencies to a minimum - bearing in mind many more established and capable tools exist, but with more dependencies and features than we may need
* Build software development, packaging and delivery experience at ICHEC

The project does not aim to:

* Replace any established tool in this area - if there is a more suitable tool it should be used, this project is just a fallback for use under certain conditions - e.g. dependency issues or complexity in other tools.

# Running Tests

In a Python virtual environment do:

```sh
pip install .'[test]'
```

## Unit Tests

```sh
pytest
```

## Linting and Static Analysis

```sh
black src test
mypy src test
```

## All Tests

Requires `tox`:

```sh
tox
```

