from csv2db import csv2db

table_list = [
    {
        'name' : 'transaction',
        'column_dict': {
            'transaction_code' : 'Transaction code',
            'date' : 'Date'
        },
        'unique_column_list': ['transaction_code'],
        'primary_column' : 'transaction_code',
        'parent_table_list' : [],
        'foreign_key_list' : []
    },
    {
        'name' : 'item',
        'column_dict': {
            'item_code' : 'Item code',
            'price' : 'Price'
        },
        'unique_column_list': ['item_code'],
        'primary_column' : 'item_code',
        'parent_table_list' : [],
        'foreign_key_list' : []
    }
]