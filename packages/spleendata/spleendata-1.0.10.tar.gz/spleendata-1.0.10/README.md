# Spleen data downloader

[![Version](https://img.shields.io/docker/v/fnndsc/pl-spleendata?sort=semver)](https://hub.docker.com/r/fnndsc/pl-spleendata)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl-spleendata)](https://github.com/FNNDSC/pl-spleendata/blob/main/LICENSE)
[![ci](https://github.com/FNNDSC/pl-spleendata/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/pl-spleendata/actions/workflows/ci.yml)

`pl-spleendata` is a [_ChRIS_](https://chrisproject.org/) _FS_ plugin which downloads an exemplar spleen dataset useful for training and inference experiments.

## Abstract

This is a simple _FS_ plugin suitable for training and inference on 3D spleen NiFTI volumes, as part of the [MONAI spleen segmentation exemplar notebook](https://github.com/Project-MONAI/tutorials/blob/main/3d_segmentation/spleen_segmentation_3d.ipynb). _FS_ plugins are suitable as root nodes of ChRIS compute trees, i.e. the data node from which all processing continues. If you need to inject spleen data into a non-root tree node, use the [companion _DS_ spleen data node](https://github.com/FNNDSC/pl-spleendatads).

By default, the download is pretty big -- 1.2Gb, so make sure you have time and space. It is possible to post-download prune this. For example, if you are only interested in _training_, you can use a `--trainingOnly` flag which will prune out the 43Mb of testing NiFTI volumes. Conversely, if you are just interested in _inference_, the `--testingOnly` will remove the post download 1.2Gb of training data, saving lots of space.

You still need to download the whole set, however, before you can prune.

## Installation

`pl-spleendata` is a _[ChRIS](https://chrisproject.org/) plugin_, meaning it can run from either within _ChRIS_ or the command-line.

## Local Usage

### On the metal

If you have checked out the repo, you can simply run `spleendata` using

```shell
source venv/bin/activate
pip install -U ./
spleendata output/
```

### PyPI

Alternatively, you can just do a

```shell
pip install spleendata
```

to get directly from PyPI.

### apptainer

The recommended way is to use [Apptainer](https://apptainer.org/) (a.k.a. Singularity) to run `pl-spleendata` as a container:

```shell
apptainer exec docker://fnndsc/pl-spleendata spleendata [--args values...] output/
```

To print its available options, run:

```shell
apptainer exec docker://fnndsc/pl-spleendata spleendata --help
```

## Examples

`spleendata`, being a ChRIS _FS_ plugin, only requires one positional argument: a directory that will contain the output data. Simply create an empty `output`.

```shell
mkdir output
apptainer exec docker://fnndsc/pl-spleendata:latest spleendata [--args] incoming/ outgoing/
```

## Development

Instructions for developers.

### Building

Build a local container image:

```shell
docker build -t localhost/fnndsc/pl-spleendata .
```

### Running

Mount the source code `spleendata.py` into a container to try out changes without rebuild.

```shell
docker run --rm -it --userns=host -u $(id -u):$(id -g) \
    -v $PWD/spleendata.py:/usr/local/lib/python3.11/site-packages/spleendata.py:ro \
    -v $PWD/in:/incoming:ro -v $PWD/out:/outgoing:rw -w /outgoing \
    localhost/fnndsc/pl-spleendata spleendata /incoming /outgoing
```

### Testing

Run unit tests using `pytest`.
It's recommended to rebuild the image to ensure that sources are up-to-date.
Use the option `--build-arg extras_require=dev` to install extra dependencies for testing.

```shell
docker build -t localhost/fnndsc/pl-spleendata:dev --build-arg extras_require=dev .
docker run --rm -it localhost/fnndsc/pl-spleendata:dev pytest
```

## Release

Steps for release can be automated by [Github Actions](.github/workflows/ci.yml).
This section is about how to do those steps manually.

### Increase Version Number

Increase the version number in `setup.py` and commit this file.

### Push Container Image

Build and push an image tagged by the version. For example, for version `1.2.3`:

```
docker build -t docker.io/fnndsc/pl-spleendata:1.2.3 .
docker push docker.io/fnndsc/pl-spleendata:1.2.3
```

### Get JSON Representation

Run [`chris_plugin_info`](https://github.com/FNNDSC/chris_plugin#usage)
to produce a JSON description of this plugin, which can be uploaded to _ChRIS_.

```shell
docker run --rm docker.io/fnndsc/pl-spleendata:1.2.3 chris_plugin_info -d docker.io/fnndsc/pl-spleendata:1.2.3 > chris_plugin_info.json
```

Intructions on how to upload the plugin to _ChRIS_ can be found here:
https://chrisproject.org/docs/tutorials/upload_plugin

