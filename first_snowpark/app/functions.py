from __future__ import annotations

import sys

from common import print_hello


def hello_function(name: str) -> str:
    return print_hello(name)

def test_branch_condition() -> str:
    return "my_test_task3"


# For local debugging
# Be aware you may need to type-convert arguments if you add input parameters
if __name__ == "__main__":
    print(hello_function(*sys.argv[1:]))  # type: ignore
