# ignore this function, it is just used to generate test database
def make_db(connection_string):
    from sqlalchemy import Column, Integer, String, text, ForeignKey, Table, ForeignKeyConstraint, create_engine
    from sqlalchemy.orm import relationship, backref, scoped_session, sessionmaker
    from sqlalchemy.ext.declarative import declarative_base

    # create Base
    Base = declarative_base()

    class Transaction(Base):
        __tablename__ = 'trans'
        id = Column(Integer, primary_key=True)
        code = Column(String(10))
        date = Column(String(12))

    class Item(Base):
        __tablename__ = 'item'
        id = Column(Integer, primary_key=True)
        code = Column(String(10))
        name = Column(String(20))
        price = Column(Integer)
        unit = Column(String(10))

    class Transaction_Detail(Base):
        __tablename__ = 'trans_detail'
        id = Column(Integer, primary_key=True)
        qty = Column(Integer)
        id_transaction = Column(Integer, ForeignKey('trans.id'))
        id_item = Column(Integer, ForeignKey('item.id'))

    # create engine
    engine = create_engine(connection_string, echo=True)

    # create db session
    db_session = scoped_session(sessionmaker(bind=engine))
    Base.metadata.create_all(bind=engine)
    db_session.commit()

########################################################################

from csv2db import csv2db

# connection string (used by sqlalchemy)
connection_string = 'sqlite:///test.db'
# MySQL connection_string example. Beware of the charset
# connection_string = 'mysql://root:toor@localhost:3306/test?charset=utf8'

# create database if not exists (this is just for test case, you won't need this for real case)
make_db(connection_string)


# the csv file name. If your worksheet is on "xls" format, please convert them into csv first (i.e: in MS Excel you can use File | Save As)
# the first line of the csv should be the header
file_name = 'test.csv'

# more info about csv_param: http://docs.python.org/2/library/csv.html#csv-fmt-params
csv_param = {
    'delimiter': ',',   # libre office usually use "," while microsoft office usually use "tab"
    'quotechar': '"'    # both, libre office and microsoft office usually use '"'
}

########################################################################

# define several preprocessing callbacks. These callbacks will be used to preprocess every cell based on it's column

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

# callback dictionary. The key is caption of the column, the value is the function used
callback = {
    'Date' : change_date_format,
    'Price' : remove_dollar
}

########################################################################

# specific preprocess function (in case of 2 different fields refer to the same csv column)

def filter_qty(value):
    ''' get "1" as int from "1 bottle" string
    '''
    return int(value.split(' ')[0])

def filter_unit(value):
    ''' get "bottle" from "1 bottle"
    '''
    return ' '.join(value.split(' ')[1:])

########################################################################

# the table structure of your database and how they related to your csv file
# WARNING: "unique" doesn't has any correlation with database unique constraint, unique is used as csv record identifier (since primary key does not exists in csv)
# if you have many "unique" field, AND logic will be used to distinguish a field from another field
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
            'price' : {'caption': 'Price'},
            'unit'  : {'caption': 'Quantity', 'preprocess' : filter_unit}
        }
    },
    {
        'table_name' : 'trans_detail',
        'column_list': {
            'id'                : {'primary'  : True},
            'id_transaction'    : {'reference': 'trans.id', 'unique': True},
            'id_item'           : {'reference': 'item.id', 'unique': True},
            'qty'               : {'caption'  : 'Quantity', 'preprocess': filter_qty}
        }
    }
]

# and here is the magic:
csv2db(file_name, csv_param, connection_string, table_structure_list, callback)