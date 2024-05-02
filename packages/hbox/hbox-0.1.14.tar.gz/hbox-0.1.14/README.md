# hbox

[![CI](https://img.shields.io/github/actions/workflow/status/helton/hbox/production.yml?branch=main&logo=github&label=CI)](https://github.com/helton/hbox/actions?query=event%3Apush+workflow%3A%22Deploy+%28Production%29%22)
[![pypi](https://img.shields.io/pypi/v/hbox.svg)](https://pypi.python.org/pypi/hbox)
[![versions](https://img.shields.io/pypi/pyversions/hbox.svg)](https://github.com/helton/hbox)
[![license](https://img.shields.io/github/license/helton/hbox.svg)](https://github.com/helton/hbox/blob/main/LICENSE)

hbox is a Command Line Interface (CLI) that leverages container technology to manage packages.

## Features

hbox offers the following features:

- **Container Isolation**: hbox uses containers to isolate packages, allowing multiple versions of a package to coexist without conflict.
- **Robust Configuration Options**: hbox enables high customization through configuration files. You can define package aliases and setup automatic volume mounts via `config.json`.
- **Support for Pipes**: hbox supports the use of pipes in `hbox run`, which allows you to chain commands efficiently.
- **Convenient Shims**: hbox creates `shims` (alias shortcuts) for all installed packages, simplifying command entry from `hbox run <package alias> <commands>` to `<package alias> <commands>`.

## Commands

```sh
$ hbox
usage: hbox [-h] {info,version,list,add,install,remove,uninstall,run,use,set} ...

CLI tool that leverages container technology to manage packages.

positional arguments:
  {info,version,list,add,install,remove,uninstall,run,use,set}
                        Available commands
    info                Print debug information.
    version             Show current hbox version.
    list                List all installed packages and their versions.
    add (install)       Add a specific version of a package
    remove (uninstall)  Remove a package.
    run                 Run the package.
    use (set)           Set current version of a package.

options:
  -h, --help            show this help message and exit
```

## Installation

You can install hbox via `pip` or your preferred package manager.
To install hbox via `pip`, run the following command:

```sh
pip install hbox
```

## Setup

### Shims and Shell Configuration

hbox utilizes shims and a configuration file to effectively manage your installed packages. For the successful addition of `$HBOX_DIR/shims` at the correct priority level to your path, these lines of code should be added to your `.bashrc` or `.zshrc` file:

```sh
export HBOX_DIR="$HOME/.hbox"
export PATH="$HBOX_DIR/shims":$PATH
```

### Configuration via config.json

The configuration of packages in hbox is managed by the `$HBOX_DIR/config.json` file. This file, which is created automatically upon adding a package, contains information such as package aliases pointing to multiple registries and volume mounts:

```json
{
  "debug": false,
  "packages": {
    "curl": {
      "image": "docker.io/curlimages/curl"
    },
    "aws": {
      "image": "docker.io/amazon/aws-cli",
      "volumes": [
        {
          "source": "~/.aws",
          "target": "/root/.aws"
        }
      ]
    },
    "lambda_python": {
      "image": "public.ecr.aws/lambda/python"
    },
    "jq": {
      "image": "ghcr.io/jqlang/jq"
    },
    "terraform": {
      "image": "docker.io/hashicorp/terraform"
    },
    "fga": {
      "image": "docker.io/openfga/cli"
    }
  }
}
```

You can use the `config.json` to also override the registry of any container image. By default, we pull from `docker.io`.

### Package Version Management via versions.json

hbox also creates and maintains a `$HBOX_DIR/versions.json` file that keeps track of the current version of each package. This file is under the management of hbox itself and shouldn't be manually edited:

```json
{
  "packages": [
    {
      "name": "aws",
      "versions": [
        "latest"
      ],
      "current": "latest"
    },
    {
      "name": "jq",
      "versions": [
        "latest",
        "1.7rc2"
      ],
      "current": "1.7rc2"
    },
    {
      "name": "node",
      "versions": [
        "latest",
        "14",
        "15"
      ],
      "current": "15"
    }
  ]
}
```

## Usage

Below are some examples demonstrating how you can use `hbox`:

```sh
> hbox version
0.1.1
> hbox list
> hbox add jq
latest: Pulling from jqlang/jq
...
Added 'jq' version latest.
> hbox list jq
- jq:
  - latest ✔
> jq --version
jq-1.7.1
> hbox add node latest
latest: Pulling from library/node
...
Added 'node' version latest.
> hbox list
- jq:
  - latest ✔
- node:
  - latest ✔
> hbox list node
- node:
  - latest ✔
> node --version
v22.0.0
> hbox add node 14 --set-default
'node' version 14 set as default.
14: Pulling from library/node
...
Added 'node' version 14.
> hbox list node
- node:
  - 14 ✔
  - latest
> node --version
v14.21.3
> hbox use node latest
'node' set to version latest
> node --version
v22.0.0
> hbox list node
- node:
  - 14
  - latest ✔
```

These examples should provide a quick start guide for you to understand the basic operations that you can perform with hbox.

## To do

- Support `podman`
- Support private registries and mirrors
  - maybe via registry mapping in `config.json`?
- Support local overrides for package versions
  - use merged version to allow partial overrides?
- Organize an index of packages outside this source repo
  - maybe another repo `hbox-py-index`?
- Add auto update
- Add option to keep containers instead of using `--rm`
  - maybe adding custom tags to them to identify them easily?
- Add GitHub Actions to build and publish to PyPI
- Add unit and integration tests
  - it should run on Linux and Windows 
- Double check if registered packages are available locally before using them
- Add warn when a shim will conflict with an existing command
- Add `hbox config` to support all `config.json` options
- [Experimental] Identify paths in `hbox run` to map them via container volumes automatically
- Separate `packages.json` from `config.json`
  - Allow use to override `packages.json` retrieved from centralized index/repo
- Add `hbox update` to update index
- Add `hbox register` to register a package, even with custom image
- Add option to remove images when removing packages
- Add support to colors in `hbox run` output when possible (*nix only?)
