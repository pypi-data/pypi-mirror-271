import mysql.connector
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, HTML
import os

def download_dataset():
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

    def filter_and_show(department, sample_type, ID):
        if ID == 'All':
            filtered_df = datasetinformation_df[(datasetinformation_df['Department'] == department) &
                                                (datasetinformation_df['Sample_Type'] == sample_type)]
        else:
            filtered_df = datasetinformation_df[(datasetinformation_df['Department'] == department) &
                                                (datasetinformation_df['Sample_Type'] == sample_type) &
                                                (datasetinformation_df['ID'] == ID)]

        display(filtered_df)

    def download_data(button):
        department = department_dropdown.value
        sample_type = sample_type_dropdown.value
        ID = id_dropdown.value

        if ID == 'All':
            filtered_df = datasetinformation_df[(datasetinformation_df['Department'] == department) &
                                                (datasetinformation_df['Sample_Type'] == sample_type)]
        else:
            filtered_df = datasetinformation_df[(datasetinformation_df['Department'] == department) &
                                                (datasetinformation_df['Sample_Type'] == sample_type) &
                                                (datasetinformation_df['ID'] == ID)]

        current_directory = os.getcwd()
        file_name = "filtered_datasetinfo.xlsx"
        save_path = os.path.join(current_directory, file_name)

        with pd.ExcelWriter(save_path, engine='xlsxwriter') as writer:
            filtered_df.to_excel(writer, index=False, sheet_name='Filtered Data')

        print("Archivo guardado en:", save_path)

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

    download_button = widgets.Button(description="Download Excel")
    download_button.on_click(download_data)

    def update_sample_type_dropdown(*args):
        department = department_dropdown.value
        sample_type_dropdown.options = datasetinformation_df[datasetinformation_df['Department'] == department]['Sample_Type'].unique().tolist()

    def update_id_dropdown(*args):
        department = department_dropdown.value
        sample_type = sample_type_dropdown.value
        id_dropdown.options = ['All'] + datasetinformation_df[(datasetinformation_df['Department'] == department) &
                                                               (datasetinformation_df['Sample_Type'] == sample_type)]['ID'].unique().tolist()

    department_dropdown.observe(update_sample_type_dropdown, 'value')
    department_dropdown.observe(update_id_dropdown, 'value')
    sample_type_dropdown.observe(update_id_dropdown, 'value')

    display(widgets.interactive(filter_and_show, department=department_dropdown, sample_type=sample_type_dropdown, ID=id_dropdown))
    display(download_button)
