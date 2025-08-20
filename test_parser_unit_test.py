# test_parser.py
import unittest
from datetime import datetime
from parser import parse_log_line


class TestLogParser(unittest.TestCase):

    def test_valid_log_line(self):
        line = "2025-06-18 10:25:13,212 INFO  user_id=123 action=login status=success"
        result = parse_log_line(line)
        self.assertIsNotNone(result)
        self.assertEqual(result['level'], 'INFO')
        self.assertEqual(result['user_id'], '123')
        self.assertEqual(result['action'], 'login')
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['timestamp'], datetime(2025, 6, 18, 10, 25, 13, 212000))

    def test_invalid_log_line_format(self):
        line = "Invalid log entry format"
        result = parse_log_line(line)
        self.assertIsNone(result)

    def test_missing_fields(self):
        line = "2025-06-18 10:25:13,212 INFO user_id=123 status=success"
        result = parse_log_line(line)
        self.assertIsNone(result)

    def test_different_level(self):
        line = "2025-06-18 11:00:00,000 ERROR user_id=101 action=logout status=failed"
        result = parse_log_line(line)
        self.assertIsNotNone(result)
        self.assertEqual(result['level'], 'ERROR')
        self.assertEqual(result['status'], 'failed')


if __name__ == '__main__':
    unittest.main()
