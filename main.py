from typing import Union

from fastapi import FastAPI

import  enmax

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/getanswers")
def getanswers(questions: Union[str, None] = None):
    results = enmax.get_answer(questions)
    return results