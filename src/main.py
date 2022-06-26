# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# FINAL PROJECT DATA VISUALITION
# BY:
#   JULIAN OLIVEROS FORERO
#   QUEEN


from gettext import translation
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


# ---------------------
# Viz 1: 1. The number of votes per party is detailed historic during all the times.
# ---------------------

df_president_candidates_party = president[["candidatevotes", "party_detailed"]]


df_goals_per_position_sum = df_president_candidates_party.groupby(
    ["party_detailed"]).sum().reset_index(drop=False)


df = px.data.tips()
fig_number_votes_per_party_historic = px.treemap(df_goals_per_position_sum,
                                                 path=[px.Constant(
                                                     "all"), 'party_detailed'],
                                                 values='candidatevotes',
                                                 title="The number of votes per party is detailed historic during all the times.")

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
                                                                   title="The number of votes per party is detailed historic during all the times.")

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
                                                color="party_simplified",
                                                title="Total votes per most representative parties for the period 1970 - 2020")

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


# fig_df_president_names_and_percentage_new_max_merge1 = go.Figure(data=[go.Table(
#     header=dict(values=list(df_president_names_and_percentage_new_max_merge1.columns),
#                 fill_color='paleturquoise',
#                 align='left'),
#     cells=dict(values=[df_president_names_and_percentage_new_max_merge1.year,
#                        df_president_names_and_percentage_new_max_merge1.candidatevotes,
#                        df_president_names_and_percentage_new_max_merge1.party_detailed,
#                        df_president_names_and_percentage_new_max_merge1.candidate],
#                fill_color='lavender',
#                align='left'))
# ])


# ---------------------
# Viz 1: 6. The number of votes per party is detailed historic during all the times.
# ---------------------


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
                                                               title="The number of votes per party is detailed historic during all the times.")

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
# VIZ 9: Show the percentage of votes from each party for the past years.
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
                                             title="Total votes per most representative parties for the period 1970 - 2020")

# fig_president_per_party_past_years_sum.show()


# ---------------------
# VIZ 10:  Show the name of the last 10 presidents show their names and show the number of votes they had to win.
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
    html.H1(children='Historic US Election Results'),

    html.Div(children='''
        Dash: A web application framework for Python.
        By:
            Julian Esteban Oliveros Forero
            Queen
    '''),

    dcc.Graph(
        id='fig_number_votes_per_party_historic',
        figure=fig_number_votes_per_party_historic
    ),
    dcc.Graph(
        id='fig_number_votes_per_party_historic_witout_demo_replu',
        figure=fig_number_votes_per_party_historic_witout_demo_replu
    ),
    html.Div([
        html.H4('Polotical candidate voting pool analysis'),
        html.P("Select a candidate:"),
        dcc.RadioItems(
            id='year_change_1',
            options=df_president_candidates_party_max_merge["year"].unique(),
            value="2020",
            inline=True
        ),
        dcc.Graph(id="graph_map"),
    ]),
    dcc.Graph(
        id='fig_president_per_party_past_years_sum',
        figure=fig_president_per_party_past_years_sum
    ),
    dash_table.DataTable(
        df_president_names_and_percentage_new_max_merge1.to_dict(
            'records'), [{"name": i, "id": i}
                         for i in df_president_names_and_percentage_new_max_merge1.columns
                         ]),
    dcc.Graph(
        id='fig_senate_candidates_party_sum_all',
        figure=fig_senate_candidates_party_sum_all
    ),
    dcc.Graph(
        id='fig_senate_number_votes_per_party_historic_witout',
        figure=fig_senate_number_votes_per_party_historic_witout
    ),
    html.Div([
        html.H4('Polotical candidate voting pool analysis'),
        html.P("Select a year:"),
        dcc.RadioItems(
            id='year_change_2',
            options=df_senate_candidates_party_max_merge["year"].unique(),
            value="1976",
            inline=True
        ),
        dcc.Graph(id="graph_map_senate"),
    ]),
    dcc.Graph(
        id='fig_senate_per_party_past_years_sum',
        figure=fig_senate_per_party_past_years_sum
    ),
    dash_table.DataTable(
        df_senate_names_and_percentage_new_max_merge1.to_dict(
            'records'), [{"name": i, "id": i}
                         for i in df_senate_names_and_percentage_new_max_merge1.columns
                         ]),


])


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


@app.callback(
    Output("graph_map", "figure"),
    Input("year_change_1", "value"))
def display_choropleth(input_value):
    df_president_candidates_party_max_merge_to_show_2 = df_president_candidates_party_max_merge.copy()

    df_president_candidates_party_max_merge_to_show_2.drop(
        df_president_candidates_party_max_merge_to_show_2.loc[df_president_candidates_party_max_merge_to_show_2['year'] != int(input_value)].index, inplace=True)

    fig = px.choropleth(locations=df_president_candidates_party_max_merge_to_show_2["state_po"],
                        locationmode="USA-states",
                        color=df_president_candidates_party_max_merge_to_show_2["party_detailed"],
                        scope="usa")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
