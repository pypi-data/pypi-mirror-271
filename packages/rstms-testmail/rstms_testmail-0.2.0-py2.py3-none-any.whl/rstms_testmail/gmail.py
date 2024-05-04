import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .watcher import PortWatcher

# If modifying these SCOPES, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


class Gmail:

    def __init__(self):
        with PortWatcher("ssh -q -N -R {}:localhost:{} beaker"):
            self.creds = self.authenticate_gmail_api()
            self.service = build("gmail", "v1", credentials=self.creds)

    def authenticate_gmail_api(self):
        """Shows basic usage of the Gmail API."""

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return creds

    def send(self, from_addr, to_addr, subject, message_text):
        """Create and send an email message."""
        service = self.service
        message = MIMEMultipart()
        message["to"] = to_addr
        message["from"] = from_addr
        message["subject"] = subject
        msg = MIMEText(message_text)
        message.attach(msg)

        # Encode the message in base64
        raw = base64.urlsafe_b64encode(message.as_bytes())
        raw = raw.decode()
        body = {"raw": raw}

        try:
            message = service.users().messages().send(userId="me", body=body).execute()
            print("Message Id: %s" % message["id"])
            return message
        except Exception as error:
            print(f"An error occurred: {error}")
