import dash
from dash import html
from dash import dcc,dash_table
from dash import dash_table as dt
# import dash_html_components as ht
# import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
#import dash_table as dt


election = pd.read_csv("1976-2020-president.csv")
election["candidate"] = election["candidate"].str.replace(",","",).astype(object)
election.dropna(subset=['party_detailed'], inplace=True)
election.dropna(subset=['candidate'], inplace=True)





senate=pd.read_csv("1976-2020-senate.csv",encoding='ISO-8859-1')

df_president_candidates_party = election[["candidatevotes", "party_detailed"]]


df_goals_per_position_sum = df_president_candidates_party.groupby(
    ["party_detailed"]).sum().reset_index(drop=False)

#viz 1
df = px.data.tips()
fig_number_votes_per_party_historic = px.treemap(df_goals_per_position_sum,
                                                 path=[px.Constant(
                                                     "all"), 'party_detailed'],
                                                 values='candidatevotes',
                                                 title="  The number of votes per party historic during all the times.")

fig_number_votes_per_party_historic.update_traces(root_color="lightgrey")
fig_number_votes_per_party_historic.update_layout(
    margin=dict(t=50, l=25, r=25, b=25))

# fig_number_votes_per_party_historic.show()


# ---------------------
# Viz 2: The number of votes per party is detailed historic during all the times WITHOUT REPUBLICAN NOR DEMOCRAT
# ---------------------
df_president_candidates_party_witout_demo_replu = df_president_candidates_party

df_president_candidates_party_witout_demo_replu.drop(
    df_president_candidates_party_witout_demo_replu.loc[df_president_candidates_party_witout_demo_replu['party_detailed'] == "DEMOCRAT"].index, inplace=True)
df_president_candidates_party_witout_demo_replu.drop(
    df_president_candidates_party_witout_demo_replu.loc[df_president_candidates_party_witout_demo_replu['party_detailed'] == "REPUBLICAN"].index, inplace=True)


df_president_candidates_party_witout_demo_replu = df_president_candidates_party_witout_demo_replu.groupby(
    ["party_detailed"]).sum().reset_index(drop=False)


df = px.data.tips()
fig_number_votes_per_party_historic_witout_demo_replu = px.treemap(df_president_candidates_party_witout_demo_replu,
                                                                   path=[px.Constant(
                                                                       "all"), 'party_detailed'],
                                                                   values='candidatevotes',
                                                                   title="this treemap visualization is used  to identify patterns for  The number of votes per party historic during all the times.")

fig_number_votes_per_party_historic_witout_demo_replu.update_traces(
    root_color="lightgrey")
fig_number_votes_per_party_historic_witout_demo_replu.update_layout(
    margin=dict(t=50, l=25, r=25, b=25))

# fig_number_votes_per_party_historic_witout_demo_replu.show()


# ---------------------
# VIZ 3: Show per state in all years which states are the most votes if republican or Democratic (in a map).
#        All the years show the states that have more republican or democrat Ed in history.
# ---------------------

df_president_candidates_party = election[[
    "year", "state_po", "party_detailed", "candidatevotes"]]


df_president_candidates_party_max = df_president_candidates_party.groupby(
    ["year", "state_po"], sort=False)["candidatevotes"].max().reset_index(drop=False)


df_president_candidates_party_max_merge = pd.merge(df_president_candidates_party, df_president_candidates_party_max,  how='inner', left_on=[
                                                   'year', 'state_po', 'candidatevotes'], right_on=['year', 'state_po', 'candidatevotes'])


# ---------------------
# VIZ 4: Show the percentage of votes from each party for the past years.
#        Graph that on the x-axis have democrat, republicans and other.
#        Each of those groups by year.
#        On the y axis is the number of votes.
# ---------------------
df_president_per_party_past_years = election[[
    "year", "party_simplified", "candidatevotes"]]

df_president_per_party_past_years_sum = df_president_per_party_past_years.groupby(
    ["year", "party_simplified"]).sum().reset_index(drop=False)


