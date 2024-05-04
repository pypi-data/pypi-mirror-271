import sys

from nmk.model.builder import NmkTaskBuilder
from nmk.model.keys import NmkRootConfig
from nmk.model.resolver import NmkStrConfigResolver
from nmk.utils import is_windows, run_with_logs
from nmk_base.venvbuilder import VenvUpdateBuilder


class PackageBuilder(NmkTaskBuilder):
    def build(self, artifacts: str, build_dir: str):
        # Delegate to setup
        run_with_logs(
            [sys.executable, "-c", "from setuptools import setup; setup()", "build", "-b", build_dir, "bdist_wheel", "-d", artifacts],
            self.logger,
            cwd=self.model.config[NmkRootConfig.PROJECT_DIR].value,
        )


class PythonPackageForWheel(NmkStrConfigResolver):
    def get_value(self, name: str) -> str:
        return self.model.config["pythonPackage"].value.replace("-", "_")


class Installer(VenvUpdateBuilder):
    def build(self, name: str, pip_args: str):
        # On Windows, refuse to install nmk package while running nmk (wont' work)
        if is_windows() and name == "nmk":
            self.logger.warning("Can't install nmk while running nmk!")
        else:
            super().build(pip_args)
