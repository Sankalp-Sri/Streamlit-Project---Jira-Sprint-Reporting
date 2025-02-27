import streamlit as st
import pandas as pd
import os 
import sys
from app.components.data_loader import *
from app.components.side_bar import get_side_bar_filters
from app.components.tabs import *
# from app.components.calculations import *
from dir_path import base_path
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')



def main():
    

    st.set_page_config(
        page_title="Sprint Report - Platform Services",
        page_icon="::bar_chart::",
        layout='wide',
        initial_sidebar_state='auto',
        menu_items = {
            'Report a bug' : 'mailto:sankalp.srivastava@bold.com',
            'About' : 'This app presents the work analysis of teams in platform services, based on sprint data !'
        }
    )

    
    st.title("Sprint Report - Platform Service ")
    

        # Logo file path or external image URL
    logo_url = os.path.join(base_path,'assets','bold-logo.png') # Use a local file or a URL

    st.image(logo_url, width=150) 

    with st.expander('About!'):
        st.markdown("**Details**")
        st.info("This app presents the work analysis of teams in platform service, based on sprint data")
        st.markdown("***How to interact with it?***")
        st.warning("To engage with this app you can select various filters from the side bar menu to view your choice of data and charts")


    # Load and cache data via the utility module
    data = load_data()

    if st.button("Reload Data"):
        st.cache_data.clear()

  
    #Apply Data Transformation

    trans_data = transform_data(data)



    col1,col2,col3_metric,col4_metric = st.columns([2.5,2.5,1,1],gap = 'large',vertical_alignment='center')




    #Date Filters

    startDate = pd.to_datetime(trans_data['Sprint Start Date']).min()
    endDate=pd.to_datetime(trans_data['Sprint Start Date']).max()

    with col1:
        date1 = pd.to_datetime(st.date_input("Start Date",startDate))

    with col2:
        date2 = pd.to_datetime(st.date_input("End Date",endDate))

    time_frame_data = trans_data[(trans_data['Sprint Start Date']>=date1) & (trans_data['Sprint Start Date']<=date2)].copy() 


    #####################################    Side Bar Config   #############################################
 
    manager_selected,team_selected,sprint_selected,sprint_status_selected,ticket_type_selected=get_side_bar_filters(time_frame_data)

    filtered_data = time_frame_data.copy()



    # Apply the Manager filter if any components are selected
    if manager_selected:
        filtered_data = filtered_data[filtered_data['Manager Name'].isin(manager_selected)]

    # Apply the Team Name filter if any are selected
    if team_selected:
        filtered_data = filtered_data[filtered_data['Team Name'].isin(team_selected)]

    # Apply the priority filter if any sprint are selected
    if sprint_selected:
        filtered_data = filtered_data[filtered_data['Sprint Name'].isin(sprint_selected)]

    # Apply the priority filter if any sprint status are selected
    if sprint_status_selected:
        filtered_data = filtered_data[filtered_data['Sprint Status'].isin(sprint_status_selected)]

    # Apply the priority filter if any priorities are selected
    if ticket_type_selected:
        filtered_data = filtered_data[filtered_data['Ticket Type'].isin(ticket_type_selected)]

    st.dataframe(filtered_data,use_container_width=True,hide_index=True)
    
    

    ##############################         Initialising Tabs for Different Level Reports        #####################################################3

    sprint_tab,dev_tab,qa_tab,detailed_data_tab = st.tabs(['Sprint Details','Dev Details','QA Details','Detailed Data'])

    render_sprint_tab(filtered_data,sprint_tab)

    render_dev_tab(filtered_data,dev_tab)

    render_qa_tab(filtered_data,qa_tab)

    render_detailed_data_tab(filtered_data,detailed_data_tab)



if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        CustomException(e,sys)
