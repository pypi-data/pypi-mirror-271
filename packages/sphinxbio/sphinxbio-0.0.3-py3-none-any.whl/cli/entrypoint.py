import os

import click
from pydantic import BaseModel
from sphinxbio.client import SphinxBio
from sphinxbio.environment import SphinxbioEnvironment

from .utils import find_subclasses


@click.group()
def cli():
    pass


@cli.group()
def datasets():
    pass


sphinx_api_key = os.environ.get("SPHINX_API_KEY")
if sphinx_api_key is None:
    raise ValueError("Please set SPHINX_API_KEY environment variable")

client = SphinxBio(
    environment=SphinxbioEnvironment.PRODUCTION,
    # Grab from environment variables
    username=sphinx_api_key,
    password="",
)


@datasets.command()
def register():
    # TODO: Introduce a SphinxBio wrapper around BaseModel.
    for cls in find_subclasses("sphinx", BaseModel):
        print("Registering dataset schema for", cls.__name__)
        client.register_dataset_schema(pydantic_model=cls)


if __name__ == "__main__":
    cli()
