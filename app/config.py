import os
from typing import cast


MOCKS_BASE_PATH: str = cast(str, os.getenv('MOCKS_BASE_PATH'))
