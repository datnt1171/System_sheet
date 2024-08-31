# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 14:07:44 2024

@author: KT1
"""

import gspread
import pandas as pd
import psycopg2
from io import StringIO
#Create service_account
gc = gspread.service_account(filename="creds.json")


pdf_id = gc.open("pdf_id").sheet1.get_all_values()
df_pdf = pd.DataFrame(pdf_id)

df_pdf.columns = df_pdf.iloc[0]
df_pdf = df_pdf[1:]

conn = psycopg2.connect(database="system_sheet", user="postgres", password="lkjhgnhI1@", host="localhost", port=5432)
cur = conn.cursor()


cur.execute("""CREATE TABLE pdf_data(
            pdf_path TEXT,
            pdf_name TEXT,
            cdate DATE,
            url TEXT,
            mdate TEXT)""")


    
output = StringIO()
df_pdf.to_csv(output, sep='\t', header=False, index=False)
output.seek(0)

# Define the table name
table_name = 'pdf_data'

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
