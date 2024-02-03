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


# This function searches for emails with a specific subject and extracts the company name and date
def search_emails(service):
    print("Starting email search...")
    query = "subject: Robert, your application was sent to"
    nextPageToken = None
    all_messages = []

    while True:
        results = (
            service.users()
            .messages()
            .list(userId="me", q=query, pageToken=nextPageToken)
            .execute()
        )
        messages = results.get("messages", [])
        if not messages:
            print("No more messages found.")
            break
        all_messages.extend(messages)
        nextPageToken = results.get("nextPageToken")
        if not nextPageToken:
            break

    emails = []
    for msg in all_messages:
        msg_id = msg["id"]
        print(f"Fetching message {msg_id}...")
        message = service.users().messages().get(userId="me", id=msg_id).execute()

        headers = message["payload"]["headers"]
        subject = next(
            (header["value"] for header in headers if header["name"] == "Subject"), None
        )
        date = next(
            (header["value"] for header in headers if header["name"] == "Date"), None
        )

        if subject:
            company = subject.split("to ")[1].rsplit(" ", 1)[0]
            emails.append({"subject": subject, "company": company, "date": date})
            print(f"Found: {subject}")

    return emails


# This function will update the spreadsheet with the data we extracted from the emails
def update_spreadsheet(sheet_service, data):
    range_name = "Tracker!A10A"  # Adjust based on your needs
    value_input_option = (
        "RAW"  # 'RAW' if inputting raw data, 'USER_ENTERED' to mimic user input
    )

    values = [
        [
            email["date"],
            email["company"],
            "Applied",
            "Quick Apply",
            "",
            "",
            "LinkedIn",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        for email in data
    ]

    body = {"values": values}

    result = (
        sheet_service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption=value_input_option,
            body=body,
        )
        .execute()
    )

    print(f"{result.get('updatedCells')} cells updated.")


def main():
    gmail_service = get_gmail_service()
    emails = search_emails(gmail_service)

    # Load credentials from the file
    creds = get_credentials()

    # Set up Google Sheets service
    sheet_service = build("sheets", "v4", credentials=creds)

    spreadsheet_id = "1xM4KKFcfHkSjbg249DhmF-w2gT87VOIAmXz3yLHjW-M" # Replace with your spreadsheet ID

    # Update the spreadsheet with the data we extracted from the emails
    update_spreadsheet(sheet_service, spreadsheet_id, emails)

    print("Spreadsheet updated successfully")


if __name__ == "__main__":
    main()
