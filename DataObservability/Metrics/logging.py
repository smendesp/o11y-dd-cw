import logging


class Logging():

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding='utf-8', 
            level=logging.INFO)

        return 