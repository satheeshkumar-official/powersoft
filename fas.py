from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)
def getdatab():
    conn = sqlite3.connect("powersoft.db")
    conn.row_factory = sqlite3.Row  
    return conn
def createtableindb():
    conn = getdatab()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS  userevent(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

createtableindb() 
class userev(BaseModel):
    title: str
    description: str = None
    date: str

# Create userev
@app.post("/userevent/")
def createevn(event: userev, db: sqlite3.Connection = Depends(getdatab)):
    cursor = db.cursor()
    cursor.execute("INSERT INTO events (title, description, date) VALUES (?, ?, ?)",
                   (event.title, event.description, event.date))
    db.commit()
    return {"message": "userevnt created successfully by sk"}
@app.get("/userevent/")
def getuser(db: sqlite3.Connection = Depends(getdatab)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    return [{"id": e["id"], "title": e["title"], "description": e["description"], "date": e["date"]} for e in events]
@app.put("/userevent/{event_id}")
def updateeven(event_id: int, event: userev, db: sqlite3.Connection = Depends(getdatab)):
    cursor = db.cursor()
    cursor.execute("UPDATE events SET title = ?, description = ?, date = ? WHERE id = ?",
                   (event.title, event.description, event.date, event_id))
    db.commit()
    return {"message": "userevnt updated successfully"}

# Delete userev
@app.delete("/userevent/{event_id}")
def delete(event_id: int, db: sqlite3.Connection = Depends(getdatab)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    db.commit()
    return {"message": "userevnt deleted successfully"}
