"""
Generate dataset pydantic models from API schema
"""
from typing import Iterable, List

import jinja2
from rich.console import Console

from nyc_open_data.client import datasets
from nyc_open_data.dataset import Dataset


def render(datasets: List[Dataset]) -> Iterable[str]:
    loader = jinja2.FileSystemLoader("./codegen/")
    env = jinja2.Environment(loader=loader, autoescape=False)
    template_file = "dataset_model.py.jinja"
    template = env.get_template(template_file)
    yield from template.generate(datasets=datasets)


def main():
    """
    Generate dataset pydantic models from API schema
    """
    limit = None
    console = Console(stderr=True)
    with console.status("Fetching available datasets...") as status:
        data = datasets()
        status.update("Rendering templates...")
        # console.print(data[:limit])
        with open("nyc_open_data/models.py", "w") as f:
            for chunk in render(data[:limit]):
                print(chunk, sep="", end="", file=f)


if __name__ == "__main__":
    main()
