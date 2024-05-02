# [Colony Gateway (NPAPI Plugin)](http://getcolony.com)

NPAPI-based plugin that provides a series of native features like:

* Printing using direct access to the printing infra-structure of the operative system
* Creation of native-based GUI elements

The current implementation supports only x86/x64 architectures and Windows, Linux, and Mac OS X.

## Building

To build both the CRX (Google Chrome) and the XPI (Mozilla Firefox) files for the plugin
one should use the scripts created for such effect under the [scripts](scripts) directory. The
automated process assumes the Windows build process using the Visual Studio IDE.

### Windows

Use Visual Studio 2008 Express for compilation with no additional dependencies. The build process should
create the plugin files in the output.

### Mac OS X

Download the [Gecko SDK 1.9 32 bit](https://developer.mozilla.org/en-US/docs/Gecko_SDK) from the official
website.

Use the `/Library/Internet Plug-Ins/` directory to test the plugin while the proper extension package file
is not created. Remember to rename the `*.bundle` package into an `*.plugin` based package.

### Linux

Use the `/usr/lib/mozilla/plugins/` directory to test the `*.so` based plugin file for development purposes.
[Mozilla Firefox](http://www.mozilla.org) should be the primary browser for the debugging of the NPAPI-based plugin.

### Python

It's also possible to build a Python module that exports the functionality in the NPAPI Plugin for
running the python script as `python setup.py install` under an UNIX-based machine.

## Packaging

### Google Chrome

Create a package file containing references to the complete set of plugin files for the various
platforms as defined in the `src/colony_npapi/descriptors/manifest_u.json` file.

```javascript
"plugins" : [{
    "path" : "npcolony.dll",
    "public" : true
}, {
    "path" : "libnpcolony.so",
    "public" : true
}, {
    "path" : "npcolony.plugin",
    "public" : true
}]
```

Copy the proper files (`npcolony.dll`, `libnpcolony.so` and `npcolony.plugin`) into the proper release directory
and then run the `make_all build` script to create the target files (eg: cbx and xpi).

```bash
make_all build <dir>
```

## Examples

There's an [examples directory](examples) containing HTML samples to test the plugin.

## License

Colony Gateway is currently licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).

## Build Automation

[![Build Status](https://app.travis-ci.com/hivesolutions/colony-npapi.svg?branch=master)](https://travis-ci.com/github/hivesolutions/colony-npapi)
[![Build Status GitHub](https://github.com/hivesolutions/colony-npapi/workflows/Main%20Workflow/badge.svg)](https://github.com/hivesolutions/colony-npapi/actions)
[![Coverage Status](https://coveralls.io/repos/hivesolutions/colony-npapi/badge.svg?branch=master)](https://coveralls.io/r/hivesolutions/colony-npapi?branch=master)
[![PyPi Status](https://img.shields.io/pypi/v/colony-npapi.svg)](https://pypi.python.org/pypi/appier)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/)