wide_df = px.data.medals_wide()
fig_president_per_party_past_years_sum = px.bar(df_president_per_party_past_years_sum,
                                                x="year",
                                                y="candidatevotes",
                                                color="party_simplified",
                                                title="Total votes per most representative parties for the period 1975 - 2020")

# fig_president_per_party_past_years_sum.show()


# ---------------------
# VIZ 5: Show the name of the last 10 presidents show their names and show the number of votes they had to win.
# ---------------------

df_president_names_and_percentage = election[[
    "year", "candidate", "party_detailed", "candidatevotes"]]


df_president_names_and_percentage_new = df_president_names_and_percentage.groupby(
    ["year", "party_detailed", "candidate"]).sum().reset_index(drop=False)

df_president_names_and_percentage_new_max = df_president_names_and_percentage_new.groupby(
    ["year"], sort=False)["candidatevotes"].max().reset_index(drop=False)


df_president_names_and_percentage_new_max_merge1 = pd.merge(df_president_names_and_percentage_new_max, df_president_names_and_percentage_new,  how='inner', left_on=[
    'year', 'candidatevotes'], right_on=['year', 'candidatevotes'])


fig_df_president_names_and_percentage_new_max_merge1 = go.Figure(data=[go.Table(
    header=dict(values=list(df_president_names_and_percentage_new_max_merge1.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df_president_names_and_percentage_new_max_merge1.year,
                       df_president_names_and_percentage_new_max_merge1.candidatevotes,
                       df_president_names_and_percentage_new_max_merge1.party_detailed,
                       df_president_names_and_percentage_new_max_merge1.candidate],
               fill_color='lavender',
               align='left'))
])


#---------------------
#Viz 1: 6. The number of votes per party is detailed historic during all the times.
#---------------------


df_senate_candidates_party = senate[["candidatevotes", "party_detailed"]]

df_senate_candidates_party_sum = df_senate_candidates_party.groupby(
    ["party_detailed"]).sum().reset_index(drop=False)


df = px.data.tips()
fig_senate_candidates_party_sum_all = px.treemap(df_senate_candidates_party_sum,
                                                 path=[px.Constant(
                                                     "all"), 'party_detailed'],
                                                 values='candidatevotes',
                                                 title="The number of votes per party is detailed historic during all the times.")

fig_senate_candidates_party_sum_all.update_traces(root_color="lightgrey")
fig_senate_candidates_party_sum_all.update_layout(
    margin=dict(t=50, l=25, r=25, b=25))
# fig_senate_candidates_party_sum_all.show()


# ---------------------
# Viz 7: The number of votes per party is detailed historic during all the times WITHOUT REPUBLICAN NOR DEMOCRAT for the senate
# ---------------------
df_senate_candidates_party_repli = df_senate_candidates_party

df_senate_candidates_party_repli.drop(
    df_senate_candidates_party_repli.loc[df_senate_candidates_party_repli['party_detailed'] == "DEMOCRAT"].index, inplace=True)
df_senate_candidates_party_repli.drop(
    df_senate_candidates_party_repli.loc[df_senate_candidates_party_repli['party_detailed'] == "REPUBLICAN"].index, inplace=True)


df_senate_candidates_party_repli_group = df_senate_candidates_party_repli.groupby(
    ["party_detailed"]).sum().reset_index(drop=False)


df = px.data.tips()
fig_senate_number_votes_per_party_historic_witout = px.treemap(df_senate_candidates_party_repli_group,
                                                               path=[px.Constant(
                                                                   "all"), 'party_detailed'],
                                                               values='candidatevotes',
                                                               title="The number of votes for senate-elections per party is detailed historic during all the times.")

fig_senate_number_votes_per_party_historic_witout.update_traces(
    root_color="lightgrey")
fig_senate_number_votes_per_party_historic_witout.update_layout(
    margin=dict(t=50, l=25, r=25, b=25))
# fig_senate_number_votes_per_party_historic_witout.show()


