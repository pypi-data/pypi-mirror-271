import unittest
from pathlib import Path
from email_utilities import EmailInsights
from email_utilities import EmailConversion


class EmailInsightsTestCase(unittest.TestCase):

    def setUp(self):
        self.filepath = next(Path("Examples/email").iterdir())
        self.dir = list(Path("Examples/email").iterdir()) + list(Path("Examples/html").iterdir())
        self.email_conversion = EmailConversion()
        self.email = self.email_conversion.load_email(self.filepath)
        self.emails = [self.email_conversion.load_email(file_) for file_ in self.dir]
        self.email_insights = EmailInsights()

    def test__get_email_structure(self):
        result = self.email_insights._get_email_structure(self.email)
        self.assertNotEqual(result, None)

    def test_count_email_structures(self):
        result = self.email_insights.count_email_structures(self.emails)
        self.assertGreaterEqual(len(result), 1)
