import mysql.connector
import pandas as pd
import ipywidgets as widgets
from IPython.display import display
import plotly.express as px
import plotly.graph_objects as go

def plot_lmwl():
    mydb = mysql.connector.connect(
         host="sql12.freemysqlhosting.net",
         user="sql12701694",
         password="bbHGHD5bdi",
         database="sql12701694"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SHOW TABLES")
    tab = mycursor.fetchall()
    
    datasets = mycursor.execute("""SELECT * FROM datasetinformation""")
    alldata = mycursor.fetchall()
    
    isotopesdata = pd.DataFrame(alldata, columns=['ID','Sampling_Collection_Date','O18','D','Dxs','O17','Sample_Type','Department'])

    consulta_2 = "SELECT ID, Sample_Collection_Date, O18, D, Dxs, O17, Sample_Type, Department FROM datasetinformation GROUP BY ID, Sample_Collection_Date, O18, D, Dxs, O17, Sample_Type, Department"
    mycursor.execute(consulta_2)
    results_site_2 = mycursor.fetchall()

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
            filtered_df = datasetinformation_df[(datasetinformation_df['Department'] == department) &
                                                (datasetinformation_df['Sample_Type'] == sample_type)]
        else:
            filtered_df = datasetinformation_df[(datasetinformation_df['Department'] == department) &
                                                (datasetinformation_df['Sample_Type'] == sample_type) &
                                                (datasetinformation_df['ID'] == ID)]
        Oxy = filtered_df['O18'].values
        Hyd = filtered_df['D'].values
        Oxy = Oxy.reshape((-1,1))
        H_gmwl = 8 * Oxy + 10

        data = pd.DataFrame({'Oxy': Oxy.flatten(), 'Hyd': Hyd})

        if len(filtered_df) < 4:
            print("Exploratory analysis charts will not be generated due to insufficient data quantity")
            return

        fig = px.scatter(data, x="Oxy", y="Hyd", trendline="ols", title='Local Meteoric Water Line (LMWL)')
        fig.update_traces(marker=dict(size=12, color='pink', line=dict(width=1.5, color='black')), showlegend=True)
        fig.add_trace(go.Scatter(x=Oxy.flatten(), y=H_gmwl.flatten(), mode='lines', name=f'$\delta^{{2}}H = 8 \delta^{{18}}O + 10 $', line=dict(color='black')))
        model = px.get_trendline_results(fig)
        alpha = model.iloc[0]["px_fit_results"].params[0]
        beta = model.iloc[0]["px_fit_results"].params[1]
        std_dev = model.iloc[0]["px_fit_results"].bse[1]  # Desvi
        fig.update_layout(
        title='Local Meteoric Water Line (LMWL)',
        xaxis_title='$\delta^{18}O$ (VSMOW ‰)',
        yaxis_title='$\delta^{2}H$ (VSMOW ‰)',
        legend=dict(
            x=0.01,
            y=0.98,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color="black"
            ),
            bgcolor="LightSteelBlue",
            bordercolor="dimgray",
            borderwidth=2
        )
    )
        fig.data[0].name = 'Data'
        fig.data[0].showlegend = True
        fig.data[1].name = f'$\delta^{{2}}H = {round(beta, 2)}\delta^{{18}}O + {round(alpha, 2)}$'
        fig.data[1].showlegend = True
        fig.show()

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

    interact = widgets.interactive(filter_dataframe, department=department_dropdown, sample_type=sample_type_dropdown, ID=id_dropdown)

    return interact

