from utilities import mysql_conn
import xlrd

def excel_to_db(excel_path, table: str, columns: list = []):
    excel_sheet =xlrd.open_workbook(excel_path)
    sheet_name = excel_sheet.sheet_names()
    for sh in range(0,len(sheet_name)):
        sheet = excel_sheet.sheet_by_index(sh)
        row_values = ''
        for r in range(1,sheet.nrows):
            row_value = ''
            for i in range(len(columns)):
                row_value = row_value + f'{sheet.cell(r,i).value},'
            row_value = f"({row_value.rstrip(',')})"
            row_values = row_values + ','+row_value
        final_value_set = (row_values.lstrip(','))
    cols =''
    a = final_value_set.replace('(',"('")
    b = a.replace(',',"','")
    c = b.replace(")','(",'),(')
    d = c.replace(")","')")
    e = d.replace('.0','')
    for i in range(len(columns)):
        if i > 0 :
            act_col = ',' + columns[i]
        else :
            act_col = columns[i]
        cols = cols + act_col
    query = f"INSERT INTO {table} ({cols}) VALUES {e}"
    # print(query)
    mysql_conn.mysql_obj().mysql_execute(query, fetch_result=False)
    mysql_conn.mysql_obj().commit()
    mysql_conn.mysql_obj().close()

