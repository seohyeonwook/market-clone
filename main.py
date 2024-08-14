from fastapi import FastAPI, UploadFile,Form,Response,Depends
# 1 - 서버 만들기
from fastapi.staticfiles import StaticFiles
# 2 - static만들기
from typing import Annotated
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
import sqlite3
# 3- sqlite3사용준비

con = sqlite3.connect("db.db",check_same_thread= False)
cur = con.cursor()
# 3

app = FastAPI()
# 1

SERCRET = "super-coding"
# setctet key
manager =LoginManager(SERCRET, "/login")
# access token만들어주는 라이브러리


@manager.user_loader()
def query_user(data):
    WHERE_STATEMENTS = f'id="{data}"'
    if type (data) == dict:
        WHERE_STATEMENTS = f'id="{data["id"]}"'
        
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute(f"""
                       SELECT * from users WHERE {WHERE_STATEMENTS}
                       """).fetchone()
    return user

@app.post("/login")
def login(id:Annotated[str,Form()], 
           password:Annotated[str,Form()]):
    user = query_user(id)
    if not user:
        raise InvalidCredentialsException
    elif password != user["password"]:
        raise InvalidCredentialsException
    
    access_token = manager.create_access_token(data={
    "sub": {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"]
    }
})
    # 토큰을 담아서 보내서 확인한다 = 신분증같은거??
    
    return {"access_token":access_token }
    

@app.post("/signup")
def signup(id:Annotated[str,Form()], 
           password:Annotated[str,Form()],
           name:Annotated[str,Form()],
           email:Annotated[str,Form()]):
    cur.execute(f"""
                INSERT INTO users(id,name,email,password)
                VALUES ("{id}","{name}","{email}","{password}")
                """)
    con.commit()
    return "200" 

@app.post("/items")
# 주소 items라는 경로로 보내게 되면 밑에 작업들이 이뤄질거다
async def create_item(image:UploadFile,
                title:Annotated[str,Form()],
                # form 데이터 형식으로(묶어서 보낸다) 문자열로 올거다 위에 무조건import 되어있어야함
                price:Annotated[int,Form()],
                description:Annotated[str,Form()],
                place:Annotated[str,Form()],
                insertAt:Annotated[int,Form()],
                user=Depends(manager)
                ):
    # 어떤값 받을거냐 : 형식 지정
    # print(image,title,price,description,place) - 확인용
    image_bytes = await image.read()
    cur.execute(f"""
                INSERT INTO 
                items(title,image,price,description,place,insertAt)
                VALUES ("{title}","{image_bytes.hex()}",{price},"{description}","{place}",{insertAt})
                """)
    # 숫자는 따움표 안들어간다 그래서 price는 따움표 없음
    con.commit()
    # 가져온 데이터를 테이블에 넣을거야
    return "200"

@app.get("/items")
async def get_items(user=Depends(manager)):
    con.row_factory = sqlite3.Row
    # 컬럼명 가져오는 문법 이거 없으면 컬럼 아이디 없이 그냥 리스트로 나온다
    cur = con.cursor()
    rows = cur.execute(f"""
                       SELECT * from items;
                       """).fetchall()
    return JSONResponse(jsonable_encoder(dict(row) for row in rows))
# docs에서 확인가능 확인용임 원래는 프론트엔드에서 보내주는것

@app.get("/images/{item_id}")
async def get_image(item_id):
    cur = con.cursor()
    image_bytes = cur.execute(f"""
                              SELECT image from items WHERE id={item_id}
                              """).fetchone()[0]
    
    return Response(content=bytes.fromhex(image_bytes))


app.mount("/",StaticFiles(directory = "frontend", html=True), name="frontend")
# 2 - 기본 형식 - 만들고 터미널 열고 uvicorn main:app --reload 해서 서버열기 
# crud는 mount 위에다 작성해야함
# server status code 구글검색해서 에러 코드들 한번 보자 400번대 클라이언트 500번대 서버문제
#  400 잘못된 요청 401 로그인이 틀렸을때 404 페이지 존재하지 않을때