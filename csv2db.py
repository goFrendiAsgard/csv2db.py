import csv

def csv2db(FILE_NAME, CSV_PARAM={}, CONNECTION_STRING='sqlite:///db.db', TABLE_STRUCTURE={}, CALLBACK={}):
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
        print row

    engine = create_engine(CONNECTION_STRING, echo=True) 
    '''
    # insert statement
    sql = 'INSERT INTO users(name, password) VALUES(:user_name, :user_password)'
    conn.execute(text(sql), user_name='Tino', user_password='secret')

    # select statement
    sql = 'SELECT * FROM users'
    print (conn.execute(text(sql)).fetchall())
    '''