# -*- coding: utf-8 -*-

import unittest

from datetime import datetime

from uiee import UIEE


class TestUIEE(unittest.TestCase):
    def setUp(self):
        self.uiee_file = UIEE.parse(open('./tests/fixtures/simple_record.txt'))

    def test_userid(self):
        assert self.uiee_file.user_id == 'MYUSERID'

    def test_token_set(self):
        assert self.uiee_file.token_set == 'BOOKS'

    def test_timestamp(self):
        assert self.uiee_file.timestamp == datetime(2002, 01, 01, 12, 34, 56)

    def test_records_length(self):
        assert len(self.uiee_file.records) == 2

    def test_record_author(self):
        assert self.uiee_file.records[0]['AA'] == 'Bester, Alfred'

    def test_record_date_published(self):
        assert self.uiee_file.records[1]['DP'] == '1956'

    def test_concatenation(self):
        comment = ('Book and dust jacket very good. '
                   'Small spots on back cover. '
                   'Dust jacket has some edge wear and slight rubbing. '
                   '183 pages.')
        assert self.uiee_file.records[0]['NC'] == comment
