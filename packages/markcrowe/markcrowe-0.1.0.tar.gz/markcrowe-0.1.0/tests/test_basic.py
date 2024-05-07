"""Copyright (c) 2021 Mark Crowe <https://github.com/marcocrowe>. All rights reserved."""

import os
import sys
import unittest
from population_planning.project_manager import ProjectArtifactManager
from data_analytics.github import create_jupyter_notebook_header
from markcrowe.support import FileOpenModes

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_file_open_modes(self) -> None:
        """Test FileOpenModes"""
        expected: str = "wb"
        self.assertEqual(FileOpenModes.WRITE_BINARY, expected)

    def test_project_artifact_manager(self) -> None:
        """Test ProjectArtifactManager"""
        artifact_manager: ProjectArtifactManager = ProjectArtifactManager()
        expected: str = "./../artifacts/births-by-county-1985-2020-eda-output.csv"
        self.assertEqual(artifact_manager.get_county_births_eda_filepath(), expected)

    def test_create_jupyter_notebook_header(self) -> None:
        """Test create_jupyter_notebook_header"""
        self.maxDiff = None
        actual: str = create_jupyter_notebook_header(
            "markcrowe-com",
            "data-analytics-project-template",
            "notebooks/notebook-2-01-example-better-code-population-eda.ipynb",
        )
        expected: str = (
            f"""<!--{os.linesep}import data_analytics.github as github{os.linesep}print(github.create_jupyter_notebook_header("markcrowe-com", "data-analytics-project-template", "notebooks/notebook-2-01-example-better-code-population-eda.ipynb", "master")){os.linesep}-->{os.linesep}<table style="margin: auto;"><tr><td><a href="https://mybinder.org/v2/gh/markcrowe-com/data-analytics-project-template/master?filepath=notebooks/notebook-2-01-example-better-code-population-eda.ipynb" target="_parent"><img src="https://mybinder.org/badge_logo.svg" alt="Open In Binder"/></a></td><td>online editors</td><td><a href="https://colab.research.google.com/github/markcrowe-com/data-analytics-project-template/blob/master/notebooks/notebook-2-01-example-better-code-population-eda.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a></td></tr></table>"""
        )
        self.assertEqual(actual.strip(), expected.strip())


if __name__ == "__main__":
    unittest.main()
