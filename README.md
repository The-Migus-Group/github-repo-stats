![PyPI Version](https://img.shields.io/pypi/v/github-repo-stats) ![License](https://img.shields.io/github/license/the-migus-group/github-repo-stats) ![Python Versions](https://img.shields.io/pypi/pyversions/github-repo-stats)

# GitHub Repo Stats

Fetch your repo stats from the GitHub API. Stats currently reported include:

- Forks
- Stars
- Watchers
- Clones Total
- Clones Unique
- Views Total
- Views Unique

## SetUp

In order to use tool, you will require a GitHub [personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) which will be used to authenticate you on each API call.

This should be set as an evironment variable named `GH_TOKEN`. Alternatively, you an pass it directly as an option into the cli with the `-t` / `--auth-token` flag.

## Install

Install the latest version from PyPi with:

```
python -m pip install github-repo-stats
```

## Use

```
Usage: cli.py [OPTIONS]

  Fetch GitHub repo stats!

  REQUIRES either a repos yaml file, an org name, or a user's name.

  Typical usage:

      $ gh-stats -r example.yaml

      $ gh-stats --repos example.yaml --output-file path/to/file.csv

Options:
  -r, --repos PATH        Yaml representation of Repos to Pull
  -o, --org TEXT          Pull stats for all repos owned by Org
  -u, --user TEXT         Pull stats for all repos owned by User
  -f, --output-file PATH  Output file path. Only supports CSV or JSON
  -t, --auth-token TEXT   GitHb Access Token
  --help                  Show this message and exit.
```

## Development

For local development, you may find it easier to add an `.env` file to the project root with your `GH_TOKEN`. But setting it explicitly in the environment will also work.

All dev dependencies can be found in the `requirements.txt` file.

This project uses `pytest` for testing. If creating a PR, please use `tox` to run the tests against all supported Python versions.
