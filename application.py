from google_sheets.read_sheets import read_excel, get_customer_names
from google_sheets.customer import get_customer, Customer
from tkinter import StringVar, ttk, messagebox
from gui.labelClass import CustomLabel, CustomRoot
from os import startfile
from lxml import etree
from database.database import connect_to_database
from queries.user_insert import insert_user_query

class Application():
    def __init__(self):
        self.customers_df = read_excel()
        self.customer_name_list = get_customer_names(self.customers_df)

        self.root = CustomRoot()

        self.main_frame = ttk.Frame(self.root, padding=10, borderwidth=10)

        self.create_widgets()
        self.bind_events()

    def create_widgets(self):
        CustomLabel(self.main_frame, text='Автоматичне занулення ліцензії та запуск клієнта\n', font_size=14).pack()
        CustomLabel(self.main_frame, text='Почніть вносити назву замовника у полі нижче\n', font_size=14).pack()
        CustomLabel(self.main_frame, text='та виберіть із списку\n', font_size=14).pack()

        self.customer_name = StringVar()

        self.combobox_customer_name = ttk.Combobox(
            self.main_frame,
            textvariable=self.customer_name,
            height=150, width=400
        )

        self.combobox_customer_name["values"] = self.customer_name_list
        self.combobox_customer_name.pack()
        self.main_frame.pack()

        self.customer_label = CustomLabel(self.root, text="Назва замовника:")
        self.customer_database_label = CustomLabel(self.root, text="БД:")
        self.customer_port_label = CustomLabel(self.root, text="Порт:")
        self.customer_support_GUID_label = CustomLabel(self.root, text="SecurityProfileGUID:")
        self.customer_server_label = CustomLabel(self.root, text="Сервер:")

        self.customer_label.pack()
        self.customer_database_label.pack()
        self.customer_port_label.pack()
        self.customer_support_GUID_label.pack()
        self.customer_server_label.pack()

        self.accept_button = ttk.Button(self.root, text="Вибрати замовника", command=self.check_license)
        self.user_check = ttk.Button(self.root, text="Перевірка користувача", command=self.check_user)
        self.start_button = ttk.Button(self.root, text="Запуск клієнта", command=self.start_program)

        self.accept_button.pack()
        self.user_check.pack()
        self.start_button.pack()

        
    def check_license (self):
        self.customer = get_customer(self.customers_df, self.combobox_customer_name.get())

        self.customer_label['text'] = f'Назва замовника: {self.customer.name}'
        self.customer_database_label['text'] = f'БД: {self.customer.database}'
        self.customer_port_label['text'] = f'Порт: {self.customer.port}'
        self.customer_support_GUID_label['text'] = f'SecurityProfileGUID: {self.customer.license_guid}'
        self.customer_server_label['text'] = f'Сервер: {self.customer.server}'


    def update (self, event):
        text = self.combobox_customer_name.get().lower()

        if text == "":
            self.combobox_customer_name["values"] = self.customer_name_list
        else:
            self.combobox_customer_name["values"] = [
                item
                for item in self.customer_name_list
                if text in item.lower()     
        ]


    def check_user(self):
        conn = connect_to_database(self.customer.database)
        cursor = conn.cursor()

        cursor.execute(
                    f"select UserName "
                    f"from {self.customer.database}.dbo.Users with (nolock) "
                    f"where UserLogin in ('bohdan')"
        )

        user_name = cursor.fetchone()

        if user_name is not None:
            messagebox.showinfo("Користувач", "Користувач вже існує")
        else:
            cursor.execute(insert_user_query)
            conn.commit()
            messagebox.showinfo("Користувач", "Користувача успішно створено")


    def start_program(self):
        self.update_client_config()
        self.reset_license()
        self.start_client()


    def update_client_config(self):
        config_path = "C:/Users/bohdan.kovba/Desktop/Important/Client/Client/Doctor Eleks.exe.config"
        tree = etree.parse(config_path)
        tree_root = tree.getroot()

        setting_node = tree_root.find(
            ".//setting[@name='Doctor_Eleks_localhost_DataServices']"
            "/value/ArrayOfString/string"
        )

        setting_node.text = (
            f"net.tcp://{self.customer.server}.eleks.com:"
            f"{self.customer.port}/"
        )

        tree.write(config_path, xml_declaration=True, encoding="utf-8")


    def reset_license(self):
        conn = connect_to_database(self.customer.database)
        cursor = conn.cursor()

        cursor.execute(
            f"select count(1) "
            f"from {self.customer.database}.dbo.Computer with (nolock) "
            f"where SecurityProfileGUID = '{self.customer.license_guid}' "
            f"group by SecurityProfileGUID"
        )

        result = cursor.fetchone()
        computer_count = result[0]

        if computer_count >= 2:
            cursor.execute(
                f"select top 1 ComputerID "
                f"from {self.customer.database}.dbo.Computer with (nolock) "
                f"where SecurityProfileGUID = '{self.customer.license_guid}' "
                f"order by ComputerDLC asc"
            )

            comp_id = cursor.fetchone()

            query4 = (
                f"update {self.customer.database}.dbo.Computer "
                f"set SecurityProfileGUID = NULL "
                f"where computerId in ({comp_id[0]})"
            )

            cursor.execute(query4)
            cursor.commit()

        cursor.close()
        conn.close()


    def start_client(self):
        client_path = "C:/Users/bohdan.kovba/Desktop/Important/Client/Client/Doctor Eleks.exe"
        startfile(client_path)


    def bind_events(self):
        self.combobox_customer_name.bind("<KeyRelease>", self.update)


    def run(self):
        self.root.mainloop()