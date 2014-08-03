# -*- coding: utf-8 -*-

from datetime import datetime


LENGTH = 0
FIELD = 1
TOKEN_SETS = {
    'ANTIQUES': {},
    'AUCTION': {},
    'BOOKS': {
        'AA': (128,   'Author'),
        'AC': (128,   'Compiler'),
        'AE': (128,   'Editor'),
        'AF': (128,   'Forward'),
        'AI': (28,    'Illustrator'),
        'AN': (64,    'Annotation'),
        'AP': (28,    'Photographer'),
        'AT': (128,   'Translator'),
        'BD': (14,    'Binding'),
        'BN': (13,    'ISBN Code'),
        'CI': (11,    'Catalog No'),
        'CN': (64,    'Condition'),
        'CO': (7,     'Copies'),
        'DP': (15,    'Date Published'),
        'DT': (24,    'System Date'),
        'ED': (14,    'Edition'),
        'FP': (256,   'Fixed Shipping'),
        'FU': (10,    'Monetary Units'),
        'FX': (64,    'Sales Tax'),
        'FY': (10,    'Fixed Handling Fee'),
        'IM': (256,   'Image'),
        'IS': (15,    'Status'),
        'JK': (14,    'Jacket'),
        'KE': (19,    'Keyword'),
        'KW': (19,    'Keyword'),
        'LG': (10,    'Language'),
        'LO': (15,    'Location'),
        'MT': (27,    'Main Topic'),
        'MV': (10,    'Market Value'),
        'NC': (128,   'Comments'),
        'NT': (16384, 'Notes'),
        'PC': (10,    'Purchase Cost'),
        'PG': (14,    'Pages'),
        'PP': (27,    'Place Pub'),
        'PR': (10,    'Price'),
        'PT': (14,    'Printing'),
        'PU': (28,    'Publisher'),
        'RE': (15,    'Record No'),
        'SD': (24,    'System Date'),
        'SE': (128,   'Series'),
        'TI': (128,   'Title'),
        'TP': (15,    'Size/Type'),
        'UR': (15,    'Record No'),
        'WT': (16,    'Weight'),
    },
    'RETAIL': {},
    'CUSTOM': {},
    'LISTING': {
        'XA': 'Life Span',
        'XB': [],
        'XC': {
            'BO': 'Books General',
            'AU': 'Autographs',
            'EB': 'Electronic Book',
            'EP': 'Ephemera',
            'FC': 'Facsimiles',
            'LE': 'Letters',
            'MS': 'Manuscripts',
            'MP': 'Maps',
            'MT': 'Miniatures',
            'PA': 'Pamphlets',
            'PH': 'Photographs',
            'PO': 'Posters',
            'SI': 'Serial Issues',
            'SR': 'Serial Runs',
            'SV': 'Serial Volumes',
            'TC': 'Trade Catalogs',
            'UN': 'Undefined',
        },
        'XD': {
            'S': 'For-Sale',
            'W': 'Wants',
            'T': 'For-Trade',
            'M': 'Remainders',
            'R': 'Realizations',
        },
    },
}


class UIEE(object):

    @classmethod
    def parse(cls, fp):
        uiee_file = UIEE()
        uiee_file.parse_header(fp)
        uiee_file.records = list(uiee_file.parse_records(fp))
        return uiee_file

    def parse_header(self, fp):
        self.user_id = fp.readline().strip()
        self.token_set = fp.readline().strip()
        date = fp.readline().strip()
        time = fp.readline().strip()
        self.timestamp = datetime.strptime(date + time, '%m-%d-%Y%H:%M:%S')

    def parse_records(self, fp):
        record, last_token = {}, None
        for line in iter(fp.readline, ''):
            if not line.strip():
                if record:
                    yield record
                record = {}
            else:
                line = line.strip()
                token, value = line[:2], line[3:]
                if TOKEN_SETS['BOOKS'].get(
                    token,
                    TOKEN_SETS['LISTING'].get(token, None)
                ) is None:
                    raise ValueError('Undefined Token')
                if token == last_token:
                    value = record[token] + ' ' + value
                last_token = token
                record[token] = value
        yield record
