from fastapi import FastAPI, UploadFile,Form
# 1 - 서버 만들기
from fastapi.staticfiles import StaticFiles
# 2 - static만들기
from typing import Annotated

import sqlite3
# 3- sqlite3사용준비
con = sqlite3.connect("db.db",check_same_thread= False)
cur = con.cursor()
# 3

app = FastAPI()
# 1

@app.post("/items")
# 주소 items라는 경로로 보내게 되면 밑에 작업들이 이뤄질거다
async def create_item(image:UploadFile,
                title:Annotated[str,Form()],
                # form 데이터 형식으로(묶어서 보낸다) 문자열로 올거다 위에 무조건import 되어있어야함
                price:Annotated[int,Form()],
                description:Annotated[str,Form()],
                place:Annotated[str,Form()]
                ):
    # 어떤값 받을거냐 : 형식 지정
    # print(image,title,price,description,place) - 확인용
    image_bytes = await image.read()
    cur.execute(f"""
                INSERT INTO items(title,image,price,description,place)
                VALUES ("{title}","{image_bytes.hex()}",{price},"{description}","{place}")
                """)
    # 숫자는 따움표 안들어간다 그래서 price는 따움표 없음
    con.commit()
    # 가져온 데이터를 테이블에 넣을거야
    return "200"
# docs에서 확인가능 확인용임 원래는 프론트엔드에서 보내주는것

app.mount("/",StaticFiles(directory = "frontend", html=True), name="frontend")
# 2 - 기본 형식 - 만들고 터미널 열고 uvicorn main:app --reload 해서 서버열기 
# crud는 mount 위에다 작성해야함