# SPDX-FileCopyrightText: 2022-present khulnasoft GmbH <info@khulnasoft.com>
#
# SPDX-License-Identifier: Apache-2.0
from typing import List, Union

from deepstack.core.component import component


@component
class Concatenate:
    """
    Concatenates two values
    """

    @component.output_types(value=List[str])
    def run(self, first: Union[List[str], str], second: Union[List[str], str]):
        """
        Concatenates two values
        """
        if isinstance(first, str) and isinstance(second, str):
            res = [first, second]
        elif isinstance(first, list) and isinstance(second, list):
            res = first + second
        elif isinstance(first, list) and isinstance(second, str):
            res = first + [second]
        elif isinstance(first, str) and isinstance(second, list):
            res = [first] + second
        return {"value": res}
