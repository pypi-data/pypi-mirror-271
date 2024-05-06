# winion
![pypi](https://img.shields.io/pypi/v/winion.svg)
![versions](https://img.shields.io/pypi/pyversions/winion.svg)

A producer/consumer async runtime for Python

## Usage

1. Install the package from pypi

```console
> pip install winion
```

## Development

This repository manages the dev environment as a Nix flake and requires [Nix to be installed](https://github.com/DeterminateSystems/nix-installer)

```console
> nix develop -c $SHELL
```

```console
> make setup
```

```console
> make test
```

## Publish Package to PyPi

```console
> make pypi
```

## License

`winion` is released under the [MIT license](./LICENSE)
