#!/usr/bin/env python3
import dataclasses
from dataclasses import dataclass
from pathlib import Path

from paradicms_etl.etl_github_action import EtlGitHubAction
from paradicms_etl.extractors.directory_extractor import (
    DirectoryExtractor,
)
from paradicms_etl.pipeline import Pipeline
from paradicms_etl.transformers.directory_transformer import (
    DirectoryTransformer,
)
from paradicms_ssg.models.root_model_classes_by_name import ROOT_MODEL_CLASSES_BY_NAME


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
        Pipeline(
            extractor=DirectoryExtractor(directory_path=self.__input_directory_path),
            id=self._pipeline_id,
            loader=self._loader,
            transformer=DirectoryTransformer(
                pipeline_id=self._pipeline_id,
                root_model_classes_by_name=ROOT_MODEL_CLASSES_BY_NAME,
            ),
        ).extract_transform_load()


if __name__ == "__main__":
    Action.main()
