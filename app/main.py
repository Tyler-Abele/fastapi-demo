#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "admin"
DBPASS = os.getenv('DBPASS')
DB = "xxe9ff"

#comment so that I can re-run
@app.get("/genres")
async def get_genres():
    db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
    cur=db.cursor()
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[] 
        for result in results:
            json_data.append(dict(zip(headers,result)))
        cur.close()
        db.close()
        return(json_data)   
    except Error as e:
        cur.close()
        db.close()
        return {"Error": "MySQL error: " + str(e)}

@app.get('/songs')
async def get_songs():
    db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
    cur=db.cursor()
    query = "SELECT s.title, s.album, s.artist, s.year, s.file, s.image, s.genre FROM songs s INNER JOIN genres g ON s.genre = g.genreid;"
    try:
        cur.execute(query)
        results = cur.fetchall()
        songs_data = []
        for row in results:
            song = {
                "title" : row[0],
                "album" : row[1],
                "artist" : row[2],
                "year" : row[3],
                "file" : row[4],
                "image" : row[5],
                "genre" : row[6]
            }
            songs_data.append(song)
        cur.close()
        db.close()
        return{"songs" :songs_data}
    except Error as e:
        cur.close()
        db.close()
        return{"Error" :"MySQL error: " + str(e)}


@app.get("/")  # zone apex
def zone_apex():
    return {}

