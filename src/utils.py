import logging


############## logging setup ###############
logging.basicConfig(level=logging.WARNING,
    format='%(asctime)s [%(module)s] %(levelname)s: %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
    ])

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
