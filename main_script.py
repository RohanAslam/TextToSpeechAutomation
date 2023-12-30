import pyttsx3

import os

import ssl
import smtplib

import ssl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests 
from bs4 import BeautifulSoup
from datetime import datetime, timedelta 

from email.mime.multipart import MIMEMultipart

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

from Google import Create_Service
from googleapiclient.http import MediaFileUpload
import os

current_datetime = datetime.now()

threeDaysAgo = current_datetime - timedelta(days=3)

date = "2023-12-22"
#date = threeDaysAgo.strftime("%Y-%m-%d")



def uploadFile():
    print('uploading file')
    CLIENT_SECRET_FILE = '/Users/rohan/Desktop/MTAsummaryProject/client_secret_591443615889-tns61sr29csfa6d7rtd6f8itlspbf71g.apps.googleusercontent.com.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    # Create the Drive service
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    folder_id = '1lldnk7UafxYPGanL3nig-7GNXgsA017C'

    file_names = ['2023-12-22.mp3']
    mime_types = ['audio/mpeg']

    for file_name, mime_type in zip(file_names, mime_types):
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }

        media = MediaFileUpload('/Users/rohan/Desktop/MTAsummaryProject/files/{0}'.format(file_name), mimetype=mime_type)

        # Create the file with sharing settings
        created_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        # Modify sharing settings to make the file publicly accessible
        service.permissions().create(
            fileId=created_file['id'],
            body={
                'role': 'reader',  # Set the role to 'reader' to allow viewing
                'type': 'anyone'  # Set the type to 'anyone' to allow anyone with the link
            },
            fields='id'
        ).execute()

        print(f'File ID: {created_file["id"]} uploaded and made accessible to anyone with the link')


class TextToSpeech:
    engine: pyttsx3.Engine

    def __init__(self, voice, rate: int, volume:float):
        self.engine = pyttsx3.init()
        if voice:
            self.engine.setProperty('voice',voice)
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

    def list_available_voices(self):
        voices: list = [self.engine.getProperty('voices')]

        for i,voice in enumerate(voices[0]):
            print(f'{i + 1} {voice.name} {voice.age}: {voice.languages[0]} ({voice.gender}) [{voice.id}]')

    def text_to_speech(self, text: str, file_name: str, save: bool = False):
        print('text -> speech')

        if save:
            self.engine.save_to_file(text, file_name)

        self.engine.runAndWait()

        print('Finished')


def email(link):
    email_sender = 'MTA.reminder@gmail.com'
    email_password = "enon xbwz cgrs auae"

    email_reciever = 'rohanaslam24@gmail.com'

    subject = "Huzoor Khutba Summary"

    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_reciever
    msg['Subject'] = subject

    message = """اَلسَلامُ عَلَيْكُم وَرَحْمَةُ اَللهِ وَبَرَكاتُهُ
    \n
    Please use any of the attached links to access the most recent Friday Sermon delivered by Hazrat Khalifatul Masih:
    \n
    ENGLISH:
        Apple: https://podcasts.apple.com/us/podcast/english-friday-sermon-by-head/id464683963
        \n
        Spotify: https://open.spotify.com/show/5Ocmul6IzyXDc444S76ti5
        \n
        Google: https://podcasts.google.com/feed/aHR0cHM6Ly93d3cuYWxpc2xhbS5vcmcvZnJpZGF5LXNlcm1vbi9wb2RjYXN0cy9yc3MvZnJpZGF5LXNlcm1vbi1lbi5yc3M
        \n
    URDU:
        Apple: https://podcasts.apple.com/us/podcast/urdu-friday-sermon-by-head-of-ahmadiyya-muslim-community/id75352840?mt=2#
        \n
        Spotify: https://open.spotify.com/show/4lXH1XPIRtRmWBug7OkuoQ
        \n
        Google: https://podcasts.google.com/feed/aHR0cHM6Ly93d3cuYWxpc2xhbS5vcmcvZnJpZGF5LXNlcm1vbi9wb2RjYXN0cy9yc3MvZnJpZGF5LXNlcm1vbi11ci5yc3M
        \n
    Also see this Auto Generated summary in english:
    """ + link
    msg.attach(MIMEText(message, 'plain'))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_reciever, msg.as_string())
    
    print('email sent')
    

def summary():

    # link for extract html data 
    def getdata(url): 
        r = requests.get(url) 
        return r.text 
    
    htmldata = getdata("https://www.alislam.org/friday-sermon/2023-12-08.html") 
    soup = BeautifulSoup(htmldata, 'html.parser') 
    collect = '' 
    for data in soup.find_all("p"): 
        collect = collect + data.get_text()
    return collect


def getFileID():
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  print('Getting ID')

  SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "/Users/rohan/Desktop/MTAsummaryProject/client_secret_591443615889-tns61sr29csfa6d7rtd6f8itlspbf71g.apps.googleusercontent.com.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("drive", "v3", credentials=creds)

    # Call the Drive v3 API
    results = (
        service.files()
        .list(pageSize=10, fields="nextPageToken, files(id, name)")
        .execute()
    )
    items = results.get("files", [])

    if not items:
      print("No files found.")
      return
    for item in items:
      if item['name'] == '2023-12-22.mp3':
        return item['id']
      else:
        continue
  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")


def getLink(id):

    print('getting link')
    file_id = id

    credentials = service_account.Credentials.from_service_account_file(
        '/Users/rohan/Desktop/MTAsummaryProject/summaryemail-bf09d2b5433e.json', scopes=['https://www.googleapis.com/auth/drive']
    )

    # Build the Google Drive API service
    drive_service = build('drive', 'v3', credentials=credentials)

    # Fetch the file metadata
    file = drive_service.files().get(fileId=file_id, fields='webViewLink').execute()

    # Get the share link (webViewLink) for the file
    share_link = file.get('webViewLink')

    return share_link

if __name__ == '__main__':
    tts = TextToSpeech('com.apple.speech.synthesis.voice.daniel', 200, 1.0)

    tts.text_to_speech(summary(), 'files/2023-12-22.mp3', True )

    uploadFile()

    email(getLink(getFileID()))

    os.remove('files/'+ date +'.mp3')

