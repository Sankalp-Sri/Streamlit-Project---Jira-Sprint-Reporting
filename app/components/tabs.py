import streamlit as st 
import pandas as pd 
import os 
import sys 
from app.utils.exception import CustomException
from app.utils.logger import logging
from app.components.calculations import get_score_card
import plotly.express as px
import plotly.graph_objects as go




def render_sprint_tab(data,tab_name):
    ###############################
    #TAB-1
    try:
        with tab_name:

            _,_,col3,col4 = st.columns([3,3,2,2],gap='large',vertical_alignment='center')

            #Metric Calculation
            total_story_points,avg_story_points  = get_score_card(data)

            with col3:
                st.metric(label='Total Story Points',value=total_story_points)
                st.caption("Overall Story Points")
            with col4:
                st.metric(label='Avg Story Points',value=avg_story_points)
                st.caption("Total Points/#Sprints")



            col1,col2 = st.columns([1,2],gap='large',vertical_alignment='center')
            with col1:
                sprint_wise_story = data.groupby('Sprint Name',as_index=False)['Story Points'].sum()
                sprint_wise_story.sort_values(by='Story Points',ascending=False,inplace = True)
                # st.write("Sprint Wise Story Points", anchor="my-anchor")
                st.markdown("<div style='text-align: center;'><h3>Sprint Wise Story Points</h3></div>", unsafe_allow_html=True)
                st.dataframe(sprint_wise_story,use_container_width = True,hide_index=True)
            
            with col2:
                team_wise_story = data.groupby('Team Name',as_index=False)['Story Points'].sum()
                team_wise_story.sort_values(by='Story Points',ascending=False,inplace = True)

                
                fig_pie_sprint = px.pie(team_wise_story,names='Team Name',values='Story Points',color='Team Name',hole=0.5,labels={"Story Points"})
                fig_pie_sprint.update_traces(textinfo='value')
                fig_pie_sprint.update_layout(height=500, width=400, autosize=False)
                # st.write("Story Point Breakup - Team Wise",anchor="my-anchor")
                st.markdown("<div style='text-align: center;'><h3>Story Point Breakup - Team Wise</h3></div>", unsafe_allow_html=True)
                st.plotly_chart(fig_pie_sprint,use_container_width=True,key='pie_chart_sprint')
            
            st.divider()

            monthly_trend = data.groupby('Sprint Start Date',as_index=False)[['Story Points','Bugs Raised']].sum()
            monthly_trend.sort_values(by='Sprint Start Date',ascending=True,inplace = True)

            st.markdown("<div style='text-align: center;'><h3>Sprint Velocity Chart</h3></div>", unsafe_allow_html=True)

            fig_line_sprint = go.Figure()
            fig_line_sprint.add_trace(go.Bar(x=monthly_trend['Sprint Start Date'],y=monthly_trend['Story Points'],name= 'Story Points',
                                    yaxis='y1',marker_color='darkgreen',text=monthly_trend['Story Points'],textposition='outside'))

            fig_line_sprint.add_trace(go.Scatter(x=monthly_trend['Sprint Start Date'],y=monthly_trend['Bugs Raised'],name= 'Bugs Raised',
                                    yaxis='y2',mode='lines+markers+text',line=dict(color='maroon'),text=monthly_trend['Bugs Raised'],textposition='top right'))

            fig_line_sprint.update_layout(
                
                xaxis=dict(title="Sprint Start Date",showgrid=False),
                
                # Left y-axis
                yaxis=dict(
                    title="Story Points",
                    titlefont=dict(color="black"),
                    tickfont=dict(color="black"),
                    showgrid=False,
                    range=[0, monthly_trend['Story Points'].max() + 10]
                ),
                
                # Right y-axis
                yaxis2=dict(
                    title="Bugs Raised",
                    titlefont=dict(color="maroon"),
                    tickfont=dict(color="maroon"),
                    anchor="x",
                    overlaying="y",
                    side="right",
                    showgrid=False,
                    range=[0, monthly_trend['Bugs Raised'].max() + 5]
                ),
                
                legend=dict(
                title="Metrics",  # Title for the legend
                orientation="h",  # Horizontal orientation
                x=1.0,  # Center the legend
                y=1.1,  # Position it above the chart
                xanchor='center',  # Center anchor
                yanchor='bottom'  # Anchor at the bottom
                ),
                # Set figure width and height
                width=800,
                height=500
            )


            st.plotly_chart(fig_line_sprint,use_container_width=True,key='line_chart_sprint')
    except Exception as e:
        CustomException(e,sys)


