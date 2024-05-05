'''
Used to retrieve data from a Google Sheets spreadsheet.
'''

import os.path
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.discovery import Resource

def _get_token_and_scopes(token_folder:str):
    # If modifying these scopes, delete the file token.json.
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    token_location = f"{token_folder}/token.json"
    credentials_location = f"{token_folder}/credentials.json"
    return [scopes, token_location, credentials_location]

def _remove_str_list(data: list[list[str]], remove_str_list: list[str]) -> list[list[str]]:
    '''
    Removes any unwanted strings from data.
    '''
    if "\r" not in remove_str_list:
        remove_str_list.append("\r")
    for i in data:
        for j in i:
            for k in remove_str_list:
                j = j.replace(k, "")
    return data

def call_spreadsheet_api(token_folder:str) -> list[list[str]]:
    '''
    Calls the Google Sheets API to retrieve the relevant range from the given spreadsheet.\n
    Data is returned as a list of lists, with each inner list being one row of the spreadsheet.
    '''
    scopes, token_location, credentials_location = _get_token_and_scopes(token_folder)
    creds = None
    if os.path.exists(token_location):
        creds = Credentials.from_authorized_user_file(token_location, scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        try:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_location, scopes)
                creds = flow.run_local_server(port=0)
        except RefreshError as e:
            print(e)
            flow = InstalledAppFlow.from_client_secrets_file(credentials_location, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_location, "w", encoding="utf-8") as token:
            token.write(creds.to_json())
    return creds


def retrieve_range(token_folder:str, spreadsheet_id: str, range_name: str, remove_str_list: list | None = None) -> list[list[str]]:
    '''
    Retrieves the relevant range from the given spreadsheet.\n
    Data is returned as a list of lists, with each inner list being one row of the spreadsheet.
    '''
    if remove_str_list is None: # Recommended by PyLint
        remove_str_list = []
    creds = call_spreadsheet_api(token_folder)

    data = []
    try:
        service: Resource = build("sheets", "v4", credentials=creds) # build is a general-purpose function that returns a dynamic object, so can't be type-checked

        # Call the Sheets API
        sheet = service.spreadsheets() # pylint: disable=no-member
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return data

        for row in values:
            data.append(row)
    except HttpError as err:
        print(err)
    data = _remove_str_list(data, remove_str_list)
    return data

def retrieve_range_index(token_folder:str, spreadsheet_id: str, range_name: str, remove_str_list: list | None = None) -> tuple[list[list[str]], dict[str, int]]:
    '''
    Identical to retrieve_range, except it also creates an index of the location of all data on the first row (which is assumed to be the header row). The first row is not removed.
    '''
    if remove_str_list is None:
        remove_str_list = []
    range_list = retrieve_range(token_folder, spreadsheet_id, range_name, remove_str_list)
    index: dict[str, int] = {}
    for i in range_list[0]: # Populate index
        index[i] = range_list[0].index(i)
    return range_list, index

def get_note(token_folder:str, spreadsheet_id: str, row: str, col: str):
    '''
    Retrieves the note from the specified cell of a spreadsheet.\n
    Data is returned as a list of lists, with each inner list being one row of the spreadsheet.
    '''
    coord = chr(row+64)+str(col)
    print(coord)

    creds = call_spreadsheet_api(token_folder)
    
    try:
        service: Resource = build("sheets", "v4", credentials=creds) # build is a general-purpose function that returns a dynamic object, so can't be type-checked

        # Call the Sheets API
        sheet = service.spreadsheets().get(spreadsheet_id) # pylint: disable=no-member
        result = sheet.data().rowData().values().note()
#        result = sheet.get(spreadsheetId=spreadsheet_id, fields="sheets/data/rowData/values/note").execute()
        values = result.execute()#.get("sheets/data/rowData/values/note")#("values", [])

        if not values:
            print("No data found.")
    except HttpError as err:
        print(err)
    return values