# ---------------------
# VIZ 8: Show per state in all years which states are the most votes if republican or Democratic (in a map).
#        All the years show the states that have more republican or democrat Ed in history.
# ---------------------

df_senate_candidates_party = senate[[
    "year", "state_po", "party_detailed", "candidatevotes"]]


df_senate_candidates_party_max = df_senate_candidates_party.groupby(
    ["year", "state_po"], sort=False)["candidatevotes"].max().reset_index(drop=False)


df_senate_candidates_party_max_merge = pd.merge(df_senate_candidates_party, df_senate_candidates_party_max,  how='inner', left_on=[
    'year', 'state_po', 'candidatevotes'], right_on=['year', 'state_po', 'candidatevotes'])


# ---------------------
# VIZ 9: Show the percentage of votes from each party for the past years on the senate.
#        Graph that on the x-axis have democrat, republicans and other.
#        Each of those groups by year.
#        On the y axis is the number of votes.
# ---------------------
df_senate_per_party_past_years = senate[[
    "year", "party_simplified", "candidatevotes"]]

df_senate_per_party_past_years_sum = df_senate_per_party_past_years.groupby(
    ["year", "party_simplified"]).sum().reset_index(drop=False)


wide_df = px.data.medals_wide()
fig_senate_per_party_past_years_sum = px.bar(df_senate_per_party_past_years_sum,
                                             x="year",
                                             y="candidatevotes",
                                             color="party_simplified",
                                             title="Total votes of senate-elections per most representative parties for the period 1975 - 2020")

# fig_president_per_party_past_years_sum.show()


# ---------------------
# VIZ 10:  Show the name of the senate show their names and show the number of votes they had to win.
# ---------------------

df_senate_names_and_percentage = senate[[
    "year", "candidate", "party_detailed", "candidatevotes"]]


df_senate_names_and_percentage_new = df_senate_names_and_percentage.groupby(
    ["year", "party_detailed", "candidate"]).sum().reset_index(drop=False)

df_senate_names_and_percentage_new_max = df_senate_names_and_percentage_new.groupby(
    ["year"], sort=False)["candidatevotes"].max().reset_index(drop=False)


df_senate_names_and_percentage_new_max_merge1 = pd.merge(df_senate_names_and_percentage_new_max, df_senate_names_and_percentage_new,  how='inner', left_on=[
    'year', 'candidatevotes'], right_on=['year', 'candidatevotes'])




























