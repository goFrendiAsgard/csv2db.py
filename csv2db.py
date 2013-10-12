import csv
from sqlalchemy import create_engine

def csv2db(FILE_NAME, CSV_PARAM={}, CONNECTION_STRING='sqlite:///db.db', TABLE_STRUCTURE_LIST=[], CALLBACK={}):
    csvfile = open(FILE_NAME, 'rb')
    reader = csv.reader(csvfile, **CSV_PARAM)
    header = []
    row_list = []

    # get header and row_list
    for row in reader:
        if len(header)==0:
            header = row
        else:
            row_list.append(row)

    # use callback to every cell
    for row in row_list:
        for i in xrange(len(row)):
            caption = header[i]
            if caption in CALLBACK:
                row[i] = CALLBACK[caption](row[i])

    engine = create_engine(CONNECTION_STRING, echo=True) 
    conn = engine.connect()

    table_data = {}
    table_unique_field_list = {}
    table_primary_key = {}
    table_caption_dict = {}
    for table_structure in TABLE_STRUCTURE_LIST:
        if 'table_name' not in table_structure:
            table_structure['table_name'] = ''
        if 'column_list' not in table_structure:
            table_structure['column_list'] = ''
        table_name = table_structure['table_name']
        column_list = table_structure['column_list']
        table_data[table_name] = {}
        table_caption_dict[table_name] = {}
        table_unique_field_list[table_name] = []
        table_primary_key[table_name] = ''
        for column in column_list:
            table_data[table_name][column] = ''
            if 'caption' not in column_list[column]:
                column_list[column]['caption'] = ''
            if 'primary' not in column_list[column]:
                column_list[column]['primary'] = False
            if 'unique' not in column_list[column]:
                column_list[column]['unique'] = False
            table_caption_dict[table_name][column] = column_list[column]['caption']
            if column_list[column]['primary']:
                table_primary_key[table_name]=column
            if column_list[column]['unique']:
                table_unique_field_list[table_name].append(column)

    print table_data
    print table_unique_field_list
    print table_primary_key
    print table_caption_dict
    print row_list
    '''
    # insert statement
    sql = 'INSERT INTO users(name, password) VALUES(:user_name, :user_password)'
    conn.execute(text(sql), user_name='Tino', user_password='secret')

    # select statement
    sql = 'SELECT * FROM users'
    print (conn.execute(text(sql)).fetchall())
    '''