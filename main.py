import os
import requests
import logging
from dotenv import load_dotenv

import PySimpleGUI as sg
from pydactyl import PterodactylClient


def main():
    sg.theme('DarkAmber')

    server_list = api.client.servers.list_servers().collect()
    server_dictionary = {server["attributes"]["name"]: server["attributes"]["uuid"] for server in server_list}

    layout = [
        [sg.Text('Server Upload'), sg.Combo(list(server_dictionary.keys()), key='-SERVER-', size=(20, 1))],
        [sg.Input(), sg.FileBrowse()],
        [sg.Submit(), sg.Cancel()]
    ]

    file_window = sg.Window('KISSUpload', layout)

    sg.theme()

    while True:
        file_event, file_values = file_window.read(timeout=100)

        if file_event == sg.WIN_CLOSED or file_event == 'Cancel':
            break

        if file_event == 'Submit':
            if file_values[0] == '' or file_values['-SERVER-'] == '':
                sg.popup("Please fill out all fields")
                continue

            file_path = file_values[0]
            file_values['-SERVER-'] = server_dictionary[file_values['-SERVER-']]
            upload_link = api.client.servers.files.get_upload_file_url(file_values['-SERVER-'])

            req = requests.post(upload_link + '&directory=/plugins/', files={'files': (os.path.basename(file_path), open(file_path, 'rb'))})
            if req.status_code == 200:
                sg.Popup("File uploaded successfully")
            else:
                sg.Popup("File upload failed")

    file_window.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    config = load_dotenv()
    api = PterodactylClient(os.getenv("PANEL_URL"), os.getenv("PANEL_KEY"))

    main()
