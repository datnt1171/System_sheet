# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 10:55:14 2024

@author: KT1
"""

import os
import pandas as pd
from io import StringIO
## connect to postgresql

import psycopg2
conn = psycopg2.connect(database="system_sheet", user="postgres", password="lkjhgnhI1@", host="localhost", port=5432)
cur = conn.cursor()


main_folder_path = r'D:\VL1251\Ratio_compare\production_process\QUY TRINH MOI'

excel_name_list = []
excel_sheet_list = []
#excel_text_list = []
excel_path_list = []


# Get the information of excel file
for root, dirs, files in os.walk(main_folder_path):
    for file in files:
        if file.endswith('.xlsx') or file.endswith('.xls'):
            file_path = os.path.join(root, file)
            
            # Read all sheets from the Excel file
            excel_sheets = pd.read_excel(file_path, sheet_name=None)
            
            # Loop through each sheet
            for sheet_name, sheet_data in excel_sheets.items():
                # Append file name
                excel_name_list.append(file)
                # Append sheet name
                excel_sheet_list.append(sheet_name)
                # Append the DataFrame for the current sheet
                #excel_text_list.append(sheet_data)
                # Append the path to the list
                excel_path_list.append(file_path)


# Convert excel file to pdf to display
###############################################################################
# import win32com.client

# error_path_list = []
# error_sheet_list = []
# def excel_2_pdf(excel_path, excel_sheet):
    
#         excel = win32com.client.Dispatch("Excel.Application")
#         excel.Visible = True
        
#         WB_PATH = excel_path
#         # PDF path when saving
#         PATH_TO_PDF = excel_path.replace('.xlsx','')
#         PATH_TO_PDF = PATH_TO_PDF.replace('.xls','')
#         PATH_TO_PDF = PATH_TO_PDF + "_" + excel_sheet + '.pdf'
        
        
#         # Open
#         try:
#             wb = excel.Workbooks.Open(WB_PATH)
#             # Specify the sheet you want to save by index. 1 is the first (leftmost) sheet.
#             wb.WorkSheets(excel_sheet).Select()
#             # Save
#             wb.ActiveSheet.ExportAsFixedFormat(0, PATH_TO_PDF)
#             wb.Close()
#             excel.Quit()
#         except:
            
#             error_path_list.append(excel_path)
#             error_sheet_list.append(excel_sheet)



# for excel_path, excel_sheet in zip(excel_path_list,excel_sheet_list):
#     excel_2_pdf(excel_path, excel_sheet)
###############################################################################



#excel_text_list_csv = [df.to_csv(index=False) for df in excel_text_list]  # Convert each DataFrame to a CSV string




cur.execute("""DROP TABLE excel_data;""")
cur.execute("""DROP TABLE bug_report;""")
cur.execute("""DROP TABLE users;""")
conn.commit()
# Create table
cur.execute("""CREATE TABLE excel_data(
            excel_name TEXT,
            excel_sheet TEXT,
            excel_path TEXT,
            pdf_path TEXT,
            image_path TEXT,
            pdf_name TEXT);
            """)
            
cur.execute(""" CREATE TABLE bug_report(
            id SERIAL PRIMARY KEY,
            description TEXT NOT NULL,
            user_email TEXT,
            report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            image_path TEXT
            )""")

cur.execute("""CREATE TABLE users(
            user_id SERIAL PRIMARY KEY,
            username text,
            password text
            )""")

conn.commit()



# Create pdf_path and image_path
col_map = {'excel_name':excel_name_list,
           'excel_sheet':excel_sheet_list,
           'excel_path':excel_path_list}
df = pd.DataFrame(col_map)
df['pdf_path'] = df['excel_path'].replace('.xlsx','',regex=True)
df['pdf_path'] = df['pdf_path'].replace('.xls','',regex=True)
df['pdf_path'] = df['pdf_path'] + "_" + df['excel_sheet'] + '.pdf'

df['image_path'] = df['excel_path'].replace('.xlsx','',regex=True)
df['image_path'] = df['image_path'].replace('.xls','',regex=True)
df['image_path'] = df['image_path'] + "_" + df['excel_sheet'] + '.png'

df['pdf_name'] = df['excel_name'].replace('.xlsx','',regex=True)
df['pdf_name'] = df['pdf_name'].replace('.xls','',regex=True)
df['pdf_name'] = df['pdf_name'] + "_" + df['excel_sheet'] + '.pdf'
# Insert data into table

for excel_name, excel_sheet, excel_path, pdf_path, image_path, pdf_name in \
zip(df['excel_name'], df['excel_sheet'], df['excel_path'], df['pdf_path'], df['image_path'], df['pdf_name']):
    cur.execute("""
        INSERT INTO excel_data (excel_name, excel_sheet, excel_path, pdf_path, image_path, pdf_name)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (excel_name, excel_sheet, excel_path, pdf_path, image_path, pdf_name))
