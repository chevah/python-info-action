from __future__ import print_function

import argparse
import os
import pip
import re
import sys


def parse_arguments(arguments):
    parser = argparse.ArgumentParser(
        description="Test the python-info-action output",
    )
    
    parser.add_argument(
        "--path",
        required=True,
        help="The path to the action's output file.",
    )

    parser.add_argument(
        "--package",
        required=False,
        nargs=2,
        action='append',
        default=[],
        help="Argument and version pair.  You can pass multiple times.",
    )

    return parser.parse_args(args=arguments)


def main(raw_arguments):
    arguments = parse_arguments(arguments=raw_arguments)
    with open(arguments.path) as f:
        output = f.read()

    relative_path = os.path.relpath(arguments.path, os.getcwd())

    assert re.search(
        "^'ACTION_FILE_PATH' +: '{}'$".format(re.escape(relative_path)),
        output,
        re.MULTILINE,
    )

    assert re.search(
        "^sys.prefix +: {}$".format(re.escape(sys.prefix)),
        output,
        re.MULTILINE,
    )

    arguments.package.append(("pip", pip.__version__))

    for name, version in arguments.package:
        print("checking for: {}, {}".format(name, version))
        assert re.search(
            "^{}=={}$".format(re.escape(name), re.escape(version)),
            output,
            re.MULTILINE,
        )


if __name__ == "__main__":
    sys.exit(main(raw_arguments=sys.argv[1:]))