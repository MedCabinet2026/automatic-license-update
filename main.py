import pyodbc
from tkinter import *
from tkinter import ttk
import pandas as pd
from dotenv import load_dotenv
from os import getenv, startfile
from lxml import etree

load_dotenv()
conn_str_db = (
    f"DRIVER={getenv('DRIVER_DB')};"
    f"SERVER={getenv('SERVER')};"
    f"DATABASE={getenv('DATABASE_NAME')};"
    f"UID={getenv('UID')};"
    f"PWD={getenv('PASSWORD')};"
    f"TrustServerCertificate={getenv('TrustServerCertificate')};"
    f"Encrypt={getenv('Encrypt')}"
)

df_excel = pd.read_excel("C:/Users/bohdan.kovba/Desktop/python_projects_for_de/Customer_Info_MK.xlsx", sheet_name=0, header=0)
customer_name_list = list(df_excel["Назва клініки"])

root = Tk()
root.geometry("500x500")
root.title("Automatic license reset")

main_frame = ttk.Frame(root, padding=10, borderwidth=10)
label_first_row = ttk.Label(main_frame, text='Automatic license reset\nPlease enter customer name in the field below')

customer_name = StringVar()
customer_port = StringVar()
customer_database = StringVar()
customer_license_GUID = StringVar()
customer_server = StringVar()

combobox_customer_name = ttk.Combobox(main_frame, textvariable=customer_name, height=150, width=400)
combobox_customer_name["values"] = customer_name_list

def check_license ():
    global customer_name, customer_port, customer_license_GUID, customer_database, customer_server

    customer_name = combobox_customer_name.get()
    customer_label['text'] = f'Customer Name: {customer_name}'
  
    customer_database = df_excel.loc[df_excel['Назва клініки'] == customer_name, 'Clinic DB'].iloc[0]
    customer_database_label['text'] = f'Customer Database: {customer_database}'

    customer_port = df_excel.loc[df_excel['Назва клініки'] == customer_name, 'Port'].iloc[0]
    customer_port_label['text'] = f'Customer Port: {customer_port}'

    customer_license_GUID = df_excel.loc[df_excel['Назва клініки'] == customer_name, 'SecurityProfileGUID'].iloc[0]
    customer_support_GUID_label['text'] = f'Customer Support GUID: {customer_license_GUID}'

    customer_server = df_excel.loc[df_excel['Назва клініки'] == customer_name, 'ServerName'].iloc[0]    
    customer_server_label['text'] = f'Customer Server: {customer_server}'


def update (event):
    text = combobox_customer_name.get().lower()

    if text == "":
        combobox_customer_name["values"] = customer_name_list
    else:
        combobox_customer_name["values"] = [
            item
            for item in customer_name_list
            if text in item.lower()     
        ]

query2 = ""
query3 = ""
correct_conn_str = ""

def select_license ():
    global query2, correct_conn_str, query3

    print(customer_name)
    print(customer_database)
    print(customer_port)
    print(customer_license_GUID)
    print(customer_server)

    correct_conn_str = f'net.tcp://{customer_server}.eleks.com:{customer_port}/'
    query2 = f"select count(1) from {customer_database}.dbo.Computer with (nolock) where SecurityProfileGUID = '{customer_license_GUID}' group by SecurityProfileGUID"
    query3 = f"select top 1 ComputerID from {customer_database}.dbo.Computer with (nolock) where SecurityProfileGUID = '{customer_license_GUID}' order by ComputerDLC asc"
    print(query2)


print(correct_conn_str)

def start_program():
    tree = etree.parse("C:/Users/bohdan.kovba/Desktop/Important/Client/Client/Doctor Eleks.exe.config")
    tree_root = tree.getroot()
    setting_node = tree_root.find(".//setting[@name='Doctor_Eleks_localhost_DataServices']/value/ArrayOfString/string")
    print(setting_node.text)
    setting_node.text = correct_conn_str
    print(setting_node.text)

    query4 = ""

    tree.write("C:/Users/bohdan.kovba/Desktop/Important/Client/Client/Doctor Eleks.exe.config", xml_declaration=True, encoding='utf-8')

    conn = pyodbc.connect(conn_str_db)
    print("Connected to SQL Server")
    
    cursor = conn.cursor()
    comp_id = 0
    cursor.execute(query2)
    result = cursor.fetchall()
    print(result)
    result = result[0]
    for i in result:
        if i >= 2:
            cursor.execute(query3)
            comp_id = cursor.fetchall()
            print(comp_id)
            query4 = f"update {customer_database}.dbo.Computer set SecurityProfileGUID = NULL where computerId in ({comp_id[0][0]})"
            cursor.execute(query4)
            cursor.commit()
    cursor.close()
    conn.close()

    startfile("C:/Users/bohdan.kovba/Desktop/Important/Client/Client/Doctor Eleks.exe")

customer_label = ttk.Label(root)
customer_database_label = ttk.Label(root)
customer_port_label = ttk.Label(root)
customer_support_GUID_label = ttk.Label(root)
customer_server_label = ttk.Label(root)

combobox_customer_name.bind("<KeyRelease>", update)
accept_button = ttk.Button(main_frame, text="Submit customer", command=check_license)

change_button = ttk.Button(main_frame, text="View license", command=select_license)

start_button = ttk.Button(main_frame, text="Start", command=start_program)

label_first_row.pack()
combobox_customer_name.pack()

main_frame.pack()
accept_button.pack()
change_button.pack()


customer_label.pack()
customer_database_label.pack()
customer_port_label.pack()
customer_support_GUID_label.pack()
customer_server_label.pack()

start_button.pack()

root.mainloop()