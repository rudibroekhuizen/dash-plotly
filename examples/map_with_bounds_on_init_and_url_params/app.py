import dash
import dash_leaflet as dl
from dash import html, dcc, Input, Output
import logging
import urllib.parse

# Configure logging to print to console
logging.basicConfig(level=logging.INFO)

app = dash.Dash(__name__, use_pages=True, pages_folder="")


def layout(
    min_lat=50.70,
    max_lat=52.40,
    min_lon=None,
    max_lon=None,
    center_lat=51.91,
    center_lon=4.91,
):
    return html.Div(
        [
            dcc.Location(id="url", refresh=False),
            dl.Map(
                id="map",
                bounds=[[min_lat, min_lon], [max_lat, max_lon]],
                center={"lat": center_lat, "lng": center_lon},
                style={"width": "50%", "height": "500px"},
                children=[dl.TileLayer()],
            ),
            html.Div(id="out"),
        ]
    )


dash.register_page("home", path="/", layout=layout)


# Update the url
@app.callback(
    Output("url", "search"),
    Input("map", "bounds"),
    Input("map", "center"),
    prevent_initial_call=True,
)
def update_url(bounds, center):
    center_lat = center["lat"]
    center_lon = center["lng"]
    min_lat = bounds[0][0]
    max_lat = bounds[1][0]
    min_lon = bounds[0][1]
    max_lon = bounds[1][1]

    params = {
        "max_lat": max_lat,
        "min_lat": min_lat,
        "max_lon": max_lon,
        "min_lon": min_lon,
        "center_lat": map_center_lat,
        "center_lon": map_center_lon,
    }
    query_string = urllib.parse.urlencode(params)
    return f"?{query_string}"


# Show bounds, center and zoom
@app.callback(
    Output("out", "children"),
    Input("map", "bounds"),
    Input("map", "center"),
    Input("map", "zoom"),
)
def show_logs(bounds, center, zoom):
    logging.info(f"Bounds: {bounds}")
    logging.info(f"Center: {center}")
    logging.info(f"Zoom: {zoom}")
    return f"Bounds: {bounds}, center: {center}, zoom: {zoom}"


if __name__ == "__main__":
    app.run(debug=True)
