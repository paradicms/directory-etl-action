#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

from paradicms_etl.extractors.markdown_directory_extractor import (
    MarkdownDirectoryExtractor,
)
from paradicms_etl.pipeline import Pipeline
from paradicms_etl.transformers.markdown_directory_transformer import (
    MarkdownDirectoryTransformer,
)
from paradicms_ssg.git_hub_action import GitHubAction


class Action(GitHubAction):
    @dataclass(frozen=True)
    class RequiredInputs(GitHubAction.RequiredInputs):
        markdown_directory_path: str

    @dataclass(frozen=True)
    class Inputs(GitHubAction.OptionalInputs, RequiredInputs):
        pass

    def __init__(self, *, inputs: Inputs, temp_dir_path: Path):
        GitHubAction.__init__(
            self,
            optional_inputs=inputs,
            required_inputs=inputs,
            temp_dir_path=temp_dir_path,
        )
        self.__inputs = inputs

    @classmethod
    def main(cls):
        with TemporaryDirectory() as temp_dir:
            cls(inputs=cls.Inputs.from_args(), temp_dir_path=Path(temp_dir)).__main()

    def __main(self):
        Pipeline(
            extractor=MarkdownDirectoryExtractor(
                markdown_directory_path=Path(self.__inputs.markdown_directory_path)
            ),
            id=self.__inputs.pipeline_id,
            loader=self._create_loader(),
            transformer=MarkdownDirectoryTransformer(
                pipeline_id=self.__inputs.pipeline_id
            ),
        ).extract_transform_load()


if __name__ == "__main__":
    Action.main()
