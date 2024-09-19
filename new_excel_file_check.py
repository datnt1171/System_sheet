import os
import pandas as pd
import shutil
import win32com.client

main_folder_path = r'D:\VL1251\Ratio_compare\production_process\QUY TRINH MOI'
check_folder_path = r'U:\QUY TRINH MOI'

# Check for new file
def get_cm_time(folder_path):
    excel_path_list = []
    excel_name_list = []
    excel_ctime = []
    excel_mtime = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.xlsx') or file.endswith('.xls'):
                file_path = os.path.join(root, file)
                excel_name_list.append(os.path.basename(file_path))
                excel_path_list.append(file_path)
                excel_ctime.append(os.path.getctime(file_path))
                excel_mtime.append(os.path.getmtime(file_path))
    
    map_time = {'excel_path':excel_path_list,
                'excel_name':excel_name_list,
                'ctime':excel_ctime,
                'mtime':excel_mtime}
    
    df = pd.DataFrame(map_time)
    df['ctime'] = pd.to_datetime(df['ctime'], unit='s')
    df['mtime'] = pd.to_datetime(df['mtime'], unit='s')
    return df


df_main = get_cm_time(main_folder_path) #Old file
df_check = get_cm_time(check_folder_path) #New file

# Get diff file
main_excel_name = df_main['excel_name']
check_excel_name = df_check['excel_name']
excel_new = set(check_excel_name) - set(main_excel_name)
df_new = df_check[df_check['excel_name'].isin(excel_new)]

# Remove Ignore file (non-system_sheet file)
df_ignore = pd.read_excel(r'D:\VL1251\Ratio_compare\production_process\ignore_list.xlsx')
ignore_list = df_ignore['excel_name']
df_new = df_new[~df_new['excel_name'].isin(ignore_list)]

# Convert unix time to m/d/yyyy
df_new['ctime'] = df_new['ctime'].dt.date
df_new['mtime'] = df_new['mtime'].dt.date
df_new.sort_values(by='ctime', inplace=True)




# Copy new file to temp folder to check
copy_folder = r'D:\VL1251\Ratio_compare\production_process\NEW_FILE_CHECK'

excel_file_source = df_new['excel_path'].tolist()
for file_path in excel_file_source:
    # Get the file name
    file_name = os.path.basename(file_path)
    
    # Create the destination path
    dest_path = os.path.join(copy_folder, file_name)
    
    # Copy the file
    shutil.copy2(file_path, dest_path)




def get_excel_information(path_to_folder):
    
    excel_name_list = []
    excel_sheet_list = []
    excel_path_list = []
    
    # Get the information of excel file
    for root, dirs, files in os.walk(path_to_folder):
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
    return excel_name_list, excel_sheet_list, excel_path_list

excel_name_list, excel_sheet_list, excel_path_list = get_excel_information(copy_folder)
    



def excel_2_pdf(excel_path, excel_sheet):

        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False
        
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
            
            
error_path_list = []
error_sheet_list = []

ignore_sheet_list = ['打打打打打','資料資料','INININ.A4x2','MAU1','MAU2','NEW','空白表格-再修改'
                     ,'產品編號','V','Material code','印-V','印-中']
for excel_path, excel_sheet in zip(excel_path_list,excel_sheet_list):
    if excel_sheet in ignore_sheet_list:
        continue
    else:
        excel_2_pdf(excel_path, excel_sheet)
    



col_map = {'excel_name':excel_name_list,
           'excel_sheet':excel_sheet_list,
           'excel_path':excel_path_list}
df = pd.DataFrame(col_map)

df = df[~df['excel_sheet'].isin(ignore_sheet_list)]

df['pdf_path'] = df['excel_path'].replace('.xlsx','',regex=True)
df['pdf_path'] = df['pdf_path'].replace('.xls','',regex=True)
df['pdf_path'] = df['pdf_path'] + "_" + df['excel_sheet'] + '.pdf'

df['image_path'] = df['excel_path'].replace('.xlsx','',regex=True)
df['image_path'] = df['image_path'].replace('.xls','',regex=True)
df['image_path'] = df['image_path'] + "_" + df['excel_sheet'] + '.png'

df['pdf_name'] = df['excel_name'].replace('.xlsx','',regex=True)
df['pdf_name'] = df['pdf_name'].replace('.xls','',regex=True)
df['pdf_name'] = df['pdf_name'] + "_" + df['excel_sheet'] + '.pdf'

col_path = ['excel_path','pdf_path','image_path']
for col in col_path:
    df[col] = df[col].str.replace(r'NEW_FILE_CHECK','QUY TRINH MOI')

df.to_excel(r'D:\VL1251\Ratio_compare\production_process\new_excel_data.xlsx', index=False)





