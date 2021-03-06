#Importerar diverse libraries
import plotly.express as px 
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd 
import numpy as np
from dash.dependencies import Input, Output

#initierar dash
app = dash.Dash(__name__)

#genererar data
genderdata = pd.read_csv("Gender_Data.csv", encoding="ISO-8859-1", header=0)
dagligadödsfall = pd.read_csv("National_Daily_Deaths.csv", encoding="ISO-8859-1", header=0)
veckodata = pd.read_csv("Municipality_Weekly_Data.csv", encoding="UTF-8", header=0)
gbgdata = veckodata[veckodata["Municipality"].str.contains("Göteborg")]
åldersdata = pd.read_csv("National_Total_Deaths_by_Age_Group.csv", encoding="UTF-8", header=0)
regiondailydata = pd.read_csv("Regional_Daily_Cases.csv", encoding="UTF-8", header=0)
regiontotaldata = pd.read_csv("Regional_Totals_Data.csv", encoding="UTF-8", header=0)

region_koordinater = pd.read_csv("regionkoordinater.csv", encoding="UTF-8", header=0)
regiontotaldata_koordinater = regiontotaldata.merge(region_koordinater)

#skapar figures
genderdata_graf = px.pie(genderdata, values='Total_Deaths', names='Gender', color="Gender", title='Antalet dödsfall män kontra kvinnor', height=700,
labels=dict(Gender="Kön", Total_Deaths="Totala dödsfall"))

dagligadödsfall_graf = px.bar(dagligadödsfall, x="Date", y="National_Daily_Deaths", title="Antalet döda i COVID per dag", height=700, 
labels=dict(Date="Datum", National_Daily_Deaths="Antalet döda"))

gbgdata_graf = px.bar(gbgdata, x="Municipality", y="Weekly_Cases_per_100k_Pop", color="Municipality", animation_frame="Week_Number", animation_group="Municipality", range_y=[0,75], title="Antalet fall i Göteborg per 100k veckorna 1-53 2020", height=700, 
labels=dict(Municipality="Stadsdel", Weekly_Cases_per_100k_Pop="Veckofall per 100k", Week_Number="Vecka"))

åldersdata_graf = px.pie(åldersdata, values="Total_Cases", names="Age_Group", title="Totala fall", height=700)

regiondata_graf = px.line(regiondailydata, x="Date", y="Västra_Götaland", title="Antalet döda i COVID per dag i Västra Götaland", height=700,
labels=dict(Västra_Götaland="Antal fall", Date="Datum"))

regiontotaldata_graf = px.scatter(regiontotaldata, x="Total_Deaths", y="Total_ICU_Admissions", color="Region", size="Total_Cases",title="Totala dödsfall samt IVA fall för varje region", height=700, hover_name="Region",
labels=dict(Total_Deaths="Totala dödsfall", Total_ICU_Admissions="Totala IVA fall", Total_Cases="Totala fall"))

regionkarta_graf = px.scatter_geo(regiontotaldata_koordinater, lat="lat", lon="lon", color="Region", scope="europe", size="Total_Cases", hover_name="Region", size_max=25, fitbounds="locations", height=700,
labels=dict(Total_Cases="Totala fall"))

#flyttar slidern på göteborgsgrafen
gbgdata_graf['layout']['sliders'][0]['pad']=dict(r= 10, t= 150)

#utseendet, fungerar som HTML
app.layout = html.Div(children=[

    #gör en div som får klassen "box", denna klassen har jag ändrat css på i ett annat dokument som heter div.css
    #diven får children H1 (som titel, med klassen H1) samt dash component graph som får figure värdet "genderdata_graf" vilket visar grafen. Detta är samma för resterande divs
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

        #Här görs en dropdown vilket får id drop, options som bestämmer vilka val samt värden valen ska ha och value vilket innebär värdet som dropdownmenyn ska ha från början.
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

    html.Div(className="box",children=[
        html.H1("GRAF 7", className="H1"),


        dcc.Graph(
            id="regionkartagraf",
            figure=regionkarta_graf,
        ),
    ]),

])

#Bestämmer output och input, output blir åldersgraf o figure i detta fall. Input blir drop och value
@app.callback(
    Output("åldersgraf", "figure"),
    [Input("drop", "value")]
)

#Skapar en funktion som uppdaterar graf 4 utefter dropdown values. Om man väljer någon av alternativen i dropdown så ändras "values" i pie charten. 
def update_figure(value):

    if value == "Totala fall":  värden = "Total_Cases"
    elif value == "Totala dödsfall": värden = "Total_Deaths"
    elif value == "Totala IVA fall": värden = "Total_ICU_Admissions"

    åldersdata_graf = px.pie(åldersdata, values=värden, names="Age_Group", title=f"{value} i de olika åldersgrupperna", height=700,
    labels=dict(Age_Group="Åldersgrupp"))
    åldersdata_graf.update_layout(transition_duration=500)
    return åldersdata_graf

#Kör dash på local server
if __name__ == "__main__":
    app.run_server(debug = True)