import streamlit as st 
from app.components import gsheet_ops as gs
from app.utils.exception import CustomException
from app.utils.logger import logging 
from app.utils.helper_funciton import convert_to_date
import sys
import os
import pandas as pd

if os.getenv('ENV') == 'prod':
    from config.config_prod import *
else:
    from config.config_QA import *

@st.cache_data
def load_data():
    try:
        obj_gsheet = gs.connect()
        df = gs.read_from_sheet(obj_gsheet,sheet_name=sprint_data_sheet_name,worksheet_name=sprint_data_worksheet_name)

        return df
    except Exception as e:
        raise CustomException(e,sys)
    
def transform_data(data):
    ''' Rename columns and convert date columns into datetime '''
    try:
                #Minor transformation in data
        date_cols = ['created','updated','resolution','status_category_changed','sprint_start','sprint_end','sprint_start_date']
            
        data= convert_to_date(data,date_cols)

        

                #Renaming Column Names 
        col_map = {'sprint_start_date':'Sprint Start Date','dev_assigned':'Dev Name','qa_assigned':'QA Name','story_points':'Story Points','associated_bugs':'Bugs Raised',
            'sprint_name':'Sprint Name','sprint_status':'Sprint Status','ticket_type':'Ticket Type','components':'Component','priority':'Priority','ticket_key':'Ticket Key','summary':'Summary'} 

        data.rename(columns=col_map,inplace=True) 

        data.columns = data.columns.str.title()

        return data
    except Exception as e:
        CustomException(e,sys)



    

    
