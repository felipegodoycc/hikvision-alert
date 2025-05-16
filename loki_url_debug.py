import os
from dotenv import load_dotenv

load_dotenv()
print(repr(os.getenv("LOKI_URL")))
