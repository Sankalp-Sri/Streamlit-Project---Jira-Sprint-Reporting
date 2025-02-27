import sys 
from app.utils.logger import logging

def error_message_detail(error,error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()

    file_name=exc_tb.tb_frame.f_code.co_filename 

    error_message = f"An error occured in python script with name {file_name} & line number {exc_tb.tb_lineno} & error message {str(error)}"

    return error_message

#inheriting exception class
class CustomException(Exception):
    def __init__(self, error_message,error_detail: sys):
        super().__init__(error_message)

        self.error_message = error_message_detail(error=error_message,error_detail=error_detail)

    def __str__(self):
        return self.error_message
    

if __name__=="__main__":
    try:
        1/0 
    except Exception as e:
        logging.info("Divide by zero error")
        raise CustomException(e,sys)
        
