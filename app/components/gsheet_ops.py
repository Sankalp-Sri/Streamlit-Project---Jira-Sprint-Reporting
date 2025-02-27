from oauth2client.service_account import ServiceAccountCredentials
import tempfile
import gspread
import pandas as pd
import os
from app.utils.exception import CustomException
import sys
from dotenv import load_dotenv
load_dotenv()
import json


#Defining Scopes
scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive']

with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as temp_file:
    temp_file.write(os.getenv('gsheet_json').encode('utf-8')) # Write JSON as bytes
    temp_file_path = temp_file.name



#Connection object
def connect():
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(temp_file_path,scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        raise CustomException(e,sys)
                                                             
    
#Reading Method
def read_from_sheet(conn_object,sheet_name,worksheet_name):
    try:
        wks = conn_object.open(sheet_name).worksheet(worksheet_name)
        #for getting list of dict
        sheet_data= wks.get_all_records()
        #for getting list of lists
        # sheet_data=wks.get_all_values()
        df = pd.DataFrame(sheet_data)
        return df
    except Exception as e:
        raise CustomException(e,sys)
    
    