def render_dev_tab(data,tab_name):
    try:
     with tab_name:

        #Dividing Columns
        col_filter,_,col_metric1,col_metric2 = st.columns([3,3,2,2],gap='large',vertical_alignment='center')

        

        #Dev Filter
        with col_filter:
            dev_selected=st.multiselect("Choose Dev: ",data['Dev Name'].unique())

        if dev_selected and not data.empty:
            data = data[data['Dev Name'].isin(dev_selected)]

        #Metric Calculation
        total_story_points,avg_story_points  = get_score_card(data)

        with col_metric1:
            st.metric(label='Total Story Points',value=total_story_points)
            st.caption("Overall Story Points")
        with col_metric2:
            st.metric(label='Avg Story Points',value=avg_story_points)
            st.caption("Total Points/#Sprints")
        
        # Proceed only if the filtered DataFrame is not empty
        if not data.empty:
            df_pivot_dev = data.pivot_table(
                values=['Story Points', 'Bugs Raised'],
                columns='Sprint Name',
                index='Dev Name',
                aggfunc='sum',
                dropna=True
            )

            # Swapping the column levels 
            df_pivot_dev.columns = pd.MultiIndex.from_product([df_pivot_dev.columns.levels[1], df_pivot_dev.columns.levels[0]],names=['Metric', 'Sprint Name'])

            df_pivot_dev.reset_index(inplace=True)

            # df_pivot[['Story Points','Bugs Raised']].fillna(0,inplace=True)

            st.dataframe(df_pivot_dev,use_container_width=True,hide_index=True)
        else:
            st.write("No data available for the selected developers.")


        st.divider()       

        col_pie_dev,col_line_dev = st.columns([1,2],gap='large',vertical_alignment='center')

        with col_pie_dev:
            dev_wise_story = data.groupby('Dev Name',as_index=False)['Story Points'].sum()
            dev_wise_story.sort_values(by='Story Points',ascending=False,inplace = True)

                
            fig_pie_dev = px.pie(dev_wise_story,names='Dev Name',values='Story Points',color='Dev Name',hole=0.5,labels={"Story Points"})
            fig_pie_dev.update_traces(textinfo='value')
            fig_pie_dev.update_layout(height=500, width=400, autosize=False)
            # st.write("Story Point Breakup - Team Wise",anchor="my-anchor")
            st.markdown("<div style='text-align: center;'><h3>Story Point Breakup - Dev Wise</h3></div>", unsafe_allow_html=True)
            st.plotly_chart(fig_pie_dev,use_container_width=True,key='pie_chart_dev')

        with col_line_dev:
            dev_monthly_trend= data.copy()
            dev_monthly_trend.dropna(inplace=True)
            dev_monthly_trend = dev_monthly_trend.groupby('Sprint Start Date',as_index=False)[['Story Points','Bugs Raised']].sum()
            dev_monthly_trend.sort_values(by='Sprint Start Date',ascending=True,inplace = True)

            st.markdown("<div style='text-align: center;'><h3>Sprint Velocity Chart</h3></div>", unsafe_allow_html=True)


            if not dev_monthly_trend.empty:
                fig_line_dev = go.Figure()
                fig_line_dev.add_trace(go.Bar(x=dev_monthly_trend['Sprint Start Date'],y=dev_monthly_trend['Story Points'],name= 'Story Points',
                                        yaxis='y1',marker_color='darkgreen',text=dev_monthly_trend['Story Points'],textposition='outside'))

                fig_line_dev.add_trace(go.Scatter(x=dev_monthly_trend['Sprint Start Date'],y=dev_monthly_trend['Bugs Raised'],name= 'Bugs Raised',
                                        yaxis='y2',mode='lines+markers+text',line=dict(color='maroon'),text=dev_monthly_trend['Bugs Raised'],textposition='top right'))

                fig_line_dev.update_layout(
                    
                    xaxis=dict(title="Sprint Start Date",showgrid=False),
                    
                    # Left y-axis
                    yaxis=dict(
                        title="Story Points",
                        titlefont=dict(color="black"),
                        tickfont=dict(color="black"),
                        showgrid=False,
                        range=[0, dev_monthly_trend['Story Points'].max() + 10]
                    ),
                    
                    # Right y-axis
                    yaxis2=dict(
                        title="Bugs Raised",
                        titlefont=dict(color="maroon"),
                        tickfont=dict(color="maroon"),
                        anchor="x",
                        overlaying="y",
                        side="right",
                        showgrid=False,
                        range=[0, dev_monthly_trend['Bugs Raised'].max() + 5]
                    ),
                    
                    legend=dict(
                    title="Metrics",  # Title for the legend
                    orientation="h",  # Horizontal orientation
                    x=1.0,  # Center the legend
                    y=1.1,  # Position it above the chart
                    xanchor='center',  # Center anchor
                    yanchor='bottom'  # Anchor at the bottom
                    ),
                    # Set figure width and height
                    width=800,
                    height=500
                )

            
            
                st.plotly_chart(fig_line_dev,use_container_width=True,key='line_chart_dev')
            else:
                st.write("No relevant Data")
    except Exception as e:
        CustomException(e,sys)


