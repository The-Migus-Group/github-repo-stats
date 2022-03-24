# GitHub Repo Stats


## SetUp
In order to use tool, you will require a GitHub [personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) which will be used to authenticate you on each API call.

This should be set as an evironment variable named `GH_TOKEN`. Alternatively, you an pass it directly as and option into the cli with the `-t` / `--auth-token` flag.

## Install 

TODO:


## Use

```
Usage: gh_stats.py [OPTIONS]

  Fetch GitHub repo stats!

  TODO: Add usage instructions for cli --help

Options:
  -r, --repos PATH        Yaml representation of Repos to Pull
  -o, --org TEXT          Pull stats for all repos owned by Org
  -u, --user TEXT         Pull stats for all repos owned by User
  -f, --output-file PATH  Output file path. Only supports CSV or JSON
  -t, --auth-token TEXT   GitHb Access Token
  --help                  Show this message and exit.
```
