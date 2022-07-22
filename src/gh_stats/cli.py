import csv
import json
import os
from pathlib import Path

import click
import requests
import yaml
from rich.console import Console
from rich.table import Table
from typing import Union


def check_response(response, repo) -> Union[str, dict]:
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Repo {repo} returned this error: ", response.text)


def get_repo_data(headers: dict, owner: str, repo: str) -> dict:
    """Fetches all data required for output for each repo"""

    resp_data, views, clones = None, None, None

    resp = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers=headers)

    resp_data = check_response(resp, repo)

    views_resp = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/traffic/views", headers=headers
    )

    views = check_response(views_resp, repo)

    clones_resp = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/traffic/clones", headers=headers
    )

    clones = check_response(clones_resp, repo)

    if all([resp_data, views, clones]):
        return {
            "Repo": f"{owner}/{repo}",
            "Forks": resp_data["forks_count"],
            "Stars": resp_data["stargazers_count"],
            "Watchers": resp_data["watchers_count"],
            "Clones Total": clones["count"],
            "Clones Unique": clones["uniques"],
            "Views Total": views["count"],
            "Views Unique": views["uniques"],
        }


def parse_repos_list_from_yaml(file) -> dict:
    """Parses the YAML file and converts to Python objects"""
    with open(file) as yaml_file:
        return yaml.safe_load(yaml_file)


def fetch_owners_repos(headers: str, name: str, repo_type: str) -> dict:
    """Fetch the owners repos - org or user"""
    owner = name.strip().strip("/")
    org_repos = requests.get(
        f"https://api.github.com/{repo_type}/{owner}/repos", headers=headers
    ).json()
    repo_names = [repo["name"] for repo in org_repos]
    return {"Owners": [{owner: repo_names}]}


@click.command()
@click.option(
    "-r",
    "--repos",
    type=click.Path(exists=True),
    help="Yaml representation of Repos to Pull",
)
@click.option("-o", "--org", help="Pull stats for all repos owned by Org")
@click.option("-u", "--user", help="Pull stats for all repos owned by User")
@click.option(
    "-f", "--output-file", type=Path, help="Output file path. Only supports CSV or JSON"
)
@click.option("-t", "--auth-token", help="GitHub Access Token")
def main(repos, org, user, output_file, auth_token):
    """Fetch GitHub repo stats!

    REQUIRES either a repos yaml file, an org name, or a user's name.

    Typical usage:
    \n\t$ gh-stats -r example.yaml
    \n\t$ gh-stats --repos example.yaml --output-file path/to/file.csv
    """

    if auth_token:
        HEADERS = {"Authorization": f"token {auth_token}"}
    else:
        if os.getenv("GH_TOKEN") is not None:
            HEADERS = {"Authorization": f"token {os.getenv('GH_TOKEN')}"}
        else:
            raise ValueError("Please set a GitHub Access Token.")

    if repos:
        repos_dict = parse_repos_list_from_yaml(repos)

    elif org:
        repos_dict = fetch_owners_repos(HEADERS, org, "orgs")

    elif user:
        repos_dict = fetch_owners_repos(HEADERS, user, "users")

    else:
        raise ValueError("Please provide a yaml file, owner, or user.")

    final_data = []
    for repo_owner in repos_dict["Owners"]:
        key = next(iter(repo_owner))
        for repo in repo_owner[key]:
            data = get_repo_data(HEADERS, key, repo)

            if data:
                final_data.append(data)

    if final_data:

        if output_file:
            file_path = Path(output_file)

            if file_path.suffix == ".csv":
                print("Creating CSV")
                with open(file_path, "w", newline="") as file:
                    writer = csv.DictWriter(
                        file,
                        fieldnames=[
                            "Repo",
                            "Forks",
                            "Stars",
                            "Watchers",
                            "Clones Total",
                            "Clones Unique",
                            "Views Total",
                            "Views Unique",
                        ],
                    )
                    writer.writeheader()

                    for data in final_data:
                        writer.writerow(
                            {
                                "Repo": data["Repo"],
                                "Forks": data["Forks"],
                                "Stars": data["Stars"],
                                "Watchers": data["Watchers"],
                                "Clones Total": data["Clones Total"],
                                "Clones Unique": data["Clones Unique"],
                                "Views Total": data["Views Total"],
                                "Views Unique": data["Views Unique"],
                            }
                        )

                print("CSV file created.")

            elif file_path.suffix == ".json":
                print("Creating JSON")
                with open(file_path, "w") as file:
                    file_data = {"Data": [data for data in final_data]}
                    file.write(json.dumps(file_data, indent=4))

            else:
                raise ValueError("Output file must be CSV or JSON")

        else:

            table = Table(title="GitHub Stats")
            table.add_column("Repo")
            table.add_column("Forks", justify="center")
            table.add_column("Stars", justify="center")
            table.add_column("Watchers", justify="center")
            table.add_column("Clones Total", justify="center")
            table.add_column("Clones Unique", justify="center")
            table.add_column("Views Total", justify="center")
            table.add_column("Views Unique", justify="center")

            for data in final_data:
                table.add_row(
                    str(data["Repo"]),
                    str(data["Forks"]),
                    str(data["Stars"]),
                    str(data["Watchers"]),
                    str(data["Clones Total"]),
                    str(data["Clones Unique"]),
                    str(data["Views Total"]),
                    str(data["Views Unique"]),
                )

            console = Console()
            console.print(table)


if __name__ == "__main__":
    main()
