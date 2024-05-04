# SPDX-FileCopyrightText: 2022-present khulnasoft GmbH <info@khulnasoft.com>
#
# SPDX-License-Identifier: Apache-2.0
from deepstack.core.component import component


@component
class Subtract:
    """
    Compute the difference between two values.
    """

    @component.output_types(difference=int)
    def run(self, first_value: int, second_value: int):
        """
        Run the component.

        :param first_value: name of the connection carrying the value to subtract from.
        :param second_value: name of the connection carrying the value to subtract.
        """
        return {"difference": first_value - second_value}
