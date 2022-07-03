# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# FINAL PROJECT DATA VISUALITION
# BY:
#   JULIAN OLIVEROS FORERO
#   QUEEN


from gettext import translation
from logging import _STYLES
from tkinter.tix import COLUMN
from typing import Type
import plotly.graph_objects as go
from dash import dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# -----------------------------------
#   PART 1 -   load data (+arrange data)
# -----------------------------------

president = pd.read_csv("../data/1976-2020-president.csv")

senate = pd.read_csv("../data/1976_2020_senate.csv")


# -----------------------------------
#   PART 2 - Produces charts
# -----------------------------------

# DEMOCRATIC =blue
# Republican RED

# ---------------------
# Viz 1: 1. The number of votes per party is detailed historic during all the times.
# ---------------------

df_president_candidates_party = president[["candidatevotes", "party_detailed"]]


df_goals_per_position_sum = df_president_candidates_party.groupby(
    ["party_detailed"]).sum().reset_index(drop=False)


df_goals_per_position_sum.drop(
    df_goals_per_position_sum.loc[df_goals_per_position_sum['candidatevotes'] < 600000].index, inplace=True)


fig_number_votes_per_party_historic = px.pie(df_goals_per_position_sum,
                                             values='candidatevotes',
                                             names='party_detailed',
                                             color='party_detailed',
                                             color_discrete_map={
                                                 'REPUBLICAN': 'red',
                                                 'DEMOCRAT': 'blue',
                                                 'LIBERTARIAN': 'gold',
                                                 'REFORM PARTY': 'light-blue',
                                                 'INDEPENDENT': 'gray',
                                                 'OTHER': 'green',
                                                 'GREEN': 'green',
                                             })


# fig_number_votes_per_party_historic.show()


# ---------------------
# Viz 2: The number of votes per party is detailed historic during all the times WITHOUT REPUBLICAN NOR DEMOCRAT
# ---------------------
df_president_candidates_party_witout_demo_replu = president[[
    "candidatevotes", "party_detailed"]]

df_president_candidates_party_witout_demo_replu.drop(
    df_president_candidates_party_witout_demo_replu.loc[df_president_candidates_party_witout_demo_replu['party_detailed'] == "DEMOCRAT"].index, inplace=True)
df_president_candidates_party_witout_demo_replu.drop(
    df_president_candidates_party_witout_demo_replu.loc[df_president_candidates_party_witout_demo_replu['party_detailed'] == "REPUBLICAN"].index, inplace=True)


df_president_candidates_party_witout_demo_replu = df_president_candidates_party_witout_demo_replu.groupby(
    ["party_detailed"]).sum().reset_index(drop=False)


fig_number_votes_per_party_historic_witout_demo_replu = px.treemap(df_president_candidates_party_witout_demo_replu,
                                                                   path=[px.Constant(
                                                                       "all"), 'party_detailed'],
                                                                   values='candidatevotes',
                                                                   color='party_detailed',
                                                                   color_discrete_map={
                                                                       'REPUBLICAN': 'red',
                                                                       'DEMOCRAT': 'blue',
                                                                       'LIBERTARIAN': 'gold',
                                                                       'INDEPENDENT': 'gray',
                                                                       'REFORM PARTY': 'light-blue',
                                                                       'OTHER': 'green',
                                                                       'GREEN': 'green',
                                                                       '(?)': 'black',
                                                                   })


fig_number_votes_per_party_historic_witout_demo_replu.update_traces(
    root_color="lightgrey")
fig_number_votes_per_party_historic_witout_demo_replu.update_layout(
    margin=dict(t=50, l=25, r=25, b=25))

# fig_number_votes_per_party_historic_witout_demo_replu.show()


# ---------------------
# VIZ 3: Show per state in all years which states are the most votes if republican or Democratic (in a map).
#        All the years show the states that have more republican or democrat Ed in history.
# ---------------------

