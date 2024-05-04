# SPDX-FileCopyrightText: 2022-present khulnasoft GmbH <info@khulnasoft.com>
#
# SPDX-License-Identifier: Apache-2.0
from deepstack.core.component import component
from deepstack.core.component.types import Variadic


@component
class Sum:
    @component.output_types(total=int)
    def run(self, values: Variadic[int]):
        """
        :param value: the values to sum.
        """
        return {"total": sum(values)}
