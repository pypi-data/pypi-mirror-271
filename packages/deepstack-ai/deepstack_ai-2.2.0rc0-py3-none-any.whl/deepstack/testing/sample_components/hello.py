# SPDX-FileCopyrightText: 2022-present khulnasoft GmbH <info@khulnasoft.com>
#
# SPDX-License-Identifier: Apache-2.0
from deepstack.core.component import component


@component
class Hello:
    @component.output_types(output=str)
    def run(self, word: str):
        """Takes a string in input and returns "Hello, <string>!"in output."""
        return {"output": f"Hello, {word}!"}
