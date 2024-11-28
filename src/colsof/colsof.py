#!/usr/bin/env python3

import argparse
import openpyxl

parser = argparse.ArgumentParser(description='Prints the columns of an Excel sheet')
parser.add_argument('file', type=str, help='Excel file to read')
sheet_name_group = parser.add_mutually_exclusive_group(required=True)
sheet_name_group.add_argument('-i', '--sheet-name', type=str, help='Name or index of the sheet to read')
parser.add_argument('-w', '--skip-header', action='store_true', default=True, help='Skip the first row of the sheet')
parser.add_argument('-d', '--delimiter', type=str, default=' ', help='Delimiter to use between columns')
parser.add_argument('-t', '--trim', action='store_true', help='Trim whitespace from columns')
parser.add_argument('-c', '--columns', type=str, nargs='+', default=['0'], help='Column to read (either as index or letter)')
parser.add_argument('-f', '--default-value', type=str, default='<EMPTY>', help='Default value to use for empty cells')

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
    trim: bool = args.trim

    wb = openpyxl.load_workbook(file, read_only=True) #read_only speeds up reading significantly
    if sheet_name.isdigit():
        sheet_index = int(sheet_name)
        ws = wb.worksheets[sheet_index]
    else:
        ws = wb[sheet_name]

    converted_columns = [col_to_index(col) for col in args.columns]
    converted_columns.sort()
    iter = ws.iter_rows(min_row=2 if skip_header else 1, min_col=converted_columns[0], max_col=converted_columns[-1])

    allowed_columns = set(converted_columns)
    final_columns = set()

    #check the first row and check what columns are available
    values = []
    for row in iter:
        for cell in row:
            if cell.value is not None and cell.column in allowed_columns:
                final_columns.add(cell.column)
                if cell.value:
                    values.append(str(cell.value).strip() if trim else str(cell.value)) #need to print the first row
                else:
                    values.append(args.default_value)
        break #terminate after first row

    print(args.delimiter.join(values))
    for row in iter: #iterate over the rest of the rows
        values.clear()
        for cell in row:
            if cell.column in final_columns:
                if cell.value:
                    values.append(str(cell.value).strip() if trim else str(cell.value))
                else:
                    values.append(args.default_value)
        print(args.delimiter.join(values))


if __name__ == '__main__':
    main()