def render_qa_tab(data,tab_name):
    try:
        with tab_name:

            #Dividing Columns
            col_filter,_,col_metric1,col_metric2 = st.columns([3,3,2,2],gap='large',vertical_alignment='center')

            #Dev Filter
            with col_filter:
                qa_selected=st.multiselect("Choose QA: ",data['Qa Name'].unique())

            if qa_selected and not data.empty:
                data = data[data['Qa Name'].isin(qa_selected)]

            #Metric Calculation
            total_story_points,avg_story_points  = get_score_card(data)

            with col_metric1:
                st.metric(label='Total Story Points',value=total_story_points)
                st.caption("Overall Story Points")
            with col_metric2:
                st.metric(label='Avg Story Points',value=avg_story_points)
                st.caption("Total Points/#Sprints")
            
            # Proceed only if the filtered DataFrame is not empty
            if not data.empty:
                df_pivot_qa = data.pivot_table(
                    values=['Story Points'],
                    columns='Sprint Name',
                    index='Qa Name',
                    aggfunc='sum',
                    dropna=True
                )


                df_pivot_qa.reset_index(inplace=True)

                # df_pivot[['Story Points','Bugs Raised']].fillna(0,inplace=True)

                st.dataframe(df_pivot_qa,use_container_width=True,hide_index=True)
            else:
                st.write("No data available for the selected QA.")


            "---"        

            col_pie_qa,col_line_qa = st.columns([1,2],gap='large',vertical_alignment='center')

            with col_pie_qa:
                qa_wise_story = data.groupby('Qa Name',as_index=False)['Story Points'].sum()
                qa_wise_story.sort_values(by='Story Points',ascending=False,inplace = True)

                    
                fig_pie_qa = px.pie(qa_wise_story,names='Qa Name',values='Story Points',color='Qa Name',hole=0.5,labels={"Story Points"})
                fig_pie_qa.update_traces(textinfo='value')
                fig_pie_qa.update_layout(height=500, width=400, autosize=False)
                # st.write("Story Point Breakup - Team Wise",anchor="my-anchor")
                st.markdown("<div style='text-align: center;'><h3>Story Point Breakup - QA Wise</h3></div>", unsafe_allow_html=True)
                st.plotly_chart(fig_pie_qa,use_container_width=True,key='pie_chart_qa')

            with col_line_qa:
                qa_monthly_trend= data.copy()
                qa_monthly_trend.dropna(inplace=True)
                qa_monthly_trend = qa_monthly_trend.groupby('Sprint Start Date',as_index=False)['Story Points'].sum()
                qa_monthly_trend.sort_values(by='Sprint Start Date',ascending=True,inplace = True)

                st.markdown("<div style='text-align: center;'><h3>Sprint Velocity Chart</h3></div>", unsafe_allow_html=True)

                fig_line_qa = go.Figure()
                fig_line_qa.add_trace(go.Bar(x=qa_monthly_trend['Sprint Start Date'],y=qa_monthly_trend['Story Points'],name= 'Story Points',
                                        yaxis='y1',marker_color='darkgreen',text=qa_monthly_trend['Story Points'],textposition='outside'))


                fig_line_qa.update_layout(
                    
                    xaxis=dict(title="Sprint Start Date",showgrid=False),
                    
                    # Left y-axis
                    yaxis=dict(
                        title="Story Points",
                        titlefont=dict(color="black"),
                        tickfont=dict(color="black"),
                        showgrid=False,
                        range=[0, qa_monthly_trend['Story Points'].max() + 10]
                    ),
                    
                    
                    legend=dict(
                    title="Metric",  # Title for the legend
                    orientation="h",  # Horizontal orientation
                    x=1.0,  # Center the legend
                    y=1.1,  # Position it above the chart
                    xanchor='center',  # Center anchor
                    yanchor='bottom'  # Anchor at the bottom
                    ),
                    # Set figure width and height
                    width=800,
                    height=500
                )


                st.plotly_chart(fig_line_qa,use_container_width=True,key='line_chart_qa')
    except Exception as e:
        st.write(CustomException(e,sys))



