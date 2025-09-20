import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
DEFAULT_TIMEOUT = float(os.getenv("REQ_TIMEOUT", "5.0"))  # segundos
