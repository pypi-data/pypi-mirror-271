# SPDX-FileCopyrightText: 2022-present khulnasoft GmbH <info@khulnasoft.com>
#
# SPDX-License-Identifier: Apache-2.0
from typing import List

from deepstack.core.component import component


@component
class Repeat:
    def __init__(self, outputs: List[str]):
        self._outputs = outputs
        component.set_output_types(self, **{k: int for k in outputs})

    def run(self, value: int):
        """
        :param value: the value to repeat.
        """
        return {val: value for val in self._outputs}
