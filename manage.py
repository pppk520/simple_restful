from app import create_app
import logging.config
import json

with open("config/logging.json", "r", encoding="utf-8") as fd:                         
    logging.config.dictConfig(json.load(fd))

app = create_app()


