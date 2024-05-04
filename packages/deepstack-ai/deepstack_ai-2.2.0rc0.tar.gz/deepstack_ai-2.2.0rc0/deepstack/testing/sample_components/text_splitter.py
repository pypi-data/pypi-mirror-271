# SPDX-FileCopyrightText: 2022-present khulnasoft GmbH <info@khulnasoft.com>
#
# SPDX-License-Identifier: Apache-2.0
from typing import List

from deepstack.core.component import component


@component
class TextSplitter:
    @component.output_types(output=List[str])
    def run(self, sentence: str):
        """Takes a sentence in input and returns its words in output."""
        return {"output": sentence.split()}
