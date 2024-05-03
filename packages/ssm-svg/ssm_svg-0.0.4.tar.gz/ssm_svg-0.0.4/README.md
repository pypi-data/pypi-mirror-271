# ssm

SVG spritesheet maker

[![CI](https://github.com/obeezzy/ssm/actions/workflows/main.yml/badge.svg)](https://github.com/obeezzy/ssm/actions/workflows/main.yml)
[![Deployment to PyPI](https://github.com/obeezzy/ssm/actions/workflows/deploy.yml/badge.svg?branch=v0.0.4)](https://github.com/obeezzy/ssm/actions/workflows/deploy.yml)

__ssm__ is a simple approach to creating and managing SVG spritesheets. It has 5 main functions:

* __create__: For creating spritesheets from a list of SVG sprites (i.e. SVG icons etc.)
* __list__: For listing the SVG sprites stored in a spritesheet
* __add__: For adding SVG sprites to an existing spritesheet
* __remove__: For removing SVG sprites from an existing spritesheet
* __export__: For exporting SVG sprites from an existing spritesheet. Can be used for converting a `<symbol>` back into a standalone `<svg>` or to display a format suitable for HTML (using `<use>`).

For more details, run `python -m ssm -h` after installation.

## Installation
To install the most stable version of this package, run:
```bash
$ pip install ssm-svg
```

## Usage example

Create spritesheet `icons.svg` with `search.svg` and `menu.svg` as sprites:

```bash
$ python -m ssm create -f icons.svg search.svg menu.svg
```

Create spritesheet and overwrite existing file:

```bash
$ python -m ssm create -f icons.svg search.svg menu.svg -F
```

Create spritesheet with custom ID `hamburger-icon` instead of defaulting to its file name:

```bash
$ python -m ssm create -f icons.svg search.svg hamburger-icon=menu.svg
```

List IDs of SVG sprites in spritesheet:

```bash
$ python -m ssm list -f icons.svg
```

Add SVG sprites to spritesheet:

```bash
$ python -m ssm add -f icons.svg facebook.svg instagram.svg
```

Remove SVG sprites with IDs `facebook` and `instagram` from spritesheet:

```bash
$ python -m ssm remove -f icons.svg facebook instagram
```

NOTE: Inserting the same ID more than once would cause an error.

Add SVG sprites to spritesheet with custom ID `fb-icon` instead of defaulting to its file name:

```bash
$ python -m ssm add -f icons.svg fb-icon=facebook.svg
```

Export sprite with ID `search` from spritesheet:

```bash
$ python -m ssm export -f icons.svg search
```

Export sprite with ID `search` from spritesheet for use in HTML:

```bash
$ python -m ssm export -f icons.svg search --use
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
