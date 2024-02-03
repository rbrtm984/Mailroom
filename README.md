README: Mailroom

This Python script interacts with the Gmail and Google Sheets APIs in order to process data from emails.

It automates the tedious work of tracking data from LinkedIn job application confirmations on a Google Sheet. 

It can also run automatically, auto-updating the spreadsheet whenever a new email confirmation comes in (WIP)

Functionality:
    - Sorts emails based on specified criteria (confirmation, resume review, profile view, rejection)
    - Processes data from job applications and provides insights (type of application to success ratio, rate of rejection, rate of success)

Features:
    - Connect to Gmail API programatically
    - Search Inbox using query that matches LinkedIn confirmation email format
    - Save pertinent data in a structure that can be used to update a pre-built Google Sheet
        - Project built/tested using example job hunt tracker created by Patrick Reid
    - Unit Testing coverage (WIP)