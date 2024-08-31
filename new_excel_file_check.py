import os

main_folder_path = r'D:\VL1251\Ratio_compare\production_process\QUY TRINH MOI'
check_folder_path = r'U:\QUY TRINH MOI'

excel_main_path_list = []
excel_check_path_list = []
                
                
for root, dirs, files in os.walk(main_folder_path):
    for file in files:
        if file.endswith('xlsx') or file.endswith('.xls'):
            excel_main_path_list.append(os.path.join(root, file))
            
for root, dirs, files in os.walk(check_folder_path):
    for file in files:
        if file.endswith('.xlsx') or file.endswith('.xls'):
            excel_check_path_list.append(os.path.join(root, file))
            

main_prefix = "D:\\VL1251\\Ratio_compare\\production_process\\"
check_prefix = "U:\\"
# Remove the prefix from each path in the list
excel_main_path_list = [path.replace(main_prefix, "") for path in excel_main_path_list]
excel_check_path_list = [path.replace(check_prefix, "") for path in excel_check_path_list]

new_excel_files = set(excel_check_path_list) - set(excel_main_path_list)


            