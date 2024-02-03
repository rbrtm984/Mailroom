import unittest
from unittest.mock import Mock, patch

# from mailroom import (
#     update_spreadsheet,
#     search_emails,
#     get_gmail_service,
#     get_credentials,
# )


class TestMailroom(unittest.TestCase):

    def test_update_spreadsheet(self):
        # Setup
        mock_service = Mock()
        mock_data = [
            {"subject": "Test Subject", "company": "Big Conglomerate","date": "Test Date", "Snippet": "Test Snippet"}
        ]
        spreadsheet_id = "1xM4KKFcfHkSjbg249DhmF-w2gT87VOIAmXz3yLHjW-M"
        range_ = "Sheet1"

        # Exercise
        with patch.object(
            mock_service.spreadsheets().values(), "update", autoSpec=True
        ) as mock_update:
            from mailroom import update_spreadsheet

            update_spreadsheet(mock_service, mock_data)

        # Verify
        mock_update.assert_called_once_with(
            spreadsheetId=spreadsheet_id,
            range=range_,
            valueInputOption="RAW",
            body={"values": mock_data},
        )

    # def test_get_gmail_service(self):
    # Setup
    # input_data = "Some input"
    # expected_output = "Expected output"

    # Exercise
    # result = function_to_test(input_data)

    # Verify
    # self.assertEqual(result, expected_output)

    # Cleanup - not needed in this simple case but can be useful

    # def test_search_emails(self):
    # Setup
    # input_data = "Some input"
    # expected_output = "Expected output"

    # Exercise
    # result = function_to_test(input_data)

    # Verify
    # self.assertEqual(result, expected_output)

    # Cleanup - not needed in this simple case but can be useful


if __name__ == "__main__":
    unittest.main()
