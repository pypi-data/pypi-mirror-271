#!/usr/bin/env python
import argparse
import os
import pathlib
import importlib
import importlib.util
from fico.figure import FigureContainer
from fico.building import _default_builder
import shutil
import sys
from termcolor import colored, cprint

DEFAULT_INDEX = "index:container"

# Allow imports from where the cli was invoked
invokation_path = pathlib.Path(os.curdir).resolve()
sys.path.append(str(invokation_path))

# Logging theme helper functions
underlined = lambda t: colored(t, attrs=["underline"])
red = lambda t: colored(t, "red")


def import_container(container_module_path: str) -> FigureContainer:
    module_name, container_name = container_module_path.split(":")

    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        error_msg = f"{red('Error')}: module {underlined(module_name)} not found in current directory."
        cprint(error_msg)
        sys.exit(1)

    try:
        container: FigureContainer = getattr(module, container_name)
    except AttributeError:
        error_msg = f"{red('Error')}: module {underlined(module_name)} does not define an attribute named {underlined(container_name)}."
        cprint(error_msg)
        sys.exit(1)

    if not isinstance(container, FigureContainer):
        error_msg = f"{red('Error')}: the attribute {module_name}.{container_name} is of type {type(container).__name__}, expected FigureContainer."
        cprint(error_msg)
        sys.exit(1)

    return container


def build_handler(args):
    main_container = import_container(args.container_path)

    print("Building figure collections")

    # Setting up builder, command line arguments take precedence over constructor arguments
    builder = main_container.builder if main_container.builder is not None else _default_builder
    builder.draft_mode = vars(args).get("draft", False)

    builder.build(main_container)


def clean_handler(args):
    print("Cleaning build directory.")

    if pathlib.Path("./build").is_dir():
        shutil.rmtree("./build")


def init_handler(args):
    raise NotImplementedError("Will be implemented in a future version.")


def main_cli():
    parser = argparse.ArgumentParser(prog="fico", description="Build tool for creating Matplotlib figures with sensible defaults that look native in LaTeX-documents.")

    # Defining subcommands
    subparsers = parser.add_subparsers(help="sub-command help", dest="cmd")

    parser_clean = subparsers.add_parser("clean", help="clean -h")
    parser_build = subparsers.add_parser("build", help="build -h")
    parser_init = subparsers.add_parser("init", help="init -h")

    # Adding options to subcommands
    parser_build.add_argument(
        "-d",
        "--draft",
        help="builds the figures in draft mode, results in faster rendering",
        action="store_true",
    )
    parser_build.add_argument(
        "-c",
        "--container",
        default=DEFAULT_INDEX,
        help="the path to the container to build, defaults to index:container",
        dest="container_path",
    )

    args = parser.parse_args()

    match args.cmd:
        case "clean":
            clean_handler(args)
        case "build":
            build_handler(args)
        case "init":
            init_handler(args)
        case _:
            parser.print_help()
            sys.exit(1)
