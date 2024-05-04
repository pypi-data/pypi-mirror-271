import unittest
from pathlib import Path
import email
from email_utilities import EmailConversion


class EmailConversionTestCase(unittest.TestCase):

    def setUp(self):
        self.filepath = next(Path("Examples/email").iterdir())
        self.html_filepath = next(Path("Examples/html").iterdir())
        self.html_email_conversion = EmailConversion(filepath=self.html_filepath)
        self.email_conversion = EmailConversion(filepath=self.filepath)
        self.email_conversion_no_filepath = EmailConversion()

    def test_load_email(self) -> None:
        result = self.email_conversion.load_email()
        self.assertIsInstance(result, email.message.EmailMessage)

    def test__convert_html_to_plain_text(self) -> None:
        result = self.html_email_conversion._convert_html_to_plain_text()
        self.assertIsInstance(result, str)

    def test_convert_email_to_text(self) -> None:
        result = self.email_conversion.convert_email_to_text()
        self.assertIsInstance(result, email.message.EmailMessage)


if __name__ == '__main__':
    unittest.main()
