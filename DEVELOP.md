### Development

Install [Poetry](https://python-poetry.org/) and project's dependencies

```bash
$ poetry install
```

Add new feature and launch tests

```bash
$ poetry run pytest -sv tests
```

### Releasing

Bump a version with features you want to include and build a package

```bash
$ poetry version  # patch version update
$ poetry version minor
$ poetry version major  # choose one based on semver rules
$ poetry build  # better to use the command below
$ make build
```

Upload package to GitHub and PyPI

```bash
$ git tag -a v0.4.2 -m "Version 0.4.2"
$ git push --tags
$ poetry publish
```
