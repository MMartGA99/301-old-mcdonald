import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output, State

########### Define your variables ######

# here's the list of possible columns to choose from.
list_of_columns =['total exports', 'beef', 'pork', 'poultry',
       'dairy', 'fruits fresh', 'fruits proc', 'total fruits', 'veggies fresh',
       'veggies proc', 'total veggies', 'corn', 'wheat', 'cotton']

#mycolumn='beef'
#myheading1 = f"Wow! That's a lot of {mycolumn}!"
#mygraphtitle = '2011 US Agriculture Exports by State'  --moved inside function
#mycolorscale = 'ylorrd' # Note: The error message will list possible color scales. --moved inside function
#mycolorbartitle = "Millions USD" --moved inside function
tabtitle = 'Old McDonald'
sourceurl = 'https://plot.ly/python/choropleth-maps/'
githublink = 'https://github.com/MMartGA99/301-old-mcdonald'


########## Set up the chart

import pandas as pd
df = pd.read_csv('assets/usa-2011-agriculture.csv')



########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout

app.layout = html.Div(children=[
    html.H1(id='my-heading',),
    #html.H1(f"test title"),
    html.Div([        
        html.Div([
                html.Label('Select A Variable:'),              
                dcc.Dropdown(
                    id='your_input_here',
                    options=[{"label":x, "value":x} for x in list_of_columns],              
                    value='beef',
                    style={'width': '48%'}
                    ),   
        ], className='two columns'),
        html.Div([
            dcc.Graph(id='figure-1')], 
            className = 'ten columns'),
                 ], className = 'twelve columns'),
    
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)


########## Define Callback -- NEW
@app.callback([Output('figure-1', 'figure'),
               #This second output is linked to, and updates html.H1
               Output('my-heading', 'children')],
              [Input('your_input_here', 'value')])
def radio_results(value_you_chose):
    #return html.Img(src=app.get_asset_url(image_you_chose), style={'width': 'auto', 'height': '50%'}),
    mygraphtitle = f'2011 US Agriculture Exports by {value_you_chose}'
    mycolorscale = "Cividis"  #'ylorrd' # Note: The error message will list possible color scales.
    mycolorbartitle = "Millions USD"
    
    fig = go.Figure(data=go.Choropleth(
        locations=df['code'], # Spatial coordinates
        z = df[value_you_chose].astype(float), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = mycolorscale,
        colorbar_title = mycolorbartitle,
    ))

    fig.update_layout(
        title_text = mygraphtitle,
        geo_scope='usa',
        width=1200,
        height=800
    )
    
      
    #The items returned are mapped, in order, to each output list in your @app.callback function
    return fig, f"{value_you_chose.title()} Exports Across the U.S.!"

############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)