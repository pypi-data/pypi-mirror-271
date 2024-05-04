import sys
from pathlib import Path
from typing import List

from nmk.model.builder import NmkTaskBuilder
from nmk.model.keys import NmkRootConfig
from nmk.utils import run_with_logs


class FlakeBuilder(NmkTaskBuilder):
    def build(self, src_folders: List[str]):
        # Project folder
        project_folder = Path(self.model.config[NmkRootConfig.PROJECT_DIR].value)

        # Work with relative folders if needed
        relative_src_folders = []
        for f in src_folders:
            p = Path(f)
            try:
                p = p.relative_to(project_folder)
            except ValueError:  # pragma: no cover
                pass
            relative_src_folders.append(p)

        # Delegate to flake8
        run_with_logs([sys.executable, "-m", "flake8"] + relative_src_folders, self.logger, cwd=project_folder)

        # Touch output file
        self.main_output.touch()
