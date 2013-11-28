import csv, collections, codecs, sys
from sqlalchemy import create_engine, text



def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]

def csv2db(FILE_NAME, CSV_PARAM={}, CONNECTION_STRING='sqlite:///db.db', TABLE_STRUCTURE_LIST=[], CALLBACK={}):
    # UTF-8 hell
    UTF8Writer = codecs.getwriter('utf8')
    sys.stdout = UTF8Writer(sys.stdout)

    # open the file
    csvfile = open(FILE_NAME, 'rb')
    #reader = csv.reader(csvfile, **CSV_PARAM)
    reader = unicode_csv_reader(csvfile, **CSV_PARAM)
    csv_caption = []
    csv_row_list = []

    # get header and row_list
    for row in reader:
        if len(csv_caption)==0:
            csv_caption = row
        else:
            csv_row_list.append(row)

    # use callback to every cell
    for row_index in xrange(len(csv_row_list)):
        row = csv_row_list[row_index]
        for i in xrange(len(row)):
            caption = csv_caption[i]
            if caption in CALLBACK:
                csv_row_list[row_index][i] = CALLBACK[caption](row[i])

    table_data = {}
    table_name_list = []
    table_unique_field_list = {}
    table_reference_list = {}
    table_field_list = {}
    table_primary_key = {}
    table_caption_dict = {}
    table_preprocess_dict = {}
    for table_structure in TABLE_STRUCTURE_LIST:
        if 'table_name' not in table_structure:
            table_structure['table_name'] = ''
        if 'column_list' not in table_structure:
            table_structure['column_list'] = ''
        table_name = table_structure['table_name']
        column_list = table_structure['column_list']
        table_name_list.append(table_name)
        table_data[table_name] = {}
        table_caption_dict[table_name] = {}
        table_field_list[table_name] = []
        table_unique_field_list[table_name] = []
        table_reference_list[table_name] = []
        table_primary_key[table_name] = ''
        table_preprocess_dict[table_name] = {}
        for column in column_list:
            table_field_list[table_name].append(column)
            table_data[table_name][column] = ''
            if 'caption' not in column_list[column]:
                column_list[column]['caption'] = ''
            if 'primary' not in column_list[column]:
                column_list[column]['primary'] = False
            if 'unique' not in column_list[column]:
                column_list[column]['unique'] = False
            if 'reference' not in column_list[column]:
                column_list[column]['reference'] = ''
            if 'preprocess' not in column_list[column]:
                column_list[column]['preprocess'] = False
            table_caption_dict[table_name][column] = column_list[column]['caption']
            if column_list[column]['primary']:
                table_primary_key[table_name]=column
            if column_list[column]['unique']:
                table_unique_field_list[table_name].append(column)
            if column_list[column]['reference'] != '':      
                reference_table, reference_column = column_list[column]['reference'].split('.')
                table_reference_list[table_name].append({
                    'ref_table':reference_table, 'ref_column':reference_column,
                    'real_column':column})
            if isinstance(column_list[column]['preprocess'], collections.Callable):
                table_preprocess_dict[table_name][column] = column_list[column]['preprocess']

    engine = create_engine(CONNECTION_STRING, encoding='utf8', convert_unicode=True, echo=False) 
    conn = engine.connect()

    for csv_row in csv_row_list:
        # get table_data from csv (or from previous record)
        for table_name in table_name_list:
            field_list = table_field_list[table_name]
            caption_dict = table_caption_dict[table_name]
            primary_key = table_primary_key[table_name]  
            preprocess_dict = table_preprocess_dict[table_name]         
            data = {}
            all_is_empty = True
            for field in field_list:
                for i in xrange(len(csv_row)):
                    caption = csv_caption[i]
                    if caption == caption_dict[field] and caption != '': 
                        if csv_row[i] == '':
                            data[field] = None
                        else:
                            if field in preprocess_dict:
                                data[field] = preprocess_dict[field](csv_row[i])
                            else:
                                data[field] = csv_row[i]
                            all_is_empty = False  
            if all_is_empty:                
                table_data[table_name].pop(primary_key, None)
            else:
                table_data[table_name] = data
        for table_name in table_name_list:
            field_list = table_field_list[table_name]
            primary_key = table_primary_key[table_name]
            reference_list = table_reference_list[table_name]            
            unique_field_list = table_unique_field_list[table_name]
            
            # get foreign key values
            for reference in reference_list:
                reference_table = reference['ref_table']
                reference_column = reference['ref_column']
                real_column = reference['real_column']
                if reference_table in table_data:
                    if reference_column in table_data[reference_table]:
                        table_data[table_name][real_column] = table_data[reference_table][reference_column]

            # define sql_syntaxes
            where_by_unique_field_list = []
            for unique_field in unique_field_list:
                where_by_unique_field_list.append(unique_field+' = :'+unique_field)
            where_by_unique_field = ' AND '.join(where_by_unique_field_list)
            where_by_primary_key = primary_key+' = :'+primary_key
            field_name_list = []
            field_value_list = []
            field_set_list = []
            for field in field_list:
                if field != primary_key:
                    field_name_list.append(field)
                    field_value_list.append(':'+field)
                    field_set_list.append(field+'=:'+field)
            field_name = ', '.join(field_name_list)
            field_value = ', '.join(field_value_list)
            field_set = ', '.join(field_set_list)
            selected_field_name = primary_key
            if field_name != '':
                selected_field_name += ', '+field_name

            sql_select_by_unique_field = 'SELECT '+selected_field_name+' FROM '+table_name+' WHERE '+where_by_unique_field
            sql_select_by_primary_key = 'SELECT '+selected_field_name+' FROM '+table_name+' WHERE '+where_by_primary_key
            sql_insert = 'INSERT INTO '+table_name+'('+field_name+') VALUES('+field_value+')'
            sql_update = 'UPDATE '+table_name+' SET '+field_set+' WHERE '+where_by_primary_key

            if primary_key not in table_data[table_name]:
                field_list = table_field_list[table_name]
                for field in field_list:
                    if field not in table_data[table_name] and field != primary_key:
                        table_data[table_name][field] = None
                # if there is such a data, get id by using unique_field
                sql = sql_select_by_unique_field
                result = conn.execute(text(sql), **table_data[table_name]).fetchall()
                operation = '' # This variable is just for visual matter
                operation_success = False
                operation_sql = ''
                if len(result)>0:
                    row = result[0]
                    table_data[table_name][primary_key] = row[0]
                    sql = sql_update
                    data = table_data[table_name]
                    operation_success = conn.execute(text(sql), **table_data[table_name])
                    operation_sql = sql
                    operation = 'update'
                else:
                    sql = sql_insert
                    data = table_data[table_name]
                    operation_success = conn.execute(text(sql), **table_data[table_name])
                    operation_sql = sql
                    operation = 'insert'
                    sql = sql_select_by_unique_field
                    result = conn.execute(text(sql), **table_data[table_name]).fetchall()
                    if len(result)>0:
                        row = result[0]
                        table_data[table_name][primary_key] = row[0]                    
                # View
                operation_success_string = "success" if operation_success else "fail"
                print ('')
                print ('TABLE NAME : '+table_name)
                print ('OPERATION  : '+operation)
                print ('SUCCESS    : '+operation_success_string)
                for key in table_data[table_name]:
                    try:
                        print ('  '+key+' : '+unicode(table_data[table_name][key]))
                    except:
                        print ('  '+key+' : '+str(table_data[table_name][key]))
                print ('SQL        : '+operation_sql)
                print ('')