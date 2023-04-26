#!/usr/bin/env python3
import dataclasses
from dataclasses import dataclass
from pathlib import Path

from paradicms_etl.etl_github_action import EtlGitHubAction
from paradicms_etl.extractors.markdown_directory_extractor import (
    MarkdownDirectoryExtractor,
)
from paradicms_etl.pipeline import Pipeline
from paradicms_etl.transformers.markdown_directory_transformer import (
    MarkdownDirectoryTransformer,
)
from paradicms_ssg.models.root_model_classes_by_name import ROOT_MODEL_CLASSES_BY_NAME


class Action(EtlGitHubAction):
    """
    Extract, transform, and load data from a Paradicms Markdown directory.
    """

    @dataclass(frozen=True)
    class Inputs(EtlGitHubAction.Inputs):
        markdown_directory_path: str = dataclasses.field(
            default=".",
            metadata={"description": "Path to a directory of Markdown files"},
        )

    def __init__(self, *, markdown_directory_path: str, **kwds):
        EtlGitHubAction.__init__(self, **kwds)
        self.__markdown_directory_path = Path(markdown_directory_path)

    def _run(self):
        Pipeline(
            extractor=MarkdownDirectoryExtractor(
                markdown_directory_path=self.__markdown_directory_path
            ),
            id=self._pipeline_id,
            loader=self._loader,
            transformer=MarkdownDirectoryTransformer(
                pipeline_id=self._pipeline_id,
                root_model_classes_by_name=ROOT_MODEL_CLASSES_BY_NAME,
            ),
        ).extract_transform_load()


if __name__ == "__main__":
    Action.main()
