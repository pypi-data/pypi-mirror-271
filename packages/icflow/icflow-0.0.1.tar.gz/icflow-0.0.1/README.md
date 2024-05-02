`icflow` is a Python package with some prototype 'workflow' tools for use in ICHEC.

# Goals
The goal is to use it to help convert tools and approaches used by ML 'domain experts' into a more standardized workflow by:

* Analysing incoming Juyter notebooks, models, datasets and runtime environments (conda/container)
* Identifying 'hard-coded' data that can be moved into config files
* Adding utility scripts and methods for fetching data and models as needed
* Describing a study as a workflow, using some scripts here to 'stitch' the workflow together

Ultimately we will end up using some common workflow tools across ICHEC, likely something established and open-source (eg MLFlow) - this package is intended to understand and flesh-out our workflow needs and start transforming how we set up studies to ultimately move to these more standard tools.

# Tests

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

