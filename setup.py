from setuptools import find_packages,setup 
from typing import List

def get_requirements(file_path:str)->List[str]:
    ''' This will return the list of required libraries'''
    requirements=[]
    e_setup = '-e .'

    with open(file_path) as file_obj:
        requirements= file_obj.readlines()
        requirements= [req.replace("\n","") for req in requirements]

        if e_setup in requirements:
            requirements.remove(e_setup)
    return requirements



setup(
    name='Streamlit_App_Incident_Reports',
    version='0.0.1',
    author='sankalp srivastava',
    author_email='sankalp.srivastava@bold.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)