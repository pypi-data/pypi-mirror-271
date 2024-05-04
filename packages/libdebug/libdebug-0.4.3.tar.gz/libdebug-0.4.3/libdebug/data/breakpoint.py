#
# This file is part of libdebug Python library (https://github.com/libdebug/libdebug).
# Copyright (c) 2023-2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from libdebug.state.thread_context import ThreadContext


@dataclass
class Breakpoint:
    """A breakpoint in the target process.

    Attributes:
        address (int): The address of the breakpoint in the target process.
        symbol (str): The symbol, if available, of the breakpoint in the target process.
        hit_count (int): The number of times this specific breakpoint has been hit.
        hardware (bool): Whether the breakpoint is a hardware breakpoint or not.
        condition (str): The breakpoint condition. Available values are "X", "W", "RW". Supported only for hardware breakpoints.
        length (int): The length of the breakpoint area. Supported only for hardware breakpoints.
        enabled (bool): Whether the breakpoint is enabled or not.
    """

    address: int = 0
    symbol: str = ""
    hit_count: int = 0
    hardware: bool = False
    callback: None | Callable[["ThreadContext", Breakpoint], None] = None
    condition: str = "x"
    length: int = 1
    enabled: bool = True

    _linked_thread_ids: list[int] = field(default_factory=list)
    # The thread ID that hit the breakpoint

    _disabled_for_step: bool = False
    _changed: bool = False

    def enable(self) -> None:
        """Enable the breakpoint."""
        from libdebug.state.debugging_context import provide_context

        if provide_context(self).running:
            raise RuntimeError(
                "Cannot enable a breakpoint while the target process is running."
            )

        self.enabled = True
        self._changed = True

    def disable(self) -> None:
        """Disable the breakpoint."""
        from libdebug.state.debugging_context import provide_context

        if provide_context(self).running:
            raise RuntimeError(
                "Cannot disable a breakpoint while the target process is running."
            )

        self.enabled = False
        self._changed = True

    def hit_on(self, thread_context: "ThreadContext") -> bool:
        """Returns whether the breakpoint has been hit on the given thread context."""
        return self.enabled and thread_context.instruction_pointer == self.address

    def __hash__(self) -> int:
        return hash(self.address)
