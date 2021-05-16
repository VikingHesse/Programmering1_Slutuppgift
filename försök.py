import plotly.express as px 
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd 
import numpy as np
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

#genererar data
genderdata = pd.read_csv("Gender_Data.csv", encoding="ISO-8859-1", header=0)
dagligadödsfall = pd.read_csv("National_Daily_Deaths.csv", encoding="ISO-8859-1", header=0)
veckodata = pd.read_csv("Municipality_Weekly_Data.csv", encoding="UTF-8", header=0)
gbgdata = veckodata[veckodata["Municipality"].str.contains("Göteborg")]
åldersdata = pd.read_csv("National_Total_Deaths_by_Age_Group.csv", encoding="UTF-8", header=0)
regiondailydata = pd.read_csv("Regional_Daily_Cases.csv", encoding="UTF-8", header=0)
regiontotaldata = pd.read_csv("Regional_Totals_Data.csv", encoding="UTF-8", header=0)

#skapa figs
genderdata_graf = px.pie(genderdata, values='Total_Deaths', names='Gender', title='Antalet dödsfall män kontra kvinnor', height=700)
dagligadödsfall_graf = px.bar(dagligadödsfall, x="Date", y="National_Daily_Deaths", title="Antalet döda i COVID per dag", height=700)
gbgdata_graf = px.bar(gbgdata, x="Municipality", y="Weekly_Cases_per_100k_Pop", color="Municipality", animation_frame="Week_Number", animation_group="Municipality", range_y=[0,75], title="Antalet fall i Göteborg per 100k veckorna 1-53 2020", height=700)
åldersdata_graf = px.pie(åldersdata, values="Total_Cases", names="Age_Group", title="Totala fall", height=700)
regiondata_graf = px.line(regiondailydata, x="Date", y="Västra_Götaland", title="Antalet döda i COVID per dag i Västra Götaland", height=700)
regiontotaldata_graf = px.scatter(regiontotaldata, x="Total_Deaths", y="Total_ICU_Admissions", color="Region", size="Total_Cases",title="Totala dödsfall samt IVA fall för varje region", height=700)

#flyttar slidern på göteborgsgrafen
gbgdata_graf['layout']['sliders'][0]['pad']=dict(r= 10, t= 150,)

# utseendet
app.layout = html.Div(children=[

    html.Div(className="box",children=[
        html.H1("GRAF 1", className="H1"),


        dcc.Graph(
            id="gendergraf",
            figure=genderdata_graf,
        ),
    ]),

    html.Div(className="box",children=[
        html.H1("GRAF 2", className="H1"),
        


        dcc.Graph(
            id="dagligadödsfallgraf",
            figure=dagligadödsfall_graf,
        ),
    ]),

    html.Div(className="box",children=[
        html.H1("GRAF 3", className="H1"),


        dcc.Graph(
            id="gbgdatagraf",
            figure=gbgdata_graf,
        ),
    ]),

    html.Div(className="box",children=[
        html.H1("GRAF 4", className="H1"),

        dcc.Dropdown(
            id = "drop",
            options = [dict(label = "Totala fall", value="Totala fall"), dict(label = "Totala dödsfall", value="Totala dödsfall"), dict(label = "Totala IVA fall", value="Totala IVA fall")],
            value = "Totala fall"
        ),
        
        dcc.Graph(
            id="åldersgraf",
            figure=åldersdata_graf,
        ),
    ]),
    
    html.Div(className="box",children=[
        html.H1("GRAF 5", className="H1"),


        dcc.Graph(
            id="regiongraf",
            figure=regiondata_graf,
        ),
    ]),

    html.Div(className="box",children=[
        html.H1("GRAF 6", className="H1"),


        dcc.Graph(
            id="regiontotaldatagraf",
            figure=regiontotaldata_graf,
        ),
    ]),

])


@app.callback(
    Output("åldersgraf", "figure"),
    [Input("drop", "value")]
)

def update_figure(value):

    if value == "Totala fall":  värden = "Total_Cases"
    elif value == "Totala dödsfall": värden = "Total_Deaths"
    elif value == "Totala IVA fall": värden = "Total_ICU_Admissions"

    åldersdata_graf = px.pie(åldersdata, values=värden, names="Age_Group", title=f"{value} i de olika åldersgrupperna", height=700)
    åldersdata_graf.update_layout(transition_duration=500)
    return åldersdata_graf


if __name__ == "__main__":
    app.run_server(debug = True)