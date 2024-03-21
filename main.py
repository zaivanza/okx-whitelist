import sys
from traceback import format_exc
from loguru import logger
from utils import OKX


if __name__ == '__main__':
    try:
        session = OKX()
        session.main()
        logger.success("It's done!")
    except Exception as e:
        sys.exit(f"Unexpected error: {e}\n\n"
                 f"Open the issue at https://github.com/zaivanza/okx-whitelist/issues with traceback {format_exc()}")
