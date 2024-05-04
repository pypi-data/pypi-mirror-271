import mysql.connector
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import ipywidgets as widgets
from IPython.display import display

def compare_departments():
    
    mydb = mysql.connector.connect(
         host="sql12.freemysqlhosting.net",
         user="sql12701694",
         password="bbHGHD5bdi",
         database="sql12701694"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SHOW TABLES")
    tab = mycursor.fetchall()

    consulta_2 = "SELECT ID, Sample_Collection_Date, O18, D, Dxs, O17, Sample_Type, Department FROM datasetinformation GROUP BY ID, Sample_Collection_Date, O18, D, Dxs, O17, Sample_Type, Department"
    mycursor.execute(consulta_2)
    results_site_2 = mycursor.fetchall()
    
    data = {
        'Department': [],
        'Sample_Collection_Date': [],
        'Sample_Type': [],
        'ID': [],
        'O18': [],
        'D': [],
        'O17': [],
        'Dxs': []
    }

    for ID, sample_collection_date, dataset_18O, dataset_D, dataset_Dxs, dataset_17O, sample_type, department in results_site_2:
        data['Department'].append(department)
        data['Sample_Collection_Date'].append(sample_collection_date)
        data['Sample_Type'].append(sample_type)
        data['ID'].append(ID)
        data['O18'].append(dataset_18O)
        data['O17'].append(dataset_17O)
        data['D'].append(dataset_D)
        data['Dxs'].append(dataset_Dxs)

    datasetinformation_df = pd.DataFrame(data)

    datasetinformation_df['Month'] = datasetinformation_df['Sample_Collection_Date'].dt.month

    department_dropdown_1 = widgets.Dropdown(
        options=datasetinformation_df['Department'].unique().tolist(),
        description='D1:'
    )

    department_dropdown_2 = widgets.Dropdown(
        options=datasetinformation_df['Department'].unique().tolist(),
        description='D2:'
    )

    sample_type_dropdown_1 = widgets.Dropdown(
        options=[],
        description='ST1:'
    )

    sample_type_dropdown_2 = widgets.Dropdown(
        options=[],
        description='ST2:'
    )

    season_dropdown_1 = widgets.Dropdown(
        options=['All', 'Summer', 'Winter'],
        description='Season 1:'
    )

    season_dropdown_2 = widgets.Dropdown(
        options=['All', 'Summer', 'Winter'],
        description='Season 2:'
    )

    def filter_dataframe(department, department_2, sample_type, sample_type_2, season, season_2):
        
        summer_months = [12, 1, 2, 3]
        winter_months = [6, 7, 8]

        
        filtered_df_1 = datasetinformation_df[(datasetinformation_df['Department'] == department) &
                                               (datasetinformation_df['Sample_Type'] == sample_type) &
                                               (((season == 'Summer') & datasetinformation_df['Month'].isin(summer_months)) |
                                                ((season == 'Winter') & datasetinformation_df['Month'].isin(winter_months)) |
                                                (season == 'All'))]

        filtered_df_2 = datasetinformation_df[(datasetinformation_df['Department'] == department_2) &
                                               (datasetinformation_df['Sample_Type'] == sample_type_2) &
                                               (((season_2 == 'Summer') & datasetinformation_df['Month'].isin(summer_months)) |
                                                ((season_2 == 'Winter') & datasetinformation_df['Month'].isin(winter_months)) |
                                                (season_2 == 'All'))]

        
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=filtered_df_1['Month'],
            y=filtered_df_1['O18'],
            mode='markers',
            name=department,
            marker=dict(
                color='pink',
                size=8
            )
        ))

        fig.add_trace(go.Scatter(
            x=filtered_df_2['Month'],
            y=filtered_df_2['O18'],
            mode='markers',
            name=department_2,
            marker=dict(
                color='blue',
                size=8
            )
        ))

        fig.update_layout(
            title="Comparison of &#948;<sup>18</sup>O between Departments",
            xaxis_title="Month",
            yaxis_title="$\delta^{18}O (VSMOW ‰)$",
            showlegend=True,
            yaxis=dict(
                autorange='reversed'  # Invertir el eje y
            )
        )

        fig.show()

    def update_sample_type_dropdown_1(*args):
        department = department_dropdown_1.value
        sample_type_dropdown_1.options = datasetinformation_df[datasetinformation_df['Department'] == department]['Sample_Type'].unique().tolist()


    def update_sample_type_dropdown_2(*args):
        department = department_dropdown_2.value
        sample_type_dropdown_2.options = datasetinformation_df[datasetinformation_df['Department'] == department]['Sample_Type'].unique().tolist()


    department_dropdown_1.observe(update_sample_type_dropdown_1, 'value')
    department_dropdown_2.observe(update_sample_type_dropdown_2, 'value')

    return widgets.interactive(filter_dataframe,
                               department=department_dropdown_1,
                               department_2=department_dropdown_2,
                               sample_type=sample_type_dropdown_1,
                               sample_type_2=sample_type_dropdown_2,
                               season=season_dropdown_1,
                               season_2=season_dropdown_2)