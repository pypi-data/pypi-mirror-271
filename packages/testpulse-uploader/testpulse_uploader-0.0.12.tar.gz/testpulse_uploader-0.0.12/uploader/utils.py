
import argparse
import re
from typing import Optional, Pattern


def regex_pattern(regex: str) -> Optional[Pattern[str]]:
    if not regex:
        return None

    try:
        return re.compile(regex)
    except re.error:
        msg = f"String '{regex}' is not valid regex pattern"
        raise argparse.ArgumentTypeError(msg)
