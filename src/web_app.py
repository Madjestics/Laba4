import datetime

import fastapi

from src.model import CreateNote, Note, UpdateNote, GetNoteInfo, DeleteNote, GetNotesList, GetNoteText

api_router = fastapi.APIRouter()

listOfNotes = {}
index = 0

@api_router.post("/createNote", response_model=CreateNote)
def createNote(note_id: int):
    global listOfNotes, index
    note = Note(note_id)
    listOfNotes[index] = note.note_id
    index += 1
    return CreateNote(id=note.note_id)

@api_router.patch("/updateNote", response_model=UpdateNote)
def updateNote(note_id: int, text:str):
    global listOfNotes
    for note in listOfNotes:
        if note.note_id == note_id:
            note.update(text, datetime.datetime.now())
            break
    return UpdateNote(id = note.note_id, text = note.text)

@api_router.get("/getNoteInfo", response_model=GetNoteInfo)
def getNoteInfo(note_id: int):
    global listOfNotes
    for note in listOfNotes:
        if note.note_id == note_id:
            break
    return GetNoteInfo(created_at = note.created_time, updated_at = note.updated_time)

@api_router.delete("/removeNote", response_model=DeleteNote)
def removeNote(note_id : int):
    global listOfNotes
    for i in listOfNotes.keys():
        if listOfNotes[i] == note_id:
            deleted_note = listOfNotes[i]
            listOfNotes.pop(i)
            newList = {}
            for j in range(len(listOfNotes.keys())):
                if (j>=i):
                    newList[j] = listOfNotes[j+1]
                else:
                    newList[j] = listOfNotes[j]
            listOfNotes = newList
            break
    return DeleteNote(removed_id = deleted_note)

@api_router.get("/getNotesList", response_model=GetNotesList)
def getNotesList():
    return GetNotesList(notes_list = listOfNotes)

@api_router.get("/getNoteText", response_model=GetNoteText)
def getNoteText(id: int):
    global listOfNotes
    for note in listOfNotes:
        if note.note_id == id:
            right_note = note
            break
    return GetNoteText(id = note.note_id, text = note.text)