import termcolor
from fico.figure import FigureCollection, FigureContainer
import pathlib
import matplotlib.pyplot as plt
import matplotlib.style
import itertools
import pathlib
import os
import traceback


class FigureBuilder:
    def __init__(
        self,
        draft_mode: bool = False,
        style: str | dict | pathlib.Path | list = None,
        build_dir: str | pathlib.Path = "build"
    ):
        """A builder that traverses the `FigureCollection`s and `Figure`s defined within a given `FigureContainer` and renders them to files in directories that reflect the structure of the container -> collection -> figure tree.

        The styling applied by the builder is in isolated context that doesn't leak into the surrounding environment.

        Args:
            draft_mode (bool, optional): if True, only builds figures marked with `only_build_this`. Defaults to False.
            style (str | dict | pathlib.Path | list, optional): styles used to build the figures in the isolated context of this builder, passed to `matplotlib.style.context`. Defaults to None.
            build_dir (str | pathlib.Path, optional): the root directory of the generated files. Defaults to `build`.
        """

        self.draft_mode: bool = draft_mode
        self._style = style
        self._build_dir = build_dir

    def should_only_build_some(self, container: FigureContainer) -> bool:
        """

        Args:
            container (FigureContainer): _description_

        Returns:
            bool: _description_
        """
        return self._any_has_only_build_this(container) and self.draft_mode
    
    def _any_has_only_build_this(self, container: FigureContainer):
        collections = container.collections
        figure_lists = [col.figures for col in collections]
        figures = itertools.chain(*figure_lists)

        return any([fig.only_build_this for fig in figures])
    
    @property 
    def style(self):
        return self._get_default_style_path() if self._style is None else self._style
    
    @style.setter
    def style(self, new_style):
        self._style = new_style


    def _get_default_style_path(self):
        # Setting stylesheet for all figures
        # TODO: Fix this hack to access the style file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        publication_style_path = os.path.join(
            current_dir, "styles/eit6_publication.mplstyle"
        )

        return publication_style_path

    def _get_figure_build_txt(self, figure):
        figure_txt = f"{figure}"

        if self.should_only_build_some(self._current_container) and not figure.only_build_this:
            figure_txt += termcolor.colored(" [SKIPPING]", "yellow")

        return figure_txt

    def _get_figure_out_path(
        self, collection_name: str, figure_name: str
    ) -> pathlib.Path:
        return pathlib.Path(
            self._build_dir, collection_name, figure_name
        )

    def _handle_build_error(self, collection, figure, error):
        print(
            termcolor.colored(
                f"Failed to build {collection}:{figure.name}. Error: {error}\n{traceback.format_exc()}",
                "red",
            )
        )

    def _build_collection(self, collection: FigureCollection) -> int:
        total_figure_count = len(collection)
        built_figure_count = 0

        print(
            f"Building {termcolor.colored(total_figure_count, 'green')} figures in {termcolor.colored(collection.name, 'green')}:"
        )

        for figure in collection.figures:
            print("\t" + self._get_figure_build_txt(figure))

            if self.should_only_build_some(self._current_container) and not figure.only_build_this:
                # If only some figures should be built but this isn't one of them, skip to next figure
                continue

            output_path = self._get_figure_out_path(collection.name, figure.name)
            output_path.parent.mkdir(exist_ok=True, parents=True)

            try:
                figure.build(output_path)
                built_figure_count += 1
            except Exception as e:
                self._handle_build_error(collection, figure, e)

        return built_figure_count

    def build(self, container: FigureContainer):
        """Builds the figures defined in a `FigureContainer`.

        Args:
            container (FigureContainer): the container to be built.
        """
        self._current_container = container
        with matplotlib.style.context(self.style, True):
            figure_count = 0

            for collection in container.collections:
                built_figures = self._build_collection(collection)
                figure_count += built_figures

            print(f"Built {figure_count} figures.")

_default_builder = FigureBuilder(draft_mode=False, style=None, build_dir="build")
