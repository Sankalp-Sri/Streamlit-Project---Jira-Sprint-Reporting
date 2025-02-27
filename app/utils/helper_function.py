import pandas as pd 
from datetime import datetime
from app.utils.exception import CustomException
import sys

def convert_to_date(dataframe,date_columns):
    try:
        for col in date_columns:
            dataframe[col]=pd.to_datetime(dataframe[col],errors='coerce')
        return dataframe
    except Exception as e:
        raise CustomException(e,sys)
