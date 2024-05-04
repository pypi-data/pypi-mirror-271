import mysql.connector
import pandas as pd
import ipywidgets as widgets
from IPython.display import display

def department_information():
    host = "sql12.freemysqlhosting.net"
    user = "sql12701694"
    password = "bbHGHD5bdi"
    database = "sql12701694"

    mydb = mysql.connector.connect(
         host=host,
         user=user,
         password=password,
         database=database
    )
    mycursor = mydb.cursor()
    mycursor.execute("SHOW TABLES")
    tab = mycursor.fetchall()
    
    datasets_stations = mycursor.execute("""SELECT * FROM siteinformation""")
    allstations = mycursor.fetchall()
    
    stations = pd.DataFrame(allstations, columns=['ID', 'Station', 'Latitude', 'Longitude', 'Altitude', 'Department', 'Start_Date',
                                  'End_Date', 'Sampling_Frequency', 'Sample_Type', 'Number_of_O18_data',
                                  'Number_of_D_data', 'Number_of_O17_data', 'O18_analytical_precision',
                                  'D_analytical_precision', 'O17_analytical_precision', 'Contact', 'Contact_Email',
                                  'References', 'Database'])

    consulta = "SELECT Department, Sample_Type, ID, Number_of_O18_data, Number_of_O17_data, Sampling_Frequency FROM siteinformation GROUP BY Department, Sample_Type, ID, Number_of_O18_data, Number_of_O17_data, Sampling_Frequency"
    mycursor.execute(consulta)
    results_site = mycursor.fetchall()

    data = {
        'Department': [],
        'Sample_Type': [],
        'ID': [],
        'Number_of_O18_d2H_dataset': [],
        'Number_of_O17_data': [],
        'Sampling_frequency': []
    }

    for department, sample_type, ID, dataset_d18o, dataset_d17o, sampling_frequency in results_site:
        data['Department'].append(department)
        data['Sample_Type'].append(sample_type)
        data['ID'].append(ID)
        data['Number_of_O18_d2H_dataset'].append(dataset_d18o)
        data['Number_of_O17_data'].append(dataset_d17o)
        data['Sampling_frequency'].append(sampling_frequency)

    siteinformation_df = pd.DataFrame(data)

    database_column = stations['Database']
    database_df = pd.DataFrame({'Database': database_column, 'ID': stations['ID']})
    database_df = database_df.drop_duplicates(subset='ID')
    siteinformation_df = pd.merge(siteinformation_df, database_df, on='ID', how='left')

    department_dropdown = widgets.Dropdown(
        options=siteinformation_df['Department'].unique().tolist(),
        description='Search Department:'
    )

    def filter_dataframe(department):
        filtered_df = siteinformation_df[siteinformation_df['Department'] == department]
        display(filtered_df)

    interact = widgets.interactive(filter_dataframe, department=department_dropdown)

    return interact
