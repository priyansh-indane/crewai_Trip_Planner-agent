import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    body: str = Field(
        ..., 
        description="The complete trip plan output to be sent via email"
    )

class MyCustomTool(BaseTool):
    name: str = "email sender tool"
    description: str = (
        "Sends the final trip planning result via email to the receiver. "
        "Use this tool at the end to deliver the complete trip plan."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, body: str) -> str:
        sender = "lakesun552@gmail.com"
        receiver = "indanepriyansh@gmail.com"
        password = "xryiffmslizzdfom"

        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = "Your Trip Plan is Ready!"

        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender, password)
                server.sendmail(sender, receiver, msg.as_string())
            return "Email sent successfully with the trip plan!"
        except Exception as e:
            return f"Failed to send email: {str(e)}"