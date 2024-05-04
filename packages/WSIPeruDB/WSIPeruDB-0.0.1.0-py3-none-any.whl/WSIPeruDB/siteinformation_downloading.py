import mysql.connector
import pandas as pd
import ipywidgets as widgets
import os

def download_site_information():
    mydb = mysql.connector.connect(
         host = "sql12.freemysqlhosting.net",
         user = "sql12701694",
         password = "bbHGHD5bdi",
         database = "sql12701694"
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

    siteinformation_df = pd.DataFrame(stations)

    def filter_and_show(department, sample_type, ID):
        if ID == 'All':
            filtered_df = siteinformation_df[(siteinformation_df['Department'] == department) &
                                             (siteinformation_df['Sample_Type'] == sample_type)]
        else:
            filtered_df = siteinformation_df[(siteinformation_df['Department'] == department) &
                                             (siteinformation_df['Sample_Type'] == sample_type) &
                                             (siteinformation_df['ID'] == ID)]

        display(filtered_df)

    def download_data(button):
        department = department_dropdown.value
        sample_type = sample_type_dropdown.value
        ID = id_dropdown.value

        if ID == 'All':
            filtered_df = siteinformation_df[(siteinformation_df['Department'] == department) &
                                             (siteinformation_df['Sample_Type'] == sample_type)]
        else:
            filtered_df = siteinformation_df[(siteinformation_df['Department'] == department) &
                                             (siteinformation_df['Sample_Type'] == sample_type) &
                                             (siteinformation_df['ID'] == ID)]

        current_directory = os.getcwd()
        file_name = "filtered_data_siteinfo.xlsx"
        save_path = os.path.join(current_directory, file_name)

        with pd.ExcelWriter(save_path, engine='xlsxwriter') as writer:
            filtered_df.to_excel(writer, index=False, sheet_name='Filtered Data')

        print("Archivo guardado en:", save_path)

    department_dropdown = widgets.Dropdown(
        options=siteinformation_df['Department'].unique().tolist(),
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
        sample_type_dropdown.options = siteinformation_df[siteinformation_df['Department'] == department]['Sample_Type'].unique().tolist()

    def update_id_dropdown(*args):
        department = department_dropdown.value
        sample_type = sample_type_dropdown.value
        id_dropdown.options = ['All'] + siteinformation_df[(siteinformation_df['Department'] == department) &
                                                           (siteinformation_df['Sample_Type'] == sample_type)]['ID'].unique().tolist()

    department_dropdown.observe(update_sample_type_dropdown, 'value')
    department_dropdown.observe(update_id_dropdown, 'value')
    sample_type_dropdown.observe(update_id_dropdown, 'value')

    display(widgets.interactive(filter_and_show, department=department_dropdown, sample_type=sample_type_dropdown, ID=id_dropdown))
    display(download_button)