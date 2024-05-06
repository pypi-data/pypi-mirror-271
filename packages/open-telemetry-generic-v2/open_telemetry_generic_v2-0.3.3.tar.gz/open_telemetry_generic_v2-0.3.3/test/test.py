import opentele 

from random import randint
from flask import Flask, request
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



@app.route("/rolldice")
@wrapper.wrapper_function
def roll():
    return randint(1, 6)
