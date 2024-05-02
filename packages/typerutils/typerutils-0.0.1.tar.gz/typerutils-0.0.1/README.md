# typerutils

[Typer](https://typer.tiangolo.com/) utility helpers

## Usage

Install the package from pypi

```console
> pip install typerutils
```

## Development

This repository manages the dev environment as a Nix flake and requires [Nix to be installed](https://github.com/DeterminateSystems/nix-installer)

```console
> nix develop -c $SHELL
```

```shell
> make setup
```

```shell
> make test
```

## Publish Package to PyPi

```shell
> make pypi
```

## License

`typerutils` is released under the [MIT license](./LICENSE)
