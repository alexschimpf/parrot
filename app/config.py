import os
from typing import cast


RULES_BASE_PATH: str = cast(str, os.getenv('RULES_BASE_PATH', '.boot'))
assert RULES_BASE_PATH
