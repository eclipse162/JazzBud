import os
from dotenv import load_dotenv

load_dotenv()

MY_ENV_VAR = os.getenv("test")

print(MY_ENV_VAR)