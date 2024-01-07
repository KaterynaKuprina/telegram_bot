from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


class MyCalendar:
    GOOGLE_CREDENTIALS_FILE = "refined-cortex-383811-222f72067798.json"
    SCOPES = ["https://www.googleapis.com/calendar/v3"]

    def __init__(self):
        credentials = Credentials.from_authorized_user_file(self.GOOGLE_CREDENTIALS_FILE, scopes=self.SCOPES)
        self.service = build("calendar", "v3", credentials=credentials)


obj = MyCalendar()