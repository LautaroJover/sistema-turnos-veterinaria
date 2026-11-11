import os
from urllib.parse import quote_plus
from databases import Database
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("DB_USER", "root")
raw_password = os.getenv("DB_PASSWORD", "")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "3306")
db_name = os.getenv("DB_NAME", "veterinaria_huellitas")

# Escapa caracteres como /, @ o : para que nunca falle el parser de puerto
encoded_password = quote_plus(raw_password)

DATABASE_URL = f"mysql+aiomysql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"

db = Database(DATABASE_URL)