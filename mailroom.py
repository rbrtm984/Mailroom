import os.path
import google.auth
from google.auth import load_credentials_from_file
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.credentials import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
]

def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds, _ = load_credentials_from_file("token.json")
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def get_gmail_service():
    creds = get_credentials()

    return build("gmail", "v1", credentials=creds)


def search_emails(service):
    print("Starting email search...")
    query = "subject: Robert, your application was sent to"
    results = service.users().messages().list(userId="me", q=query).execute()
    messages = results.get("messages", [])

    if not messages:
        print("No messages found.")
        return []

    emails = []
    for msg in messages:
        msg_id = msg["id"]
        print(f"Fetching message {msg_id}...")
        message = service.users().messages().get(userId="me", id=msg_id).execute()

        headers = message["payload"]["headers"]
        subject = next((header["value"] for header in headers if header["name"] == "Subject"), None)
        date = next((header["value"] for header in headers if header["name"] == "Date"), None)

        if subject:
            company = subject.split("to ")[1].split(" on ")[0]
            emails.append({"subject": subject, "company": company, "date": date})
            print(f"Found: {subject}")

    return emails

def update_spreadsheet(sheet_service, data):
    # This function will update the spreadsheet with the data we extracted from the emails
    pass


def main():
    gmail_service = get_gmail_service()
    emails = search_emails(gmail_service)

    # Load credentials from the file
    # creds = get_credentials()

    print("Emails fetched successfully:")
    for email in emails:
        print(email)
    # # Set up Google Sheets service
    # sheet_service = build("sheets", "v4", credentials=creds)

    # # Update the spreadsheet with the data we extracted from the emails
    # update_spreadsheet(sheet_service, emails)


if __name__ == "__main__":
    main()
