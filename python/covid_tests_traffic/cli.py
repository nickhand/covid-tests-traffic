import json

import click
import git
import pandas as pd
from rich.progress import track

from . import HOME_DIR

COVID_PAGES = ["covidtests.gov/", "special.usps.com/testkits", "covid.gov/tests"]


def load_commit_data(commit, filename="data.json"):
    """Iterate through commits."""

    blobs = commit.tree.blobs
    matches = list(filter(lambda b: b.name == filename, blobs))

    data = None
    if len(matches):

        data = json.loads(matches[0].data_stream.read())
        data = pd.DataFrame(data["data"]).assign(
            active_visitors=lambda df: df["active_visitors"].astype(int),
            datetime=data["taken_at"],
        )

    return data


@click.group()
@click.version_option()
def cli():
    """Data tool to analyze data for top government pages."""
    pass


def _update(start_commit=None):
    """Run the update."""

    # Initialize the repo
    top_folder = (HOME_DIR / ".." / "..").resolve()
    print(top_folder)
    repo = git.Repo(str(top_folder), odbt=git.GitDB)

    # The commits
    if start_commit is None:
        rev = "main"
    else:
        rev = f"{start_commit}..HEAD"
    commits = list(reversed(list(repo.iter_commits(rev))))
    if not len(commits):
        return

    # Outputs
    meta = {}
    out = []

    # Loop over each commit, with a progress bar
    for commit in track(
        commits,
        description="Processing...",
        total=len(commits),
    ):
        

        # Load the data for this commit
        df = load_commit_data(commit)

        # Process the data
        if df is not None:

            # Grab only the top pages
            covid = df.query("page in @COVID_PAGES")
            not_covid = df.query("page not in @COVID_PAGES")

            # Save
            out.append(
                pd.concat(
                    [
                        covid.groupby("datetime")["active_visitors"]
                        .sum()
                        .rename("covid_traffic"),
                        not_covid.groupby("datetime")["active_visitors"]
                        .sum()
                        .rename("other_traffic"),
                    ],
                    axis=1,
                ).reset_index()
            )

    # Save the metadata
    meta["committed_datetime"] = str(commit.committed_datetime)
    meta["hexsha"] = commit.hexsha

    # Combine the data
    out = pd.concat(out, ignore_index=True).sort_values("datetime")

    return out, meta


@cli.command()
def extract():
    """Save a fresh copy of the data."""

    # Update the data
    out, meta = _update()

    # Output folder
    top_folder = (HOME_DIR / ".." / "..").resolve()
    output_folder = top_folder / "processed"
    if not output_folder.exists():
        output_folder.mkdir(parents=True)

    # Save the data
    out.to_csv(output_folder / "data-covid-tests-traffic.csv", index=False)

    # Save the metadata
    json.dump(meta, open(output_folder / "meta.json", "w"))


@cli.command()
def update():
    """Update the data."""

    # Get the existing file name
    top_folder = (HOME_DIR / ".." / "..").resolve()
    output_folder = top_folder / "processed"
    filename = output_folder / "data-covid-tests-traffic.csv"

    assert filename.exists()

    # Load the existing data
    existing_data = pd.read_csv(filename)
    existing_meta = json.load(open(output_folder / "meta.json"))

    # Update the data
    new_data, new_meta = _update(existing_meta["hexsha"])

    # Combine the data
    combined_data = pd.concat([existing_data, new_data], ignore_index=True)

    # Save the data
    combined_data.to_csv(filename, index=False)

    # Save the metadata
    json.dump(new_meta, open(output_folder / "meta.json", "w"))
