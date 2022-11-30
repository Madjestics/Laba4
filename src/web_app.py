import datetime

import fastapi

from src.model import CreateNote, Note, UpdateNote, GetNoteInfo, DeleteNote, GetNotesList, GetNoteText

api_router = fastapi.APIRouter()

listOfNotes = []
listOfId = {}
index = 0

@api_router.post("/createNote", response_model=CreateNote)
def createNote(note_id: int, token:str):
    global listOfNotes, listOfId, index
    if (note_id not  in listOfId.values()):
        note = Note(note_id, datetime.datetime.now())
        listOfId[index] = note.note_id
        index += 1
        listOfNotes.append(note)
        return CreateNote(id=note.note_id)
    return CreateNote(id=-1)

@api_router.patch("/updateNote", response_model=UpdateNote)
def updateNote(note_id: int, text:str, token:str):
    global listOfNotes
    for note in listOfNotes:
        if note.note_id == note_id:
            note.update(text, datetime.datetime.now())
            return UpdateNote(id = note.note_id, text = note.text)
    return UpdateNote(id = -1, text = "id not found")

@api_router.get("/getNoteInfo", response_model=GetNoteInfo)
def getNoteInfo(note_id: int, token:str):
    global listOfNotes
    for note in listOfNotes:
        if note.note_id == note_id:
            return GetNoteInfo(created_at = note.created_time, updated_at = note.updated_time)
    return GetNoteInfo(created_at = 0, updated_at = 0)

@api_router.delete("/removeNote", response_model=DeleteNote)
def removeNote(note_id : int, token:str):
    global listOfNotes, index, listOfId
    for i in listOfId.keys():
        if listOfId[i] == note_id:
            deleted_note = listOfId[i]
            listOfId.pop(i)
            listOfNotes.pop(i)
            newList = {}
            for j in range(len(listOfId.keys())):
                if (j>=i):
                    newList[j] = listOfId[j+1]
                else:
                    newList[j] = listOfId[j]
            listOfId = newList
            index -= 1
            break
    return DeleteNote(removed_id = deleted_note)

@api_router.get("/getNotesList", response_model=GetNotesList)
def getNotesList(token:str):
    return GetNotesList(notes_list = listOfId)

@api_router.get("/getNoteText", response_model=GetNoteText)
def getNoteText(id: int, token:str):
    global listOfNotes
    for note in listOfNotes:
        if note.note_id == id:
            return GetNoteText(id = note.note_id, text = note.text)
    return GetNoteText(id=-1, text="id not found")