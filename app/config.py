import os

class Config:
    DATA_FILE = os.getenv("DATA_FILE", "data/servio_data.json")

config = Config()
