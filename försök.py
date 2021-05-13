import plotly.express as px 
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd 
import numpy as np
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# genererar data
genderdata = pd.read_csv("Gender_Data.csv", encoding="ISO-8859-1", header=0)
dagligadödsfall = pd.read_csv("National_Daily_Deaths.csv", encoding="ISO-8859-1", header=0)
veckodata = pd.read_csv("Municipality_Weekly_Data.csv", encoding="UTF-8", header=0)
gbgdata = veckodata[veckodata["Municipality"].str.contains("Göteborg")]

# skapa figs
fig = px.pie(genderdata, values='Total_Deaths', names='Gender', title='Antalet dödsfall män kontra kvinnor')
fig2 = px.bar(dagligadödsfall, x="Date", y="National_Daily_Deaths", title="Antalet döda i COVID per dag")
fig3 = px.bar(gbgdata, x="Municipality", y="Weekly_Cases_per_100k_Pop", color="Municipality", animation_frame="Week_Number", animation_group="Municipality", range_y=[0,75], title="Antalet fall i Göteborg per 100k veckorna 1-53 2020", height=700)

#flyttar slidern på fig 3
fig3['layout']['sliders'][0]['pad']=dict(r= 10, t= 150,)

# utseendet
app.layout = html.Div(children=[

    html.Div([
        html.H1(children = "COVID DATA GRAF 1"), 


        dcc.Graph(
            id="graph1",
            figure=fig,
        ),
    ]),

    html.Div([
        html.H1(children="COVID DATA GRAF 2"),


        dcc.Graph(
            id="graph2",
            figure=fig2,
        ),
    ]),

    html.Div([
        html.H1(children="COVID DATA GRAF 3"),


        dcc.Graph(
            id="graph3",
            figure=fig3,
        ),
    ]),
])




if __name__ == "__main__":
    app.run_server(debug = True)