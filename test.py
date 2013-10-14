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
# WARNING: "unique" doesn't has any correlation with database unique constraint, unique is used as csv record identifier (since primary key might not exists)
# if you have many "unique" field, AND logic will be used
table_structure_list = [
    {
        'table_name' : 'trans',
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
            'name'  : {'caption': 'Item Name'},
            'price' : {'caption': 'Price'}
        }
    },
    {
        'table_name' : 'trans_detail',
        'column_list': {
            'id'                : {'primary'  : True},
            'id_transaction'    : {'reference': 'trans.id', 'unique': True},
            'id_item'           : {'reference': 'item.id', 'unique': True},
            'qty'               : {'caption'  : 'Quantity'}
        }
    }
]

# define several preprocessing procedure (since human sucks...)
def change_date_format(human_date):
    ''' change 08/31/2000 into 2000-08-31
    '''
    date_part = human_date.split('/')
    if len(date_part) == 3:
        day = date_part[1]
        month = date_part[0]
        year = date_part[2]
        computer_date = year + '-' + month + '-' + day
    else:
        computer_date = ''
    return computer_date
def remove_dollar(value):
    ''' remove $, computer doesn't understand $
    '''
    return float(value.replace('$', ''))

# define callback to several fields
# the callbacks are used to preprocess the csv data
callback = {
    'Date' : change_date_format,
    'Price' : remove_dollar,
    'Quantity' : int
}

# and here is the magic:
csv2db(file_name, csv_param, connection_string, table_structure_list, callback)