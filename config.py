import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

BASE_URL = "https://www.smu.edu.in/smit"

CHROMA_PATH = "./vectorstore/chroma_db"

COLLECTION_NAME = "smit_knowledge_base"