from loguru import logger
from utils import OKX

if __name__ == '__main__':
    session = OKX()
    session.main()
    logger.succes("It's done!")