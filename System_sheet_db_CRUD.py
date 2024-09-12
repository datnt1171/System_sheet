# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 10:55:14 2024

@author: KT1
"""

import os
import pandas as pd


main_folder_path = r'D:\VL1251\Ratio_compare\production_process\QUY TRINH MOI'

excel_name_list = []
excel_sheet_list = []
excel_text_list = []
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
                excel_text_list.append(sheet_data)
                # Append the path to the list
                excel_path_list.append(file_path)


# Convert excel file to pdf to display
###############################################################################
import win32com.client

error_path_list = []
error_sheet_list = []
def excel_2_pdf(excel_path, excel_sheet):
    
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = True
        
        WB_PATH = excel_path
        # PDF path when saving
        PATH_TO_PDF = excel_path.replace('.xlsx','')
        PATH_TO_PDF = PATH_TO_PDF.replace('.xls','')
        PATH_TO_PDF = PATH_TO_PDF + "_" + excel_sheet + '.pdf'
        
        
        # Open
        try:
            wb = excel.Workbooks.Open(WB_PATH)
            # Specify the sheet you want to save by index. 1 is the first (leftmost) sheet.
            wb.WorkSheets(excel_sheet).Select()
            # Save
            wb.ActiveSheet.ExportAsFixedFormat(0, PATH_TO_PDF)
            wb.Close()
            excel.Quit()
        except:
            
            error_path_list.append(excel_path)
            error_sheet_list.append(excel_sheet)



for excel_path, excel_sheet in zip(excel_path_list,excel_sheet_list):
    excel_2_pdf(excel_path, excel_sheet)
###############################################################################



excel_text_list_csv = [df.to_csv(index=False) for df in excel_text_list]  # Convert each DataFrame to a CSV string

## connect to postgresql
import psycopg2
conn = psycopg2.connect(database="system_sheet", user="postgres", password="lkjhgnhI1@", host="localhost", port=5432)
cur = conn.cursor()


# cur.execute("""DROP TABLE Excel_data;""")
# cur.execute("""DROP TABLE bug_report;""")
# cur.execute("""DROP TABLE users;""")
# conn.commit()
# Create table
cur.execute("""CREATE TABLE Excel_data(
            excel_id SERIAL PRIMARY KEY,
            excel_name TEXT,
            excel_sheet TEXT,
            excel_text TEXT,
            excel_path TEXT);
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

# Make the changes to the database persistent
conn.commit()

# Insert data into table
for name, sheet, text, path in zip(excel_name_list, excel_sheet_list, excel_text_list_csv, excel_path_list):
    cur.execute("""
        INSERT INTO Excel_data (excel_name, excel_sheet, excel_text, excel_path)
        VALUES (%s, %s, %s, %s);
    """, (name, sheet, text, path))
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
# Import user into user table
cur.execute("INSERT INTO users (username, password) VALUES ('dat', '123')")
cur.execute("INSERT INTO users (username, password) VALUES ('stanley', '123')")
cur.execute("INSERT INTO users (username, password) VALUES ('dungtq', '123')")


cur.close()
conn.close()

cur.execute("SELECT * from excel_data where excel_text like '%5703%' ;")
temp = cur.fetchall()