df_president_candidates_party = president[[
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


df_president_per_party_past_years = president[[
    "year", "party_simplified", "candidatevotes"]]

df_president_per_party_past_years_sum = df_president_per_party_past_years.groupby(
    ["year", "party_simplified"]).sum().reset_index(drop=False)


wide_df = px.data.medals_wide()
fig_president_per_party_past_years_sum = px.bar(df_president_per_party_past_years_sum,
                                                x="year",
                                                y="candidatevotes",
                                                color='party_simplified',
                                                color_discrete_map={
                                                    'REPUBLICAN': 'red',
                                                    'DEMOCRAT': 'blue',
                                                    'LIBERTARIAN': 'gold',
                                                    'REFORM PARTY': 'light-blue',
                                                    'INDEPENDENT': 'gray',
                                                    'OTHER': 'green',
                                                    'GREEN': 'green',
                                                },
                                                text="party_simplified")


# fig_president_per_party_past_years_sum.show()


# ---------------------
# VIZ 5: Show the name of the last 10 presidents show their names and show the number of votes they had to win.
# ---------------------

df_president_names_and_percentage = president[[
    "year", "candidate", "party_detailed", "candidatevotes"]]


df_president_names_and_percentage_new = df_president_names_and_percentage.groupby(
    ["year", "party_detailed", "candidate"]).sum().reset_index(drop=False)

df_president_names_and_percentage_new_max = df_president_names_and_percentage_new.groupby(
    ["year"], sort=False)["candidatevotes"].max().reset_index(drop=False)


df_president_names_and_percentage_new_max_merge1 = pd.merge(df_president_names_and_percentage_new_max, df_president_names_and_percentage_new,  how='inner', left_on=[
    'year', 'candidatevotes'], right_on=['year', 'candidatevotes'])


# ---------------------
# Viz 6. The number of votes per party is detailed historic during all the times.
# ---------------------


df_senate_candidates_party = senate[["candidatevotes", "party_detailed"]]

df_senate_candidates_party_sum = df_senate_candidates_party.groupby(
    ["party_detailed"]).sum().reset_index(drop=False)


df_senate_candidates_party_sum.drop(
    df_senate_candidates_party_sum.loc[df_senate_candidates_party_sum['candidatevotes'] < 1000000].index, inplace=True)


fig_senate_candidates_party_sum_all = px.pie(df_senate_candidates_party_sum,
                                             values='candidatevotes',
                                             names='party_detailed',
                                             color='party_detailed',
                                             color_discrete_map={
                                                 'REPUBLICAN': 'red',
                                                 'REFORM PARTY': 'light-blue',
                                                 'DEMOCRAT': 'blue',
                                                 'LIBERTARIAN': 'gold',
                                                 'INDEPENDENT': 'gray',
                                                 'OTHER': 'green',
                                                 'GREEN': 'green',
                                             })


# ---------------------
# Viz 7: The number of votes per party is detailed historic during all the times WITHOUT REPUBLICAN NOR DEMOCRAT for the senate
# ---------------------
df_senate_candidates_party_repli = senate[["candidatevotes", "party_detailed"]]

df_senate_candidates_party_repli.drop(
    df_senate_candidates_party_repli.loc[df_senate_candidates_party_repli['party_detailed'] == "DEMOCRAT"].index, inplace=True)
df_senate_candidates_party_repli.drop(
    df_senate_candidates_party_repli.loc[df_senate_candidates_party_repli['party_detailed'] == "REPUBLICAN"].index, inplace=True)


df_senate_candidates_party_repli_group = df_senate_candidates_party_repli.groupby(
    ["party_detailed"]).sum().reset_index(drop=False)


fig_senate_number_votes_per_party_historic_witout = px.treemap(df_senate_candidates_party_repli_group,
                                                               path=[px.Constant(
                                                                   "all"), 'party_detailed'],
                                                               values='candidatevotes',
                                                               color='party_detailed',
                                                               color_discrete_map={
                                                                   'REPUBLICAN': 'red',
                                                                   'DEMOCRAT': 'blue',
                                                                   'REFORM PARTY': 'light-blue',
                                                                   'LIBERTARIAN': 'gold',
                                                                   'INDEPENDENT': 'gray',
                                                                   'OTHER': 'green',
                                                                   'GREEN': 'green',
                                                                   '(?)': 'black',
                                                               })


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
                                             color='party_simplified',
                                             color_discrete_map={
                                                 'REPUBLICAN': 'red',
                                                 'DEMOCRAT': 'blue',
                                                 'REFORM PARTY': 'light-blue',
                                                 'LIBERTARIAN': 'gold',
                                                 'INDEPENDENT': 'gray',
                                                 'OTHER': 'green',
                                                 'GREEN': 'green',
                                             },
                                             text="party_simplified")


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


# -----------------------------------
#   PART 3 - Create layout
# -----------------------------------


app.layout = html.Div(children=[


    html.P(children='Data Vizualization Final Project By:'),
    html.P(children='Queen Mudau and Julian Oliveros Forero'),


    html.Div([
        html.Div(" . ", style={
            'color': 'rgba(255, 0, 0, 0.0001)',
            'backgroundColor': 'rgba(255, 0, 0, 0.9)',
            "font-size": "40px"}),
        html.Div("  .  ", style={
            "font-weight": "bold",
            'color': 'rgba(0, 0, 255, 0.0000001)',
            'backgroundColor': 'rgba(0, 0, 255, 0.9)',
            "font-size": "40px"})

    ], style={
        'border': '1px solid black'
    }),


    html.H1(children='Historic US Election Results for the period  1976-2020',
            style={'textAlign': 'center', "font-weight": "bold"}),
    html.Br(),

    html.H2(children='Historic US Election for President',
            style={'textAlign': 'center', "font-weight": "bold", "margin-left": "15px"}),
    html.Br(),

    html.P(children='Hipothesis: Over the past century the democratic political party had has the control on the presidncy and the senate of the united States',
           style={'textAlign': 'center', "font-weight": "bold", "margin-left": "15px"}),
    html.Br(),


    html.H3(children='Total amount of votes during the period 1976-2020 per political party for presidency elections',
            style={"font-weight": "bold"}),
    dcc.Graph(
        id='fig_number_votes_per_party_historic',
        figure=fig_number_votes_per_party_historic
    ),
    html.Li(children="Democrat and republic party are the  governing party in a presidential system with more votes since they hold a majority of elected positions in presidential systems.",
            style={
                'color': 'black',
                "font-size": "20px"}),
    html.Br(),




    html.H3(children='Total amount of votes during the period 1976-2020 per political (without Democratic and Republic) party for presidency elections',
            style={"font-weight": "bold"}),
    dcc.Graph(
        id='fig_number_votes_per_party_historic_witout_demo_replu',
        figure=fig_number_votes_per_party_historic_witout_demo_replu
    ),
    html.Li(children="The Independent Party it is the largest continuing third party in the United States.",
            style={
                'color': 'black',
                "font-size": "20px"}),
    html.Br(),




    html.H3(children='Map that shows which political party had the most votes per state over the diferent presidency elections between 1976-2020',
            style={"font-weight": "bold"}),


    html.Div([
        html.P('Select Year:', style={
               'color': 'black',
               'margin-left': '1%',
               "font-size": "29px",
               "font-weight": "bold"}),
        dcc.Slider(
             id='year_change_1',
             included=False,
             updatemode='drag',
             tooltip={'always_visible': True},
             step=4,
             value=2020,
             marks={
                 yr: str(yr) for yr in df_president_candidates_party_max_merge["year"]}
             ),
        dcc.Graph(id="graph_map")

    ]),
    html.Li(children='As the voting history shows, president   Reagan  from Republic party  carried every state except for Minnesota(MN) and  also  remain  the only presidential candidate since  1976  to 2020 to win almost all the state. Republic party won the elections for three consecutive term.',
            style={
                'color': 'black',
                "font-size": "20px"}
            ),
    html.Li(children='States—such as Alaska(AK), Oklahoma(OK), and Wyoming(WY)—have consistently supported the Republican Party. On the other hand, Minnesota(MN), has been Democrat strongholds .',
            style={
                'color': 'black',
                "font-size": "20px"}),
    html.Li(children="""Many states get heavy red, many others get heavy blue, while some stay "swing", which are: Virginia, North Carolina, Pennsylvania, Ohio, Iowa, Georgia, Florida and Arizona. these are 'battleground' for presidential campaigns .""",
            style={
                'color': 'black',
                "font-size": "20px"}),




    html.Br(),


    # html.Div([
    #     html.P("Select a year:"),
    #     dcc.RadioItems(
    #         id='year_change_1',
    #         options=df_president_candidates_party_max_merge["year"].unique(),
    #         value="2020",
    #         inline=True
    #     ),
    #     dcc.Graph(id="graph_map"),
    # ]),




    html.H3(children='Graph tha shows the total votes of the most representative parties over the diferent presidency elections between 1976-2020',
            style={"font-weight": "bold"}),
    dcc.Graph(
        id='fig_president_per_party_past_years_sum',
        figure=fig_president_per_party_past_years_sum
    ),
    html.Li(children="Minor parties face difficulties in  winning elections. looking at 2020 election is the indications that the minor-party candidates was factors anywhere near the level they were for  1990s election.",
            style={
                'color': 'black',
                "font-size": "20px"}),
    html.Br(),



    html.H3(children='Table of the elected president, the political party and number of votes between 1976-2020',
            style={"font-weight": "bold"}),
    dash_table.DataTable(
        df_president_names_and_percentage_new_max_merge1.to_dict(
            'records'), [{"name": i, "id": i}
                         for i in df_president_names_and_percentage_new_max_merge1.columns
                         ],
        style_header={'border': '1px solid black',
                      'marginLeft': 'auto',
                      'marginRight': 'auto',
                      'text-align': 'center',
                      'backgroundColor': 'rgb(210, 210, 210)',
                      "font-weight": "bold"},

        style_cell={'border': '1px solid grey',
                    'text-align': 'center',
                    'color': 'black',
                    "font-weight": "bold",
                    "font-size": "20px"},

        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{party_detailed} contains "REPUBLICAN"',
                },
                'backgroundColor': 'rgba(255, 0, 0, 0.8)',
            },
            {
                'if': {
                    'filter_query': '{party_detailed} contains "DEMOCRAT"',
                },
                'backgroundColor': 'rgba(0, 0, 255, 0.8)',

            }]),
    html.Li(children="The 2020 election had  the largest voter turnout in U.S.                                                                                                                       Because of the COVID-19 pandemic, many states expanded vote-by-mail to help people safely vote in the 2020 election. the availability of mail voting helped increase overall voter turnout.",
            style={
                'color': 'black',
                "font-size": "20px"}),

    html.Li(children="After the presidency Bush, it seems to be more challenging for any Republican candidate to get more popular votes. History repeated in the 2016 election with 8 times larger margin, Trump won the presidency with almost 3 million votes behind Clinton.",
            style={
                'color': 'black',
                "font-size": "20px"}),

    html.Li(children="The voter turnout rate in America has fluctuated over time but in general, it has been increasing. It's heavily relied on the voting policies change in America. the voting right has reached closer to each of every group of society.",
            style={
                'color': 'black',
                "font-size": "20px"}),
    html.Br(),







    html.H2(children='Historic US Election for Senate',
            style={'textAlign': 'center', "font-weight": "bold"}),
    html.Br(),


    html.H3(children='Total amount of votes during the period 1976-2020 per political party for the senate elections',
            style={"font-weight": "bold"}),
    dcc.Graph(
        id='fig_senate_candidates_party_sum_all',
        figure=fig_senate_candidates_party_sum_all
    ),
    html.Li(children="""During the period 1976 and 2020 the two most representatives parties that have had control over the senate of the us are the republicans and democrasts being the Democrats the onees that have had more number of votes leading with a 4% of diference repect the Republicans""",
            style={
                'color': 'black',
                "font-size": "20px"}),
    html.Li(children="The 4% of all the votes correspond to around 60 diferent parties while the other 94% correspond to democratis and republicans",
            style={
                'color': 'black',
                "font-size": "20px"}),
    html.Br(),


    html.H3(children='Total amount of votes during the period 1976-2020 per political (without Democratic and Republic) party for senate elections',
            style={"font-weight": "bold"}),
    dcc.Graph(
        id='fig_senate_number_votes_per_party_historic_witout',
        figure=fig_senate_number_votes_per_party_historic_witout
    ),
    html.Li(children="The Libertarian, Democratic-farmer-Labor and Independent are the next 3 parties with more votes in the senate of the US.",
            style={
                'color': 'black',
                "font-size": "20px"}),
    html.Br(),


    html.H3(children='Map that shows which political party had the most votes per state over the diferent senate elections between 1976-2020',
            style={"font-weight": "bold"}),

    html.Div([
        html.P('Select Year:', style={
               'color': 'black',
               'margin-left': '1%',
               "font-size": "29px",
               "font-weight": "bold"}),
        dcc.Slider(
             id='year_change_2',
             included=False,
             updatemode='drag',
             tooltip={'always_visible': True},
             step=4,
             value=2020,
             marks={
                 yr: str(yr) for yr in df_senate_candidates_party_max_merge["year"]}
             ),
        dcc.Graph(id="graph_map_senate")

    ]),

    html.Li(children="During the year 2000 the states of ND,MN and GA had candidate that did not belong to Republican neither democratic party.",
            style={
                'color': 'black',
                "font-size": "20px"}),
    html.Li(children="The western states of the US over the period where mostly Democratic ",
            style={
                'color': 'black',
                "font-size": "20px"}),
    html.Li(children="After 1996 the south East states of US started to voted mostly for Republic party ",
            style={
                'color': 'black',
                "font-size": "20px"}),
    html.Li(children="Over the other states theres not a clear trend of votes either for republican nor democratis since it changes a lot between both.",
            style={
                'color': 'black',
                "font-size": "20px"}),
    html.Br(),


    html.H3(children='Graph tha shows the total votes of the most representative parties over the diferent senate elections between 1976-2020',
            style={"font-weight": "bold"}),
    dcc.Graph(
        id='fig_senate_per_party_past_years_sum',
        figure=fig_senate_per_party_past_years_sum
    ),
    html.Li(children="Since the last century the amount of total votes during the elections of the senate has increased which means that its good that more people have claim the right to vote",
            style={
                'color': 'black',
                "font-size": "20px"}),
    html.Li(children="During the period 2012-2018 the total amount of votes for the Democratac party was slightly higher than for the republican. and for the year 2020 this results changes to be the Republican having more votes. ",
            style={
                'color': 'black',
                "font-size": "20px"}),
    html.Li(children="The diference of amount of votes for parties that are not republican nor democrtic its very low even dthought its bigger for the actual century than from the last one.",
            style={
                'color': 'black',
                "font-size": "20px"}),

    html.Br(),


    html.H3(children='Table of the most voted senators, the political party and number of votes between 1976-2020',
            style={"font-weight": "bold"}),
    dash_table.DataTable(
        df_senate_names_and_percentage_new_max_merge1.to_dict(
            'records'), [{"name": i, "id": i}
                         for i in df_senate_names_and_percentage_new_max_merge1.columns
                         ],

        style_header={'border': '1px solid black',
                      'marginLeft': 'auto',
                      'marginRight': 'auto',
                      'text-align': 'center',
                      'backgroundColor': 'rgb(210, 210, 210)',
                      "font-weight": "bold"},

        style_cell={'border': '1px solid grey',
                    'text-align': 'center',
                    'color': 'black',
                    "font-weight": "bold",
                    "font-size": "20px"},

        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{party_detailed} contains "REPUBLICAN"',
                },
                'backgroundColor': 'rgba(255, 0, 0, 0.8)'
            },
            {
                'if': {
                    'filter_query': '{party_detailed} contains "DEMOCRAT"',
                },
                'backgroundColor': 'rgba(0, 0, 255, 0.8)'

            }]),
    html.Li(children="The candiates with more votes during the period 1976-2020 for the senate has not a clear winner between the political parties republican and democratats.",
            style={
                'color': 'black',
                "font-size": "20px"}),

    html.Li(children="For the period of 1976-1890 the republican party candidates where having most of the votes.",
            style={
                'color': 'black',
                "font-size": "20px"}),
    html.Br(),
    html.Br(),


    html.H2(children='Final Conclusions',
            style={'textAlign': 'center', "font-weight": "bold"}),
    html.Br(),
    html.Li(children="Minor parties can invigorate voter interest by promoting a unique or flamboyant candidate and by focusing attention on a contentious issue. the methods implemented for  2020 elections must be repeated to increase voters   turnover. Recessions may not fully urge people to go voting, but it has been the game-changer in deciding if the ruling party will continue to stay in power.so the parties in power must always prepare for that.",
            style={
                'color': 'black',
                "font-size": "20px"}),

    html.Li(children="because there are only two big parties which can able to govern the country, American has not always voted to choose the president but the party. And more importantly, they vote to decide whether to continue the direction of the current ruling party or to change.",
            style={
                'color': 'black',
                "font-size": "20px"}),

    html.Li(children="The diference ov er the total votes and the number of elected president for the parties Democratad and Conservative is slightly diferent which is good for the country since its not allways governed by the same political party.",
            style={
                'color': 'black',
                "font-size": "20px"}),
    html.Br(),



    html.Div([
        html.Div(" . ", style={
            'color': 'rgba(255, 0, 0, 0.00001)',
            "font-weight": "bold",
            'backgroundColor': 'rgba(255, 0, 0, 0.8)',
            "font-size": "40px"}),
        html.Div("  .  ", style={
            "font-weight": "bold",
            'color': 'rgba(0, 0, 255, 0.000001)',
            'backgroundColor': 'rgba(0, 0, 255, 0.8)',
            "font-size": "40px"})

    ], style={
        'border': '1px solid black'
    }),


])


