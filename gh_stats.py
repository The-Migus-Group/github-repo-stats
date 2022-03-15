import csv
import click
import requests
import yaml
from dotenv import dotenv_values
from rich.console import Console
from rich.table import Table


def get_repo_data(headers: dict, owner: str, repo: str) -> dict:
    """Fetches all data required for output for each repo"""
    rep_data = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}", headers=headers
    ).json()

    views = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/traffic/views", headers=headers
    ).json()

    clones = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/traffic/clones", headers=headers
    ).json()

    return {
        "Repo": f"{owner}/{repo}",
        "Forks": rep_data["forks_count"],
        "Stars": rep_data["stargazers_count"],
        "Watchers": rep_data["watchers_count"],
        "Clones Total": clones["count"],
        "Clones Unique": clones["uniques"],
        "Views Total": views["count"],
        "Views Unique": views["uniques"],
    }


def parse_repos_list_from_yaml(file) -> dict:
    """Parses the YAML file and converts to Python objects"""
    with open(file) as yaml_file:
        return yaml.safe_load(yaml_file)


@click.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--output", default=None)
def main(file, output):
    """Fetch GitHub repo stats!"""

    config = dotenv_values(".env")
    headers = {"Authorization": f"token {config.get('TOKEN')}"}

    repos = parse_repos_list_from_yaml(file)

    if output is not None and output == "csv":
        with open("data.csv", "w") as file:
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

            for repo_owner in repos["Owners"]:
                owner = next(iter(repo_owner))
                for repo in repo_owner[owner]:
                    data = get_repo_data(headers, owner, repo)

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

        for repo_owner in repos["Owners"]:
            owner = next(iter(repo_owner))
            for repo in repo_owner[owner]:
                data = get_repo_data(headers, owner, repo)

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
