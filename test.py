from csv2db import csv2db

# connection string (used by sqlalchemy)
connection_string = 'sqlite:///test.db'

# the csv file name. If your worksheet is on "xls" format, please convert them into csv first (i.e: in MS Excel you can use File | Save As)
# the first line of the csv should be the header
file_name = 'test.csv'

# more info about csv_param: http://docs.python.org/2/library/csv.html#csv-fmt-params
csv_param = {
    'delimiter': ',', 
    'quotechar': '|'
}

# the table structure of your database and how they related to your csv file
table_structure = [
    {
        'table_name' : 'transaction',
        'column_list': {
            'id'    : {'primary': True},
            'code'  : {'caption': 'Transaction Code', 'unique': True},
            'date'  : {'caption': 'Date'}
        }
    },
    {
        'table_name' : 'item',
        'column_list': {
            'id'    : {'primary': True},
            'code'  : {'caption': 'Item Code', 'unique': True},
            'name'  : {'caption': 'Item Name'}
            'price' : {'caption': 'Price'}
        }
    },
    {
        'table_name' : 'transaction_detail',
        'column_list': {
            'id'                : {'primary'  : True},
            'id_transaction'    : {'reference': 'transaction.id'},
            'id_item'           : {'reference': 'item.id'},
            'qty'               : {'caption'  : 'Quantity'}
        }
    }
]

# and here is the magic:
csv2db(file_name, csv_param, connection_string, table_structure)