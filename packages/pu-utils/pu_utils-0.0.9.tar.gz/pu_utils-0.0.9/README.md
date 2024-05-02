# Pulumi utils

Some random stuff to help writing Pulumi script easier.

This package is initially created to write deployment script for API Gateway backed by AWS Lambda.

This is a Python-only package. Only Python 3.is supported. Former versions may still work, but I
don't have enough effort to test for them.

## Install

```sh
pip install pu-utils
```

## Usage

TBD

## Limitations

- No multi-region support. This library assumes all the resources are in the same region

## How to release

```sh
./scripts/build.sh
twine upload dist/*
```
