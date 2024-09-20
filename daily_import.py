# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 10:56:29 2024

@author: KT1
"""

import pandas as pd
import psycopg2

conn = psycopg2.connect(database="system_sheet", user="postgres", password="lkjhgnhI1@", host="localhost", port=5432)
cur = conn.cursor()

def insert_data(df_data, table_name):
    """
    Inserts data from a DataFrame into a specified PostgreSQL table.

    Parameters:
    df_data (pd.DataFrame): DataFrame containing the data to insert.
    conn (psycopg2 connection): Active connection to the PostgreSQL database.
    table_name (str): The name of the table to insert data into.
    """
    try:
        # Get the column names from the DataFrame
        columns = list(df_data.columns)

        # Create the SQL insert query dynamically based on column names
        insert_query = f"""
            INSERT INTO {table_name} ({', '.join(columns)})
            VALUES ({', '.join(['%s'] * len(columns))});
        """

        # Convert the DataFrame to a list of tuples (for batch insert)
        data = [tuple(row[1:]) for row in df_data.itertuples()]

        # Execute the batch insert
        cur.executemany(insert_query, data)
        conn.commit()

        print("Data inserted successfully!")
    except Exception as e:
        conn.rollback()  # Rollback in case of any error
        print(f"An error occurred: {e}")
        
        
        
# Check_point
check_point = pd.read_excel(r'D:\VL1251\Ratio_compare\production_process\check_point.xlsx')
check_point_id = check_point['id'][0]

# System_sheet_header data
system_sheet_header = pd.read_excel(r'D:\VL1251\Ratio_compare\production_process\system_sheet_header.xlsx')
system_sheet_header = system_sheet_header[system_sheet_header['id']>check_point_id]
insert_data(system_sheet_header, 'system_sheet_header') #Insert data


# Substrate data
df_substrate = pd.read_excel(r'D:\VL1251\Ratio_compare\production_process\df_substrate.xlsx')
df_substrate = df_substrate[df_substrate['id']>check_point_id]
df_substrate = df_substrate[['id','pdf_name','substrate_gb','substrate_vn','substrate_tw']]
insert_data(df_substrate,'substrate') #Insert data


# Excel data
df = pd.read_excel(r'D:\VL1251\Ratio_compare\production_process\new_excel_data.xlsx')
insert_data(df,'excel_data') #Insert data

# Update check_point
new_check_point = system_sheet_header['id'].tail(1)
new_check_point.to_excel(r'D:\VL1251\Ratio_compare\production_process\check_point.xlsx')
