#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2020 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import setuptools

def rename_sources(sources, base = ".c", target = ".cpp"):
    renamed = []
    for source in sources:
        source_extension = os.path.splitext(source)[1]
        if not source_extension == base: continue
        source_name = os.path.splitext(source)[0]
        new_source_path = source_name + target
        os.rename(source, new_source_path)
        renamed.append(new_source_path)
    return renamed

def rollback_sources(sources, base = ".cpp", target = ".c"):
    return rename_sources(sources, base = base, target = target)

module = setuptools.Extension(
    "npcolony",
    define_macros = [
        ("MAJOR_VERSION", "1"),
        ('MINOR_VERSION', '0')
    ],
    include_dirs = [
        ".",
        "src/colony_npapi/",
        "/usr/local/include"
    ],
    libraries = [
        "user32",
        "gdi32",
        "winspool",
        "comdlg32"
    ] if os.name in ("nt",) else ["cups"],
    library_dirs = ["/usr/local/lib"],
    extra_compile_args = [
        "/DHAVE_LIBPYTHON",
        "/DHAVE_LIBPYTHON_UNDEF"
    ] if os.name in ("nt",) else [
        "-std=c99",
        "-pedantic",
        "-finline-functions",
        "-Wall",
        "-Wno-long-long",
        "-Wno-variadic-macros",
        "-Wno-strict-aliasing",
        "-Wno-strict-prototypes",
        "-DNO_CONFIG_H",
        "-DCOLONY_PLATFORM_UNIX"
    ],
    sources = [
        "src/colony_npapi/stdafx.c",
        "src/colony_npapi/encoding/base_64.c",
        "src/colony_npapi/plugin/base.c",
        "src/colony_npapi/plugin/python.c",
        "src/colony_npapi/plugin/util.c",
        "src/colony_npapi/print/print_unix.c",
        "src/colony_npapi/print/print_win32.c",
        "src/colony_npapi/system/gui_unix.c",
        "src/colony_npapi/system/gui_win32.c"
    ]
)

if os.name in ("nt",):
    module.sources = rename_sources(module.sources)
try:
    setuptools.setup(
        name = "npcolony",
        version = "1.2.1",
        author = "Hive Solutions Lda.",
        author_email = "development@hive.pt",
        description = "Colony Framework",
        license = "Apache License, Version 2.0",
        keywords = "colony npapi native",
        url = "http://colony_npapi.hive.pt",
        packages = [
            "npcolony_py",
            "npcolony_py.test"
        ],
        test_suite = "npcolony_py.test",
        package_dir = {
            "" : os.path.normpath("src/python")
        },
        zip_safe = False,
        ext_modules = [module],
        classifiers = [
            "Development Status :: 5 - Production/Stable",
            "Topic :: Utilities",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.0",
            "Programming Language :: Python :: 3.1",
            "Programming Language :: Python :: 3.2",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12"
        ],
        long_description = open(os.path.join(os.path.dirname(__file__), "README.md"), "rb").read().decode("utf-8"),
        long_description_content_type = "text/markdown"
    )
finally:
    if os.name in ("nt",):
        rollback_sources(module.sources)
