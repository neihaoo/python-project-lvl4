# Task Manager (Hexlet Python Project Level 4)

[![Actions Status](https://github.com/neihaoo/python-project-lvl4/workflows/hexlet-check/badge.svg)](https://github.com/neihaoo/python-project-lvl4/actions)
[![Actions Status](https://github.com/neihaoo/python-project-lvl4/workflows/project-check/badge.svg)](https://github.com/neihaoo/python-project-lvl4/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/c20075eb9c7791f0dabb/maintainability)](https://codeclimate.com/github/neihaoo/python-project-lvl4/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/c20075eb9c7791f0dabb/test_coverage)](https://codeclimate.com/github/neihaoo/python-project-lvl4/test_coverage)

Task Manager is a task management system. It allows you to set tasks, assign performers and change their statuses. Registration and authentication are required to work with the system.

[View demo on Heroku](https://hexlet-project-task-manager.herokuapp.com)

## Requirements

* Python 3.8+
* Poetry
* GNU Make

## Setup

```sh
make setup
```

## Run server

```sh
make start
# Open http://localhost:8000
```

## Check codestyle

```sh
make lint
```

## Run tests

```sh
make test
make test-coverage-report # run tests with coverage report
```