external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout=html.Div([

    html.Div([
      html.Img(src=app.get_asset_url('USA-flag-660x345.png'),
             style={'height': '40px'},
             className='title_image'),
      html.H6("US ELECTIONS 1976-2020 ",
            style={'color':'red'},
            className='title'),

        ],className= 'logo_title'),


     html.Div([
         html.P('Select Year:', className='fix_label', style={'color': 'white', 'margin-left': '1%'}),
         dcc.Slider(
             id='select_years',
             included=False,
             updatemode='drag',
             tooltip={'always_visible':True},
             step=1,
             value=2008,
             #dots=False,
             #value=[(1972,2020)],
             marks={yr: str(yr) for yr in election['year'] },
             className='dcc_coupon'
         ),


    ], className="one-half column", id="title2"),


html.Div([
    html.Div([
              html.P('Select State:', className='fix_label',  style={'color': 'white'}),

                     dcc.Dropdown(id='w_countries',
                                  multi=False,
                                  clearable=True,
                                  disabled=False,
                                  style = {'display': True},
                                  value='ALABAMA',
                                  placeholder='State',
                                  options=[{'label': c, 'value': c}
                                           for c in (election['state'].unique())], className='dcc_compon'),

               html.P('Select party:', className='fix_label', style={'color': 'red'}),

                  dcc.Dropdown(id='party',
                     multi=False,
                      clearable=True,
                      disabled=False,
                     style={'display': True},
                     #value='DEMOCRAT',
                      placeholder='State',
                      options=[], className='dcc_compon'),

             ],className = "create_container four columns"),

html.Div([
    dcc.Graph(id='bar_chart1',
                  config={'displayModeBar': 'hover'}, style={'height': '350px'})
],className='create_container six columns'),

 html.Div([
             dcc.Graph(id = 'line_chat',
                       config = {'displayModeBar': 'hover'}),

         ], className = 'create_container2 six columns'),




html.Div([
dcc.Graph(
        id='fig_number_votes_per_party_historic_witout_demo_replu',
        figure=fig_number_votes_per_party_historic_witout_demo_replu)
   ], ),


html.Div([
   dcc.Graph( id='fig_number_votes_per_party_historic',
              figure=fig_number_votes_per_party_historic)
    ], className='create_container2 six columns' ),



html.Div([
dcc.Graph(
        id='fig_president_per_party_past_years_sum',
        figure=fig_president_per_party_past_years_sum)
 ], className='create_container2 six columns' ),

html.Div([

    dash_table.DataTable(
        df_president_names_and_percentage_new_max_merge1.to_dict(
            'records'), [{"name": i, "id": i}
                         for i in df_president_names_and_percentage_new_max_merge1.columns
                         ]),

], className='create_container2 six columns' ),


html.Div([
        html.H4('Polotical candidate voting pool analysis',className='fix_label',  style={'color': 'white'}),
        html.P("Select a candidate:",className='fix_label',  style={'color': 'red'}),
        dcc.RadioItems(
            id='year_change_1',
            options=df_president_candidates_party_max_merge["year"].unique(),
            value="2020",
            inline=True
        ),
        dcc.Graph(id="graph_map"),
    ]),

html.Div([
dcc.Graph(
        id='fig_senate_candidates_party_sum_all',
        figure=fig_senate_candidates_party_sum_all
    ),
], className='create_container2 six columns' ),

html.Div([
    dcc.Graph(
        id='fig_senate_number_votes_per_party_historic_witout',
        figure=fig_senate_number_votes_per_party_historic_witout
    ),
], className='create_container2 six columns' ),

html.Div([
        html.Div(id='text1'),
        html.Div(id='text2'),
        html.Div(id='text3'),
], className = 'create_container2 two columns', style = {'width': '260px'}),


    html.Div([
        html.H4('Polotical candidate voting pool analysis for senate_candidates',className='fix_label',  style={'color': 'white'}),
        html.P("Select a year:",className='fix_label',  style={'color': 'red'}),
        dcc.RadioItems(
            id='year_change_2',
            options=df_senate_candidates_party_max_merge["year"].unique(),
            value="1976",
            inline=True
        ),
        dcc.Graph(id="graph_map_senate"),
    ]),
html.Div([
    dcc.Graph(
        id='fig_senate_per_party_past_years_sum',
        figure=fig_senate_per_party_past_years_sum),
], className='create_container2 six columns' ),


html.Div([
    dash_table.DataTable(
        df_senate_names_and_percentage_new_max_merge1.to_dict(
            'records'), [{"name": i, "id": i}
                         for i in df_senate_names_and_percentage_new_max_merge1.columns
                         ]),

], className='create_container2 six columns' ),

],)
], id="mainContainer", style={"display": "flex", "flex-direction": "column"})









@app.callback(
    Output('party', 'options'),
    Input('w_countries', 'value')
 )

def update_country(w_countries):
    elect=election[election['state']==w_countries]
    return [{'label':i, 'value':i} for i in elect['party_detailed'].unique()]
    #return {'party': {'options': [{'label': i, 'value': i} for i in elect['party_detailed'].unique() ]}}
@app.callback(
        Output('party', 'value'),
        Input('party', 'options'))
def get_country_value(party):
     return [k['value'] for k in party][1]



@app.callback(Output('bar_chart1', 'figure'),

              [Input('select_years', 'value')])
