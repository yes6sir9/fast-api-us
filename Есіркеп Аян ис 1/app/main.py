from fastapi import FastAPI
from sqlmodel import select
from app.models import Note
from app.schemas import NoteCreate, NoteOut
from app.database import engine, async_session, SQLModel

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@app.post("/notes", response_model=NoteOut)
async def create_note(note: NoteCreate):
    async with async_session() as session:
        new_note = Note(text=note.text)
        session.add(new_note)
        await session.commit()
        await session.refresh(new_note)
        return new_note

@app.get("/notes", response_model=list[NoteOut])
async def get_notes():
    async with async_session() as session:
        result = await session.execute(select(Note))
        notes = result.scalars().all()
        return notes
