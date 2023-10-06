import os 
import sys
sys.path.append(os.getcwd())

from src.utils.logger import logger
from datetime import datetime

class Base():
    def __init__(self) -> None:
        self.date_slash = datetime.now().strftime('%m/%d/%Y')
        self.date_dash = datetime.now().strftime('%Y-%m-%d')
        self.data_today = f'{self.date_slash}'
    
    def error_handler(self, message: str) -> dict:
        """
            This method is used to handle error in the class
        Args:
            message (str): The error message

        Returns:
            ```python
            {
                'status': 'error',
                'message': message,
                'data': None
            }
            ```
        """
        logger(message)
        return {
            'status': 'error',
            'message': message,
            'data': None
        }