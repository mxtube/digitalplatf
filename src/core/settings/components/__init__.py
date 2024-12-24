import os
import environ
from pathlib import Path


# Build paths inside the project like this: BASE_DIR.joinpath('some')
# `pathlib` is better than writing: dirname(dirname(dirname(__file__)))
BASE_DIR = Path(__file__).parent.parent.parent.parent

# Loading `.env` files
env = environ.Env()
environ.Env.read_env(
    os.path.join(BASE_DIR, '../.env')
)
