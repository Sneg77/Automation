from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle
import datetime #for reading present date
import time 
import requests #for retreiving coronavirus data from web
from plyer import notification #for getting notification on your PC

SCOPES = ['https://mail.google.com/']
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)


if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:


        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.j  son', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
service = build('gmail', 'v1', credentials=creds)


# Call the Gmail API

def get_counter():
    msg = False
    results = service.users().messages().list(userId='me', labelIds='INBOX', q='is:unread').execute()
    messages = results.get('messages', [])
    if messages:
        msg = True
    return msg

def get_author():
    results = service.users().messages().list(userId='me', labelIds='INBOX', q='is:unread').execute()
    messages = results.get('messages', [])
    mail_from = []
    message = messages[0]
    msg = service.users().messages().get(userId='me', id=message['id']).execute()
    email_data = msg['payload']['headers']
    for values in email_data:
        name = values['name']
        if name == "From":
            from_name = values['value']
            mail_from.append(from_name)
    return mail_from


def get_subject():
    results = service.users().messages().list(userId='me', labelIds='INBOX', q='is:unread').execute()
    messages = results.get('messages', [])
    mail_subject = []
    message = messages[0]
    msg = service.users().messages().get(userId='me', id=message['id']).execute()
    email_data = msg['payload']['headers']
    for values in email_data:
        name = values['name']
        if name == "Subject":
            subject = values['value']
            mail_subject.append(subject)
    return mail_subject


def get_text():
    results = service.users().messages().list(userId='me', labelIds='INBOX', q='is:unread').execute()
    messages = results.get('messages', [])
    mail_text = []
    message = messages[0]
    msg = service.users().messages().get(userId='me', id=message['id']).execute()
    email_data = msg['payload']['headers']
    for values in email_data:
        name = values['name']
        if name == "From":
            mail_text.append(msg['snippet'][:100])
    service.users().messages().modify(userId='me', id=message['id'],body={'removeLabelIds':['UNREAD']}).execute()
    return mail_text


def test():
    results = service.users().messages().list(userId='me', labelIds='INBOX', q='is:unread').execute()
    messages = results.get('messages', [])
    mail_text = []
    print(messages[0])
    message = messages[0]
    msg = service.users().messages().get(userId='me', id=message['id']).execute()
    email_data = msg['payload']['headers']
    for values in email_data:
        name = values['name']
        if name == "From":
            mail_text.append(msg['snippet'][:100])
def main():
    flag = True
    while(True):
        try:
            if flag:
                notification.notify(title = "NOTICE: Email notification active!")
                flag = False
            if get_counter():
                while get_counter():
                    notification.notify(
                        title = "New Message:",
                        app_name = "EmailNotification",
                        message = "От: {author}\nТема: {subject}\n{text}".format(
                                    author = get_author()[0],
                                    subject = get_subject()[0],
                                    text = get_text()[0]
                                    ),  
                        timeout  = 60
                    )
        except:
            notification.notify(title = "Error")
        time.sleep(1)
    main()

if __name__ == "__main__":
    main()
