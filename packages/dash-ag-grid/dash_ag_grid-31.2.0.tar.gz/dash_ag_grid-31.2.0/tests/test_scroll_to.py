from dash import Dash, html, Input, Output
from dash_ag_grid import AgGrid
import plotly.express as px
import json
from dash.testing.wait import until
import pandas as pd
import pytest

from . import utils


@pytest.fixture
def df():
    return pd.read_csv(
        "https://raw.githubusercontent.com/plotly/datasets/master/ag-grid/olympic-winners.csv"
    )


@pytest.fixture
def scroll_to_inputs():
    return [
        {"rowIndex": 100, "rowPosition": "bottom", "cell": (100, 0)},
        {"column": "bronze", "columnPosition": "end", "cell": (100, 8)},
        {"rowId": "Elizabeth Beisel12/8/2012", "rowPosition": "top", "cell": (200, 8)},
        {"rowIndex": 300, "rowId": 500, "cell": (300, 8)},
        {
            "rowIndex": 400,
            "rowId": "Ryan Bayley29/08/2004",
            "column": "athlete",
            "rowPosition": "bottom",
            "columnPosition": "start",
            "cell": (400, 0),
        },
        {
            "data": {
                "athlete": "Sabine Völker",
                "age": 28,
                "country": "Germany",
                "year": 2002,
                "date": "24/02/2002",
                "sport": "Speed Skating",
                "gold": 0,
                "silver": 2,
                "bronze": 1,
                "total": 3,
            },
            "column": "bronze",
            "columnPosition": "end",
            "cell": (100, 8),
        },
        {
            "rowIndex": 2000,
            "rowId": "Elizabeth Beisel12/8/2012",
            "data": {
                "athlete": "Elizabeth Beisel",
                "age": 19,
                "country": "United States",
                "year": 2012,
                "date": "12/8/2012",
                "sport": "Swimming",
                "gold": 0,
                "silver": 1,
                "bronze": 1,
                "total": 2,
            },
            "column": "age",
            "columnPosition": "start",
            "cell": (2000, 1),
        },
    ]


def test_st001_scroll_to(dash_duo, df, scroll_to_inputs):
    app = Dash()

    # basic columns definition with column defaults
    columnDefs = [{"field": c} for c in df.columns]

    app.layout = html.Div(
        [
            AgGrid(
                id="grid",
                columnDefs=columnDefs,
                rowData=df.to_dict("records"),
                defaultColDef={"resizable": True, "sortable": True, "filter": True},
                getRowId="params.data.athlete+params.data.date",
            ),
            html.Button(id="btn"),
            html.Div(id="scrollTo-output"),
            html.Div(id="scrollTo-input"),
        ]
    )

    # Displays the prop scrollTo when it changes in the grid
    @app.callback(
        Output("scrollTo-output", "children"),
        Input("grid", "scrollTo"),
    )
    def display_scrollTo(scroll_to):
        return json.dumps(scroll_to)

    # On click sets up a new value for scrollTo from the fixture scroll_to_inputs
    @app.callback(
        Output("grid", "scrollTo"),
        Input("btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def update_scrollTo(n_clicks):
        return scroll_to_inputs[n_clicks - 1]

    dash_duo.start_server(app)
    grid = utils.Grid(dash_duo, "grid")

    # Check that the grid has been loaded successfully
    until(lambda: "Michael Phelps" == grid.get_cell(0, 0).text, timeout=3)

    for i in range(len(scroll_to_inputs)):
        info = scroll_to_inputs[i]

        y, x = info["cell"]
        dash_duo.find_element("#btn").click()
        dash_duo.wait_for_text_to_equal("#scrollTo-output", json.dumps(info), timeout=5)
        until(lambda: grid.get_cell(y, x).is_displayed(), timeout=3)

        # row testing
        if "rowPosition" in info:
            if info["rowPosition"] == "bottom":
                assert not grid.cell_in_viewport(y + 1, x)
                assert grid.cell_in_viewport(y - 1, x)
            elif info["rowPosition"] == "middle":
                assert grid.cell_in_viewport(y + 1, x)
                assert grid.cell_in_viewport(y - 1, x)
            else:
                assert grid.cell_in_viewport(y + 1, x)
                assert not grid.cell_in_viewport(y - 1, x)
        elif "rowIndex" in info or "rowId" in info or "data" in info:
            assert grid.cell_in_viewport(y + 1, x)
            assert not grid.cell_in_viewport(y - 1, x)

        # column testing
        if "column" in info:
            if "columnPosition" in info:
                if info["columnPosition"] == "end":
                    if x + 1 < len(df.columns):
                        assert not grid.cell_in_viewport(y, x + 1)
                    if x - 1 >= 0:
                        assert grid.cell_in_viewport(y, x - 1)
                elif info["columnPosition"] == "middle":
                    if x + 1 < len(df.columns):
                        assert grid.cell_in_viewport(y, x + 1)
                    if x - 1 >= 0:
                        assert grid.cell_in_viewport(y, x - 1)
                else:
                    if x + 1 < len(df.columns):
                        assert grid.cell_in_viewport(y, x + 1)
                    if x - 1 >= 0:
                        assert not grid.cell_in_viewport(y, x - 1)
            else:
                if x + 1 < len(df.columns):
                    assert grid.cell_in_viewport(y, x + 1)
                if x - 1 >= 0:
                    assert not grid.cell_in_viewport(y, x - 1)


def test_st002_initial_scroll_to(dash_duo, df):
    app = Dash()

    # basic columns definition with column defaults
    columnDefs = [{"field": c} for c in df.columns]

    app.layout = html.Div(
        [
            AgGrid(
                id="grid",
                columnDefs=columnDefs,
                rowData=df.to_dict("records"),
                defaultColDef={"resizable": True, "sortable": True, "filter": True},
                scrollTo={
                    "rowIndex": 2000,
                    "rowPosition": "top",
                    "column": "bronze",
                    "columnPosition": "end",
                },
            ),
        ]
    )

    dash_duo.start_server(app)

    grid = utils.Grid(dash_duo, "grid")
    until(lambda: "1" == grid.get_cell(2000, 9).text, timeout=3)

    y = 2000
    x = 8

    until(
        lambda: grid.get_cell(y, x).is_displayed(),
        timeout=3,
    )

    # row testing
    assert grid.cell_in_viewport(y + 1, x)
    assert not grid.cell_in_viewport(y - 1, x)

    # column testing
    assert not grid.cell_in_viewport(y, x + 1)
    assert grid.cell_in_viewport(y, x - 1)
