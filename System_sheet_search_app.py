# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 15:53:28 2024

@author: KT1
"""

import streamlit as st
import pandas as pd
import psycopg2
import base64
import math
conn = psycopg2.connect(database="test_1", user="postgres", password="lkjhgnhI1@", host="localhost", port=5432)
cur = conn.cursor()

def get_excel_path(keyword):
    cur.execute("SELECT excel_sheet, excel_path \
                FROM Excel_data \
                WHERE excel_text LIKE %s", (f"%{keyword}%",))
    matched_data = cur.fetchall()
    matched_df = pd.DataFrame(pd.DataFrame(data = matched_data, columns=['excel_sheet','excel_path']))
    excel_path_list = matched_df['excel_path'].tolist()
    excel_sheet_list = matched_df['excel_sheet'].to_list()
    
    return excel_path_list, excel_sheet_list
keyword = "093"
a, b = get_excel_path(keyword)
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

# Path to the PDF file

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

def search_multiple_keywords(keywords):
    # Sanitize user input by escaping special characters
    keywords = [kw.strip() for kw in keywords if kw.strip()]  # Remove empty strings

    # Prepare SQL query
    query = "SELECT excel_sheet, excel_path FROM Excel_data WHERE "
    conditions = " AND ".join(["excel_text LIKE %s" for _ in keywords])
    query += conditions

    # Prepare parameters for the query
    params = tuple(f"%{kw}%" for kw in keywords)  # SQL LIKE pattern

    # Execute the query
    cur.execute(query, params)
    results = cur.fetchall()
    return results


search_by = st.sidebar.selectbox(
    "Search by Furniture code/Customer name/Paint code",
    ("Furniture code","Customer name","Paint code")
)
RESULTS_PER_PAGE = 5
if search_by == "Furniture code":


    st.title("Search by Furniture (Panel) code")
    search_str = st.text_input("Enter panel code")
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1
    if st.button("Search"):
        if search_str:
            # Mock function to get excel paths (replace with your actual function)
            excel_path_list, excel_sheet_list = get_excel_path(search_str)
            if excel_path_list:
                # Prepare lists for PDF and image paths
                pdf_path_list = []
                image_path_list = []
                for excel_path, excel_sheet in zip(excel_path_list, excel_sheet_list):
                    pdf_path_list.append(get_pdf_path(excel_path, excel_sheet))
                    image_path_list.append(get_image_path(excel_path, excel_sheet))
                    

                # Calculate start and end index for slicing the results list
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
                            except:
                                st.write('No PDF Preview For This System Sheet')
            else:
                st.write("No System Sheet Found For This Code")
        else:
            st.write("Please enter a code to search")



elif search_by == "Paint code":
    st.title("Search by paint combination")
    multiple_paint_code = "multiple paint code"
    st.write(f"Please enter **{multiple_paint_code}** (a combination of paint) \
              each paint code must seperate by a white space")
    search_str = st.text_input("Enter paint combination")
    if st.button("Search"):
        if search_str:
            excel_path_list = search_multiple_keywords(search_str)
            for excel_path in excel_path_list:
                st.write(excel_path)
        else:
            st.write("No System Sheet")
    else:
        st.write("Enter a code to search")

