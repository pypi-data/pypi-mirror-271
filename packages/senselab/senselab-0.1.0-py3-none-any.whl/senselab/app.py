"""This script defines a simple function that prints 'Hello World!' to the console.

It then calls this function if the script is run as the main program.
"""

from typing import Any, Dict

from senselab.utils.decorators import get_response_time


@get_response_time
def hello_world() -> Dict[str, Any]:
    """Prints hello world."""
    return {"output": "Hello World!"}

if __name__ == "__main__":
    a = hello_world()
    print(a)