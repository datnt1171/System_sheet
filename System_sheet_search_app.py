# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 15:53:28 2024

@author: KT1
"""

import streamlit as st
import pandas as pd
import psycopg2
import base64

#Create Connection
conn = psycopg2.connect(database="test_1", user="postgres", password="lkjhgnhI1@", host="localhost", port=5432)
cur = conn.cursor()

# Function Defination
def get_pdf_path(excel_path, excel_sheet):
    pdf_path = excel_path.replace('.xlsx','')
    pdf_path = excel_path.replace('.xls','')
    pdf_path = pdf_path + "_" + excel_sheet + '.pdf'
    return pdf_path

def get_image_path(excel_path, excel_sheet):
    image_path = excel_path.replace('.xlsx','')
    image_path = excel_path.replace('.xls','')
    image_path = image_path + "_" + excel_sheet + '.png'
    return image_path

def display_PDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # Embedding PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="500" height="700" type="application/pdf"></iframe>'
    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

def display_image(file):
    st.image(image = file,use_column_width = 'always')

def get_excel_path(company_input, panel_input, paint_input):
    # Convert input to f-string
    company_input = f"%{company_input}%" if company_input else None
    panel_input = f"%{panel_input}%" if panel_input else None
    paint_input = f"%{paint_input}%" if paint_input else None
    
    params = (company_input, company_input, panel_input, panel_input, paint_input, paint_input)
    #Execute query
    cur.execute("""
        SELECT excel_path, excel_sheet FROM excel_data WHERE
        (%s IS NULL OR excel_text LIKE %s) AND
        (%s IS NULL OR excel_text LIKE %s) AND
        (%s IS NULL OR excel_text LIKE %s)
    """, params)
    
    matched_data = cur.fetchall()
    matched_df = pd.DataFrame(pd.DataFrame(data = matched_data, columns=['excel_path','excel_sheet']))
    
    excel_path_list = matched_df['excel_path'].tolist()
    excel_sheet_list = matched_df['excel_sheet'].to_list()
    return excel_path_list, excel_sheet_list


with st.sidebar:
    st.markdown('# Input Company Name')
    company_input = st.text_input('company name')
    
    st.markdown('# Input Panel (Furniture) code')
    panel_input = st.text_input('panel code')
    
    st.markdown('# Input Paint Code')
    paint_input = st.text_input('paint code')
    
    search_button = st.button('Search')
    
if search_button:
    st.markdown('# System Sheet Search Result')
    excel_path_list, excel_sheet_list = get_excel_path(company_input if company_input else None,
                                panel_input if panel_input else None,
                                paint_input if paint_input else None)
    if excel_path_list:
        # Prepare lists for PDF and image paths
        pdf_path_list = []
        image_path_list = []
        for excel_path, excel_sheet in zip(excel_path_list, excel_sheet_list):
            pdf_path_list.append(get_pdf_path(excel_path, excel_sheet))
            image_path_list.append(get_image_path(excel_path, excel_sheet))
            

        for pdf_path, image_path in zip(pdf_path_list, image_path_list):
            with st.container():
                col_1, col_2 = st.columns(2)
                with col_1:
                    try:
                        display_image(image_path)
                    except:
                        st.write('No Image Preview For This System Sheet')
                with col_2:
                    try:
                        display_PDF(pdf_path)
                        st.write(pdf_path)
                    except:
                        st.write('No PDF Preview For This System Sheet')
    else:
        st.write("No System Sheet Found For This Code")
else:
    st.write("Please enter a code to search")
