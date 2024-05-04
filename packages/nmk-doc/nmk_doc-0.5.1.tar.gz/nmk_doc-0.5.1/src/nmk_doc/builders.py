"""
Python module for **nmk-doc** plugin builders.
"""

from nmk.model.builder import NmkTaskBuilder
from nmk.utils import run_with_logs


class NmkDocSphinxBuilder(NmkTaskBuilder):
    """
    Builder used to trigger **sphinx** documentation build
    """

    def build(self, source_folder: str, output_folder: str):
        """
        Called by the **doc.build** task, to build the **sphinx** documentation

        :param source_folder: doc source folder
        :param output_folder: doc output folder
        """

        # Invoke sphinx
        run_with_logs(["sphinx-build", source_folder, output_folder])

        # Touch main output index (for incremental build)
        self.main_output.touch()
