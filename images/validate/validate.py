import argparse
from time import sleep

import pandas as pd
from pandas_schema import Column, Schema
from pandas_schema.validation import LeadingWhitespaceValidation, TrailingWhitespaceValidation, \
    CanConvertValidation, MatchesPatternValidation, InRangeValidation, InListValidation

parser = argparse.ArgumentParser(description="A validation module")
parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()

with open(f'/work/{args.input}') as f:
    data = pd.read_json(f)

    schema = Schema([
        Column('userId', [CanConvertValidation(int)]),
        Column('id', [InRangeValidation(0, 75)]),  # a stupid validation, but will cause invalid rows...
        Column('title', [LeadingWhitespaceValidation(), TrailingWhitespaceValidation()]),
        Column('body', [LeadingWhitespaceValidation(), TrailingWhitespaceValidation()]),
    ])

    errors = schema.validate(data)

    with open(f'/work/{args.output}', 'w') as out:
        for error in errors:
            out.writelines(f'{error}\n')

        out.close()
