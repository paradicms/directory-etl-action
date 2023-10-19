#!/usr/bin/env python3
import dataclasses
from dataclasses import dataclass
from pathlib import Path

from paradicms_etl.etl_github_action import EtlGitHubAction
from paradicms_etl.extractors.directory_extractor import DirectoryExtractor
from paradicms_etl.transformers.directory_transformer import DirectoryTransformer


class Action(EtlGitHubAction):
    """
    Extract, transform, and load data from files in a directory.
    """

    @dataclass(frozen=True)
    class Inputs(EtlGitHubAction.Inputs):
        input_directory_path: str = dataclasses.field(
            default=".",
            metadata={
                "description": "Path to a directory of JSON, Markdown, YAML, and/or other files containing data to extract, transform, and load"
            },
        )

    def __init__(self, *, input_directory_path: str, **kwds):
        EtlGitHubAction.__init__(self, **kwds)
        self.__input_directory_path = Path(input_directory_path)

    def _run(self):
        self._run_pipeline(
            extractor=DirectoryExtractor(directory_path=self.__input_directory_path),
            transformer=DirectoryTransformer(pipeline_id=self._pipeline_id),
        )


if __name__ == "__main__":
    Action.main()
