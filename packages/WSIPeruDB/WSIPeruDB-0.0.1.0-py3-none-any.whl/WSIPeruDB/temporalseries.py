import mysql.connector
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import ipywidgets as widgets
from IPython.display import display

def analyze_temporal_series():
    
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

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)

    data = {
         'Department': [],
         'Sample_Collection_Date':[],
         'Sample_Type': [],
         'ID': [],
         'O18': [],
         'D': [],
         'O17':[],
         'Dxs':[]
    }


    for ID,sample_collection_date,dataset_18O, dataset_D, dataset_Dxs, dataset_17O, sample_type, department in results_site_2:
        data['Department'].append(department)
        data['Sample_Collection_Date'].append(sample_collection_date)
        data['Sample_Type'].append(sample_type)
        data['ID'].append(ID)
        data['O18'].append(dataset_18O)
        data['O17'].append(dataset_17O)
        data['D'].append(dataset_D)
        data['Dxs'].append(dataset_Dxs)

    datasetinformation_df = pd.DataFrame(data)

    department_dropdown = widgets.Dropdown(
        options=datasetinformation_df['Department'].unique().tolist(),
        description='Department:'
    )

    sample_type_dropdown = widgets.Dropdown(
        options=[],
        description='Sample Type:'
    )

    id_dropdown = widgets.Dropdown(
        options=[],
        description='ID:'
    )

    def filter_dataframe(department, sample_type, ID):
        if ID == 'All':
            filtered_df_1 = datasetinformation_df[(datasetinformation_df['Department'] == department) &
                                                  (datasetinformation_df['Sample_Type'] == sample_type)]

            # Crear histograma
            layout = go.Layout(title="Histogram of &#948;<sup>18</sup>O")
            fig = go.Figure(data=[go.Histogram(x=filtered_df_1['O18'], marker_color='pink', marker_line_color='black', marker_line_width=1)], layout=layout)
            fig.update_xaxes(title_text="$\delta^{18}O (VSMOW ‰)$")
            fig.update_yaxes(title_text="Frequency", range=[0, 50])
            fig.update_yaxes(title_text="Frequency")
            fig.show()

        else:
            filtered_df_1 = datasetinformation_df[(datasetinformation_df['Department'] == department) &
                                                  (datasetinformation_df['Sample_Type'] == sample_type) &
                                                  (datasetinformation_df['ID'] == ID)]

            # Crear serie temporal
            layout = go.Layout(title="Temporal Series of &#948;<sup>18</sup>O")
            temporal_series_1 = go.Scatter(x=filtered_df_1['Sample_Collection_Date'], y=filtered_df_1['O18'],
                                           mode='markers', marker=dict(size=12, color='pink', line=dict(width=2,color='black')),
                                           name='Series 1')
            fig = go.Figure(data=temporal_series_1, layout=layout)
            fig.update_xaxes(title_text="Sample Collection Date", title_standoff=16)
            fig.update_yaxes(title_text="$\delta^{18}O (VSMOW ‰)$", title_standoff=16, autorange="reversed")
            fig.show()

    def update_sample_type_dropdown(*args):
        department = department_dropdown.value
        sample_type_dropdown.options =  datasetinformation_df[datasetinformation_df['Department'] == department]['Sample_Type'].unique().tolist()


    def update_id_dropdown(*args):
        department = department_dropdown.value
        sample_type = sample_type_dropdown.value
        id_dropdown.options = ['All'] + datasetinformation_df[(datasetinformation_df['Department'] == department) &
                                                               (datasetinformation_df['Sample_Type'] == sample_type)]['ID'].unique().tolist()

    department_dropdown.observe(update_sample_type_dropdown, 'value')
    department_dropdown.observe(update_id_dropdown, 'value')
    sample_type_dropdown.observe(update_id_dropdown, 'value')

    return widgets.interactive(filter_dataframe, department=department_dropdown, sample_type=sample_type_dropdown, ID=id_dropdown)
