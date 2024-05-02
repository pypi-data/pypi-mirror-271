# Copyright 2024 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

from __future__ import annotations

from functools import partial
from typing import Any

from qctrlworkflowclient import (
    core_workflow,
    print_warnings,
)
from qctrlworkflowclient.router.api import DecodedResult

from fireopal.config import get_config


def _formatter(input_: DecodedResult) -> Any:
    result = input_.decoded
    if isinstance(result, dict):
        return print_warnings(result)
    return result


fire_opal_workflow = partial(core_workflow, get_config, formatter=_formatter)