def update_graph( select_years):

    election9 = election.groupby(['year', 'state', 'candidate'])['totalvotes'].sum().reset_index()
    best_candidates = election9[(election9['year'] == select_years)].sort_values(by=['totalvotes'], ascending=False).nlargest(5,
                                                                                                                 columns=[
                                                                                                                     'totalvotes'])

    fig = px.bar(
        best_candidates,
        x='candidate',
        y='totalvotes',
        title='best candidates in presidency elections for  each year',color="candidate"
    )


    return fig






    @app.callback(
        Output('text3', 'children'),
        [Input('select_years', 'value')])
    def update_text(select_years):
        election11 = election.groupby(['year'])['totalvotes'].sum().reset_index()
        current_year = election11[(election11['year'] == select_years)]['totalvotes'].sum()

        return [
            html.H6(children='Current Year',
                    style={'textAlign': 'center',
                           'color': 'red'}
                    ),

            html.P('${0:,.2f}'.format(current_year),
                   style={'textAlign': 'center',
                          'color': '#19AAE1',
                          'fontSize': 15,
                          'margin-top': '-10px'
                          }
                   ),
        ]





@app.callback(Output('line_chat', 'figure'),
              #[Input('select_years', 'value')],
              [Input('select_years', 'value')])

def update_graph( select_years):

    election9 = election.groupby(['year', 'state', 'candidate'])['totalvotes'].sum().reset_index()
    election3 = election9[(election9['year'] == select_years)].sort_values(by=['totalvotes'], ascending=False).nlargest(5,
                                                                                                                 columns=[
                                                                                                                     'totalvotes'])


    fig = px.line(
        election3,
        x='candidate',
        y='totalvotes',
        title=' best candidates in presidency elections for  each year '
    )

    return fig


    @app.callback(
        Output("graph_map", "figure"),
        Input("year_change_1", "value"))
    def display_choropleth(input_value):
        df_president_candidates_party_max_merge_to_show_2 = df_president_candidates_party_max_merge.copy()

        df_president_candidates_party_max_merge_to_show_2.drop(
            df_president_candidates_party_max_merge_to_show_2.loc[
                df_president_candidates_party_max_merge_to_show_2['year'] != int(input_value)].index, inplace=True)

        fig = px.choropleth(locations=df_president_candidates_party_max_merge_to_show_2["state_po"],
                            locationmode="USA-states",
                            color=df_president_candidates_party_max_merge_to_show_2["party_detailed"],
                            scope="usa")
        return fig

    @app.callback(
        Output("graph_map", "figure"),
        Input("year_change_1", "value"))
    def display_choropleth(input_value):
        df_president_candidates_party_max_merge_to_show_2 = df_president_candidates_party_max_merge.copy()

        df_president_candidates_party_max_merge_to_show_2.drop(
            df_president_candidates_party_max_merge_to_show_2.loc[
                df_president_candidates_party_max_merge_to_show_2['year'] != int(input_value)].index, inplace=True)

        fig = px.choropleth(locations=df_president_candidates_party_max_merge_to_show_2["state_po"],
                            locationmode="USA-states",
                            color=df_president_candidates_party_max_merge_to_show_2["party_detailed"],
                            scope="usa")
        return fig

@app.callback(
    Output("graph_map_senate", "figure"),
    Input("year_change_2", "value"))
def display_choropleth(input_value):
    df_senate_candidates_party_max_merge_2 = df_senate_candidates_party_max_merge.copy()

    print(df_senate_candidates_party_max_merge["year"].unique())
    print(input_value)
    df_senate_candidates_party_max_merge_2.drop(
        df_senate_candidates_party_max_merge_2.loc[df_senate_candidates_party_max_merge_2['year'] != int(input_value)].index, inplace=True)

    print(df_senate_candidates_party_max_merge_2)

    fig = px.choropleth(locations=df_senate_candidates_party_max_merge_2["state_po"],
                        locationmode="USA-states",
                        color=df_senate_candidates_party_max_merge_2["party_detailed"],
                        scope="usa")
    return fig

if __name__ == '__main__':
    app.run_server(debug =True)

