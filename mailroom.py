import os.path
import google.auth
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/spreadsheets']

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = google.auth.load_credentials_from_file('token.json', SCOPES)[0]
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        
    return build('gmail', 'v1', credentials=creds)

def search_emails(service):
    # This query should match the job application confirmation email format 
    # for now, it will match LinkedIn emails, which always have the subject line:
    # "Robert, your application was sent to [Company Name]"
    query = "subject: Robert, your application was sent to"
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    emails = []
    for msg in messages: 
        msg_id = msd['id']
        message = service.users().messages().get(userId="me", id=msg_id).execute()

        # Extract the data we need from each message
        # This data, for now, will be the company name
        headers = message['payload']['headers']
        subject = next(header['value'] for header in headers if header['name'] == 'Subject')
        date = next(header['value'] for header in headers if header['name'] == 'Date')
        company = subject.split("to ")[1].split(" on ")[0]
        emails.append('subject': subject, 'company': company, 'date': date)
    
    return emails

def update_spreadsheet(sheet_service, data):
    # This function will update the spreadsheet with the data we extracted from the emails

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = google.auth.load_credentials_from_file('token.json', SCOPES)[0]
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

if __name__ == '__main__':
    main()