conn.commit()




# Delete useless excel_sheet
cur.execute("""DELETE FROM excel_data WHERE excel_sheet = '打打打打打'""")
cur.execute("""DELETE FROM excel_data WHERE excel_sheet = '資料資料'""")
cur.execute("""DELETE FROM excel_data WHERE excel_sheet = 'INININ.A4x2'""")
cur.execute("""DELETE FROM excel_data WHERE excel_sheet = 'MAU1'""")
cur.execute("""DELETE FROM excel_data WHERE excel_sheet = 'MAU2'""")
cur.execute("""DELETE FROM excel_data WHERE excel_sheet = 'NEW'""")
cur.execute("""DELETE FROM excel_data WHERE excel_sheet = '空白表格-再修改'""")
cur.execute("""DELETE FROM excel_data WHERE excel_sheet = '產品編號'""")
cur.execute("""DELETE FROM excel_data WHERE excel_sheet = 'V'""")
cur.execute("""DELETE FROM excel_data WHERE excel_sheet = 'Material code'""")
cur.execute("""DELETE FROM excel_data WHERE excel_sheet = '印-V'""")
cur.execute("""DELETE FROM excel_data WHERE excel_sheet = '印-中'""")
# Import user into user table
cur.execute("INSERT INTO users (username, password) VALUES ('dat', '123')")
cur.execute("INSERT INTO users (username, password) VALUES ('stanley', '123')")
cur.execute("INSERT INTO users (username, password) VALUES ('dungtq', '123')")

conn.commit()


# cur.execute("SELECT * from excel_data where excel_text like '%5703%' ;")
# temp = cur.fetchall()





# System sheet header
cur.execute("DROP table system_sheet_header")
conn.commit()
cur.execute("""CREATE TABLE system_sheet_header(
            pdf_name TEXT,
            date DATE,
            factory_name_combined TEXT,
            panel_code TEXT,
            paint_system_grouped TEXT,
            paint_system TEXT,
            sheen TEXT,
            distressing TEXT,
            customber_name TEXT,
            description TEXT)""")
conn.commit()


system_sheet_header = pd.read_excel(r'D:\VL1251\Ratio_compare\production_process\new_db.xlsx')
output = StringIO()
system_sheet_header.to_csv(output, sep='\t', header=False, index=False)
output.seek(0)

# Define the table name
table_name = 'system_sheet_header'

try:
    # Copy data to the table
    cur.copy_from(output, table_name, sep='\t')
    conn.commit()
    print("DataFrame imported to PostgreSQL successfully!")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if cur:
        cur.close()
    if conn:
        conn.close()


df_substrate = pd.read_excel(r'D:\VL1251\Ratio_compare\production_process\df_substrate.xlsx')
df_substrate = df_substrate[['pdf_name','gb','vn','tw']]
output = StringIO()
df_substrate.to_csv(output, sep='\t', header=False, index=False)
output.seek(0)
cur.execute("""DROP TABLE substrate""")
conn.commit()
cur.execute("""CREATE TABLE substrate(
            pdf_name TEXT,
            gb TEXT,
            vn TEXT,
            tw TEXT)""")
conn.commit()
# Define the table name
table_name = 'substrate'

try:
    # Copy data to the table
    cur.copy_from(output, table_name, sep='\t')
    conn.commit()
    print("DataFrame imported to PostgreSQL successfully!")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
