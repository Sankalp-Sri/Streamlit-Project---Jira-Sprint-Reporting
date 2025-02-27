import streamlit as st
import pandas as pd
import numpy as np




#Scorecard
def get_score_card(data):
    total_story_points = int(data['Story Points'].sum())
    avg_story_points = int(total_story_points/data['Sprint Name'].nunique())
    return total_story_points,avg_story_points