def render_detailed_data_tab(data,tab_name):
    try:
        with tab_name:

            #Dividing Columns
            col_filter_1,col_filter_2,_,_ = st.columns([2,2,4,4],gap='large',vertical_alignment='center')

            #Dev Filter
            with col_filter_1:
                dev_selected_tab4=st.multiselect("Choose Devs: ",data['Dev Name'].unique())

            #QA Filter
            with col_filter_2:
                qa_selected_tab4=st.multiselect("Choose QAs: ",data['Qa Name'].unique())

        
            if dev_selected_tab4 and not qa_selected_tab4 and not data.empty:
                final_filtered_data = data[data['Dev Name'].isin(dev_selected_tab4)]
                final_filtered_data=final_filtered_data[['Ticket Key','Sprint Name','Sprint Start Date','Summary','Component','Priority','Story Points']]
            elif qa_selected_tab4 and not dev_selected_tab4 and not data.empty:
                final_filtered_data = data[data['Qa Name'].isin(qa_selected_tab4)]
                final_filtered_data=final_filtered_data[['Ticket Key','Sprint Name','Sprint Start Date','Summary','Component','Priority','Story Points']]
            elif  dev_selected_tab4 and qa_selected_tab4 and not data.empty:
                final_filtered_data = data[data['Dev Name'].isin(dev_selected_tab4)][data['QA Name'].isin(qa_selected_tab4)]
                final_filtered_data=final_filtered_data[['Ticket Key','Sprint Name','Sprint Start Date','Summary','Component','Priority','Story Points']]
            else:
                final_filtered_data=data[['Ticket Key','Sprint Name','Sprint Start Date','Summary','Component','Priority','Story Points']]

            st.dataframe(final_filtered_data,use_container_width = True,hide_index=True)
    except Exception as e:
        st.write(CustomException(e,sys))