@ app.callback(
    Output("graph_map_senate", "figure"),
    Input("year_change_2", "value"))
def display_choropleth(input_value):
    df_senate_candidates_party_max_merge_2 = df_senate_candidates_party_max_merge.copy()

    df_senate_candidates_party_max_merge_2.drop(
        df_senate_candidates_party_max_merge_2.loc[df_senate_candidates_party_max_merge_2['year'] != int(input_value)].index, inplace=True)

    fig = px.choropleth(locations=df_senate_candidates_party_max_merge_2["state_po"],
                        locationmode="USA-states",
                        color=df_senate_candidates_party_max_merge_2["party_detailed"],
                        color_discrete_map={
        'REPUBLICAN': 'red',
        'DEMOCRAT': 'blue',
        'LIBERTARIAN': 'gold',
        'INDEPENDENT': 'gray',
        'REFORM PARTY': 'light-blue',
        'OTHER': 'green',
        'GREEN': 'green',
    },
        scope="usa")
    return fig


@ app.callback(
    Output("graph_map", "figure"),
    Input("year_change_1", "value"))
def display_choropleth(input_value):
    df_president_candidates_party_max_merge_to_show_2 = df_president_candidates_party_max_merge.copy()

    df_president_candidates_party_max_merge_to_show_2.drop(
        df_president_candidates_party_max_merge_to_show_2.loc[df_president_candidates_party_max_merge_to_show_2['year'] != int(input_value)].index, inplace=True)

    fig = px.choropleth(locations=df_president_candidates_party_max_merge_to_show_2["state_po"],
                        locationmode="USA-states",
                        color=df_president_candidates_party_max_merge_to_show_2["party_detailed"],
                        color_discrete_map={
        'REPUBLICAN': 'red',
        'DEMOCRAT': 'blue',
        'LIBERTARIAN': 'gold',
        'INDEPENDENT': 'gray',
        'REFORM PARTY': 'light-blue',
        'OTHER': 'green',
        'GREEN': 'green',
    },
        scope="usa")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
