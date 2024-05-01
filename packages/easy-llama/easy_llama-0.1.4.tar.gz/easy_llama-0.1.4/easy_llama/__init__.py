# easy_llama.py
# https://github.com/ddh0/easy-llama/

"""Text generation in Python, made easy"""

__version__ = '0.1.4'

from . import formats
from . import samplers
from . import utils

from .model  import Model
from .thread import Thread


if __name__ == '__main__':
    raise RuntimeError(
        "easy_llama cannot be run directly, please import it into " + \
        "your environment"
    )
