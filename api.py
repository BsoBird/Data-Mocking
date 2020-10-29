from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from base.replaceFunc import *
import time

app = FastAPI()


class Item(BaseModel):
    content: str
    numb: int
    circular_reference_parse_max_times: int
    function_dic: dict = None


@app.get("/help")
def return_help_msg():
    return FileResponse("templates/help.html")


@app.post("/mockData/allsame")
async def update_item(item: Item):
    if item.numb > 10000:
        res = 'Not more than ten thousand at a time'
    else:
        try:
            res = run_same_data(replace_all_dic_ref_with_max_times(item.content,item.circular_reference_parse_max_times, item.function_dic), item.numb)
            return {"result": res, "num": item.numb, 'dateTime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
        except Exception as e:
            return e.args


@app.post("/mockData")
async def update_item(item: Item):
    if item.numb > 10000:
        res = 'Not more than ten thousand at a time'
    else:
        try:
            res = run(replace_all_dic_ref_with_max_times(item.content,item.circular_reference_parse_max_times,item.function_dic), item.numb)
            return {"result": res, "num": item.numb, 'dateTime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
        except Exception as e:
            return e.args


