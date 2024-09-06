from dotenv import load_dotenv
import os
from database import *

load_dotenv()

id=os.getenv("ID")
print(f"adminID {id}")