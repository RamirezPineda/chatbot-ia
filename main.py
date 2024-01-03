from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import smtplib
from email.mime.text import MIMEText

from pydantic import BaseModel

from chat import chat

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/chat")
def chatbot(message: Message):
    response = chat(message.message)
    return {"response": response}


class EmailData(BaseModel):
    name: str
    email: str
    subject: str
    message: str

@app.post("/send-email")
async def send_email(email_data: EmailData):

    sender = "Private Person <" + email_data.email + ">"
    receiver = "User <ramirez.ricky2021@example.com>"

    message = MIMEText(email_data.message)
    message["Subject"] = email_data.subject
    message["From"] = sender
    message["To"] = receiver

    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        server.login("d95dba990663a3", "bf8de2d3da745a")
        server.sendmail(sender, receiver, message.as_string())

    return {"message": "Email sent successfully"}
