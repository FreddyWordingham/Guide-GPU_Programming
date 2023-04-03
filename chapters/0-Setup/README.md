# Project Setup

## Poetry Init

Create a new `Poetry` project:

```shell
poetry init
```

-   I'm going to call this project `mandybrot_gpu`
-   Starting at version `0.1.0`
-   My description will be: `Plot the magical Mandelbrot set with a GPU.`
-   I am: `FreddyWordingham <freddy@digilab.co.uk>`
-   I'm not going to add a license
-   Compatible with Python versions `3.8` and above
-   And I'm not going to add any dependencies right now

This will generate a [`pyproject.toml`](./pyproject.toml) file containing the project metadata.

## Add .gitignore

I'm going to add a [`.gitignore`](./.gitignore) file to my project.
Python projects use a lot of files that we don't want to commit to Git, so we can use a `.gitignore` to tell Git to ignore them.

I'm going to pull the code from https://www.toptal.com/developers/gitignore/api/python into a `.gitignore` file using the `curl` command:

```shell
curl -L https://www.toptal.com/developers/gitignore/api/python > .gitignore
```

## Create a package

```shell
mkdir mandybrot_gpu
touch mandybrot_gpu/__init__.py
```

Install the package:

```shell
poetry install
```

## Test it

```shell
poetry run python -c "import mandybrot_gpu && print('Hello, World!')"
```

## Return

[Return to the top-level README](./../../README.md)
