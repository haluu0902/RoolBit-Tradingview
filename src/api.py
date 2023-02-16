from fastapi import FastAPI
from pydantic import BaseModel

#from fastapi.testclient import TestClient
from src.controller import ChromeController
import logging

logging.basicConfig(filename='log.log', format='[%(asctime)s] %(levelname)-8s :%(message)s')
logging.info(f"Start")

class OrderDetail(BaseModel):
    symbol: str
    side: str
    percent: float
    payout: float


chrome = ChromeController()
app = FastAPI()

@app.get("/")
def Home():
    return {
        "message": "Hello"
    }


@app.get("/neworder")
def NewOrder(item: OrderDetail):
    result = chrome.PlaceOrder(item.symbol, item.side, item.percent, item.payout)
    if result["result"]:
        logging.info(f"Place Order: {item.symbol} - {item.side} - {item.percent} - {item.payout} => Success!")
    else:
        logging.warning(f"Place Order: {item.symbol} - {item.side} - {item.percent} - {item.payout} => {result['message']} => Failed!")
    return result
