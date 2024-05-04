#
# This file is part of libdebug Python library (https://github.com/libdebug/libdebug).
# Copyright (c) 2023-2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from dataclasses import dataclass

from libdebug.data.register_holder import PtraceRegisterHolder
from libdebug.utils.register_utils import (
    get_reg_8h,
    get_reg_8l,
    get_reg_16,
    get_reg_32,
    get_reg_64,
    set_reg_8h,
    set_reg_8l,
    set_reg_16,
    set_reg_32,
    set_reg_64,
)

AMD64_GP_REGS = ["a", "b", "c", "d"]

AMD64_BASE_REGS = ["bp", "sp", "si", "di"]

AMD64_EXT_REGS = ["r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"]

AMD64_REGS = [
    "r15",
    "r14",
    "r13",
    "r12",
    "rbp",
    "rbx",
    "r11",
    "r10",
    "r9",
    "r8",
    "rax",
    "rcx",
    "rdx",
    "rsi",
    "rdi",
    "orig_rax",
    "rip",
    "cs",
    "eflags",
    "rsp",
    "ss",
    "fs_base",
    "gs_base",
    "ds",
    "es",
    "fs",
    "gs",
]


@dataclass
class Amd64PtraceRegisterHolder(PtraceRegisterHolder):
    """A class that provides views and setters for the registers of an x86_64 process, specifically for the `ptrace` debugging backend."""

    def apply_on(self, target, target_class):
        target.regs = self.register_file

        # If the accessors are already defined, we don't need to redefine them
        if hasattr(target_class, "instruction_pointer"):
            return

        def get_property_64(name):
            def getter(self):
                return get_reg_64(self.regs, name)

            def setter(self, value):
                set_reg_64(self.regs, name, value)

            return property(getter, setter, None, name)

        def get_property_32(name):
            def getter(self):
                return get_reg_32(self.regs, name)

            def setter(self, value):
                set_reg_32(self.regs, name, value)

            return property(getter, setter, None, name)

        def get_property_16(name):
            def getter(self):
                return get_reg_16(self.regs, name)

            def setter(self, value):
                set_reg_16(self.regs, name, value)

            return property(getter, setter, None, name)

        def get_property_8l(name):
            def getter(self):
                return get_reg_8l(self.regs, name)

            def setter(self, value):
                set_reg_8l(self.regs, name, value)

            return property(getter, setter, None, name)

        def get_property_8h(name):
            def getter(self):
                return get_reg_8h(self.regs, name)

            def setter(self, value):
                set_reg_8h(self.regs, name, value)

            return property(getter, setter, None, name)

        # setup accessors
        for name in AMD64_GP_REGS:
            name_64 = "r" + name + "x"
            name_32 = "e" + name + "x"
            name_16 = name + "x"
            name_8l = name + "l"
            name_8h = name + "h"

            setattr(target_class, name_64, get_property_64(name_64))
            setattr(target_class, name_32, get_property_32(name_64))
            setattr(target_class, name_16, get_property_16(name_64))
            setattr(target_class, name_8l, get_property_8l(name_64))
            setattr(target_class, name_8h, get_property_8h(name_64))

        for name in AMD64_BASE_REGS:
            name_64 = "r" + name
            name_32 = "e" + name
            name_16 = name
            name_8l = name + "l"

            setattr(target_class, name_64, get_property_64(name_64))
            setattr(target_class, name_32, get_property_32(name_64))
            setattr(target_class, name_16, get_property_16(name_64))
            setattr(target_class, name_8l, get_property_8l(name_64))

        for name in AMD64_EXT_REGS:
            name_64 = name
            name_32 = name + "d"
            name_16 = name + "w"
            name_8l = name + "b"

            setattr(target_class, name_64, get_property_64(name_64))
            setattr(target_class, name_32, get_property_32(name_64))
            setattr(target_class, name_16, get_property_16(name_64))
            setattr(target_class, name_8l, get_property_8l(name_64))

        # setup special registers
        setattr(target_class, "rip", get_property_64("rip"))

        # setup generic "instruction_pointer" property
        setattr(target_class, "instruction_pointer", get_property_64("rip"))

        # setup generic syscall properties
        setattr(target_class, "syscall_number", get_property_64("orig_rax"))
        setattr(target_class, "syscall_return", get_property_64("rax"))
        setattr(target_class, "syscall_arg0", get_property_64("rdi"))
        setattr(target_class, "syscall_arg1", get_property_64("rsi"))
        setattr(target_class, "syscall_arg2", get_property_64("rdx"))
        setattr(target_class, "syscall_arg3", get_property_64("r10"))
        setattr(target_class, "syscall_arg4", get_property_64("r8"))
        setattr(target_class, "syscall_arg5", get_property_64("r9"))
