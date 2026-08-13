import unittest
from tests.test_analyzer import test_extract_urls, test_mask_sensitive, test_analyze_scam_message, test_analyze_safe_message

class TestScamShield(unittest.TestCase):
    def test_urls(self):
        test_extract_urls()

    def test_mask(self):
        test_mask_sensitive()

    def test_scam_msg(self):
        test_analyze_scam_message()

    def test_safe_msg(self):
        test_analyze_safe_message()

if __name__ == '__main__':
    unittest.main()
