import streamlit as st 
import pandas as pd




def get_side_bar_filters(time_filtered_data):

    """
    Define and apply multiselect filters with layout sidebar.
    Returns the selected filter values.
    """

    

    

    with st.sidebar:
        st.header("Choose your filters: ",divider="gray")
        st.caption("Select the filters serially from top to bottom")

        manager_selected = st.sidebar.multiselect("Manager Name",time_filtered_data['Manager Name'].unique())
        team_selected = st.sidebar.multiselect("Team Name",time_filtered_data[time_filtered_data['Manager Name'].isin(manager_selected)]['Team Name'].unique())
        sprint_selected = st.sidebar.multiselect("Sprint Name",time_filtered_data[time_filtered_data['Manager Name'].isin(manager_selected) & time_filtered_data['Team Name'].isin(team_selected)]['Sprint Name'].unique()) if team_selected else st.sidebar.multiselect("Sprint Name",time_filtered_data[time_filtered_data['Manager Name'].isin(manager_selected)]['Sprint Name'].unique())
        sprint_status_selected = st.sidebar.multiselect("Sprint Status",time_filtered_data['Sprint Status'].unique())
        ticket_type_selected = st.sidebar.multiselect("Ticket Type",time_filtered_data['Ticket Type'].unique())

        
    

    
    return manager_selected,team_selected,sprint_selected,sprint_status_selected,ticket_type_selected
