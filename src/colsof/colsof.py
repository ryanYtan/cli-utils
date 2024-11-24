#!/usr/bin/env python3

import argparse
import openpyxl

parser = argparse.ArgumentParser(description='Prints the columns of an Excel sheet')
parser.add_argument('file', type=str, help='Excel file to read')
sheet_name_group = parser.add_mutually_exclusive_group(required=True)
sheet_name_group.add_argument('-i', '--sheet-name', type=str, help='Name or index of the sheet to read')
parser.add_argument('-w', '--skip-header', action='store_true', default=True, help='Skip the first row of the sheet')
parser.add_argument('-n', '--ignore-empty', action='store_true', default=False, help='Ignore empty columns')
parser.add_argument('-t', '--trim', action='store_true', help='Trim whitespace from columns')
parser.add_argument('-c', '--column', type=str, default='0', help='Column to read (either as index or letter)')

def col_to_index(col: str) -> int:
    if col.isdigit():
        return int(col)
    col = col.upper()
    index = 0
    for c in col:
        index = index * 26 + (ord(c) - ord('A')) + 1
    return index

def main():
    args = parser.parse_args()
    file: str = args.file
    sheet_name: str = args.sheet_name
    skip_header: bool = args.skip_header
    ignore_empty: bool = args.ignore_empty
    trim: bool = args.trim

    wb = openpyxl.load_workbook(file, read_only=True)
    if sheet_name.isdigit():
        sheet_index = int(sheet_name)
        ws = wb.worksheets[sheet_index]
    else:
        ws = wb[sheet_name]

    col = col_to_index(args.column)
    for row in ws.iter_rows(min_row=2 if skip_header else 1, min_col=col, max_col=col):
        for cell in row:
            value = cell.value
            if ignore_empty and not value:
                continue
            print(value.strip() if trim else value)


if __name__ == '__main__':
    main()
