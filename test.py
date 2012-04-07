from avient import *
from datetime import datetime
import re
import unittest


class AvientTest(unittest.TestCase):
    def setUp(self):
        self.response = retrievePage('757', '54051874')

    def testRetrievePage(self):
        self.assertEqual(self.response.status_code, 200)

    def testParseSchedule(self):
        schedule = parseSchedule(self.response.text)
        self.assertEqual(len(schedule), 8)
        self.assertEqual(schedule[1]['status'], 'Accepted')
        self.assertEqual(schedule[1]['station'], 'LGG')
        self.assertEqual(schedule[1]['date'], datetime(2011, 12, 5, 0, 0, 0))
        self.assertEqual(schedule[1]['desc'], 'Accepted at : LGG')
        self.assertEqual(schedule[1]['pcs'], 79)
        self.assertEqual(schedule[2]['pallets'], 'FLA90109SMJ')

    def testGenerateRss(self):
        schedule = parseSchedule(self.response.text)
        rss = generateRss(schedule)
        self.assertTrue(re.search(r'<rss version="2\.0">.*<\/rss>', rss))

if __name__ == '__main__':
    unittest.main()
