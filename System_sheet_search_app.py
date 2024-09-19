# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 11:10:53 2024

@author: KT1
"""

import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql
import streamlit_ext as ste
from datetime import datetime
import os
import uuid
from streamlit_pdf_viewer import pdf_viewer

import plotly.express as px

#Create Connection
conn = psycopg2.connect(database="system_sheet", user="postgres", password="lkjhgnhI1@", host="localhost", port=5432)
cur = conn.cursor()

# Function Defination
def display_PDF(file):
    pdf_viewer(file)#, rendering="legacy_iframe")
    
def download_PDF(file):
    with open(file, "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    ste.download_button(label="Download PDF",
                    data=PDFbyte,
                    file_name=str(file),
                    mime='application/octet-stream')

def display_image(file):
    st.image(image = file,use_column_width = 'always')
    
def get_search_output(company_input, panel_input):
    # Convert input to f-string
    company_input = f"%{company_input}%" if company_input else None
    panel_input = f"%{panel_input}%" if panel_input else None
    #params
    params = (company_input, company_input, panel_input, panel_input)
    
    cur.execute("""
        SELECT *
        FROM excel_data JOIN system_sheet_header 
        ON excel_data.pdf_name = system_sheet_header.pdf_name
        WHERE
        (%s IS NULL OR system_sheet_header.factory_name_combined ILIKE %s) AND
        (%s IS NULL OR system_sheet_header.panel_code ILIKE %s)
    """, params)
    
    matched_data = cur.fetchall()
    column_names = [description[0] for description in cur.description]
    matched_df = pd.DataFrame(data = matched_data, columns = column_names)
    matched_df = matched_df.loc[:,~matched_df.columns.duplicated()].copy()
    return matched_df

def get_substrate():
    cur.execute("""SELECT * FROM substrate""")
    substrate = cur.fetchall()
    column_names = [description[0] for description in cur.description]
    df_substrate = pd.DataFrame(data = substrate, columns = column_names)
    return df_substrate

def save_bug_report_to_db(report_content, user_email, image_path):
    try:
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(database="system_sheet", user="postgres", password="lkjhgnhI1@", host="localhost", port=5432)
        cursor = conn.cursor()
        
        # Insert bug report into a table
        insert_query = sql.SQL(
            "INSERT INTO bug_report (description, user_email, report_date, image_path) VALUES (%s, %s, %s, %s)"
        )
        cursor.execute(insert_query, (report_content, user_email, datetime.now(), image_path))
        
        # Commit the transaction
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error saving bug report to the database: {e}")
        return False
    



#Function to check user credentials
def check_credentials(username, password):
    # Hash the password
    hashed_password = password
    
    try:
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(database="system_sheet", user="postgres", password="lkjhgnhI1@", host="localhost", port=5432)
        cursor = conn.cursor()
        
        # Query to check if the user exists with the given username and hashed password
        query = sql.SQL("SELECT username, password FROM users WHERE username = %s AND password = %s")
        cursor.execute(query, (username, hashed_password))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        # Return True if user exists, otherwise False
        return result is not None
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return False

# Initialize session state for user login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "show_login_form" not in st.session_state:
    st.session_state.show_login_form = True

# Login Page
def login_page():
    st.title("Login")
    
    if st.session_state.logged_in:
        st.success("You are already logged in.")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.show_login_form = True
            st.experimental_rerun()
    else:
        # Show login form
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if check_credentials(username, password):
                    st.success("Login successful!")
                    st.session_state.logged_in = True
                    st.session_state.show_login_form = False
                    st.rerun()
                else:
                    st.error("Invalid username or password")






#########################################
    # Search App  
#########################################
       
def main_app():
    if "show_bug_form" not in st.session_state:
        st.session_state.show_bug_form = False 

    with st.sidebar:
        
        st.markdown('# Input Company Name')
        company_input = st.text_input('E.g. Kaiser, Timber, 國掌, QUỐC TRƯỞNG')
        
        st.markdown('# Input Panel (Furniture) Code')
        panel_input = st.text_input('E.g. 212, 734')
        st.write('\n')
        show_system_sheet = st.checkbox('Show System Sheet', value=False)
        st.write('\n')
        search_button = st.button('Search', type = "primary")
        st.write('\n')
        report_button = st.button('Report a Bug')
        
    if report_button:
        st.session_state.show_bug_form = not st.session_state.show_bug_form
    st.title('System Sheet Search')
    if "search_button" not in st.session_state:
        st.session_state.search_button = False 
    if search_button or st.session_state.search_button:
        st.session_state.search_button = True
        i=0
        if not company_input and not panel_input:
            st.write("Please Enter a Name/Code to search")
        else:
            matched_df = get_search_output(company_input, panel_input)
            
            if matched_df.empty:
                st.write("No System Sheet Found For This Code")
            else:
                # Filter by year
                matched_df['year'] = pd.to_datetime(matched_df['date']).dt.year
                year_list = matched_df['year'].unique()
                year_list = sorted(year_list, reverse=True)
                selected_year = st.multiselect('Select Year', year_list)
                filtered_df = matched_df[matched_df['year'].isin(selected_year)]
                
                pdf_path_list = filtered_df['pdf_path'].tolist()
                image_path_list = filtered_df['image_path'].tolist()
                pdf_name_list = filtered_df['pdf_name'].tolist()
                
                
                st.write("Total System Sheet Found:", len(pdf_path_list))
                st.write("System Sheet Characteristics")
                
                
                # Sheen plot
                sheen_df = filtered_df['sheen'].value_counts().reset_index()
                sheen_fig = px.bar(sheen_df, x='sheen', y='count', text='count')
                sheen_fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
                st.plotly_chart(sheen_fig, use_container_width=True)
                # Paint system grouped plot
                paint_system_df = filtered_df['paint_system_grouped'].value_counts().reset_index()
                paint_system_fig = px.bar(paint_system_df, x='paint_system_grouped', y='count', text='count')
                paint_system_fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
                st.plotly_chart(paint_system_fig, use_container_width=True)
                # Substrate plot
                df_substrate = get_substrate()
                df_substrate = df_substrate[df_substrate['pdf_name'].isin(pdf_name_list)]
                df_substrate = df_substrate[df_substrate['substrate_tw']!='']
                df_substrate['substrate_combined'] = df_substrate['substrate_vn'] + ' - ' + df_substrate['substrate_tw']
                df_substrate = df_substrate['substrate_combined'].value_counts().reset_index()
                substrate_fig = px.bar(df_substrate, x='substrate_combined', y='count', text='count')
                substrate_fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
                st.plotly_chart(substrate_fig, use_container_width=True)
                
                if show_system_sheet:
                    for image_path, pdf_path, pdf_name in zip(image_path_list, pdf_path_list, pdf_name_list):
                        i+=1
                        # with st.container():
                        st.write(f"Search Result No.{i}")
                        col_1, col_2 = st.columns(2)
                        with col_1:
                            try:
                                display_image(image_path)
                                #st.write(pdf_path)
                            except:
                                st.write('No Image Preview For This System Sheet')
                        with col_2:
                            try:
                                #display_pdf_with_google_drive(pdf_id)
                                display_PDF(pdf_path)
                                download_PDF(pdf_path)
                                st.write(pdf_name)
                            except:
                                st.write('No PDF Preview For This System Sheet')
                                #st.write(pdf_path)
                
#########################################
    #Bug Report Form
#########################################
    UPLOAD_DIR = r"D:\VL1251\uploaded_images"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    st.markdown("---")

    if st.session_state.show_bug_form:
        st.header("Report a Bug")

        # Create a form for the bug report
        with st.form("bug_report_form", clear_on_submit=True):
            bug_description = st.text_area("Describe the bug")
            user_email = st.text_input("Your email (Optional)", placeholder="your_email@gmail.com")
            
            # Image upload component
            uploaded_image = st.file_uploader("Upload an image (Recommended)", type=["png", "jpg", "jpeg"])
            
            # Submit button
            submit_button = st.form_submit_button(label="Submit Bug Report")
            
            # Handle the form submission
            if submit_button:
                image_path = None
                
                # Save the uploaded image if there is one
                if uploaded_image is not None:
                    # Generate a unique file name using UUID
                    file_extension = os.path.splitext(uploaded_image.name)[1]  # Get the file extension (e.g., .jpg, .png)
                    new_file_name = f"{uuid.uuid4()}{file_extension}"  # Create a unique file name
                    image_path = os.path.join(UPLOAD_DIR, new_file_name)
                    
                    # Save the file with the new name
                    with open(image_path, "wb") as f:
                        f.write(uploaded_image.getbuffer())
                
                if bug_description:
                    if save_bug_report_to_db(bug_description, user_email, image_path):
                        st.success("Bug report submitted successfully. Thank you!")
                    else:
                        st.error("Failed to submit bug report. Please try again later.")
                else:
                    st.warning("Please describe the bug before submitting.")

# Main entry point of the app
def main():
    if st.session_state.show_login_form:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()              


