from flask import Flask, render_template, jsonify
import json
import requests
from shapely.geometry import shape

app = Flask(__name__, static_folder="static")

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para obtener el polígono del barrio
@app.route('/api/polygon')
def get_polygon():
    with open('data/tunal.geojson', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return jsonify(data)

# Ruta para obtener árboles desde la API y guardarlos en GeoJSON
@app.route('/api/trees')
def get_trees():
    with open('data/tunal.geojson', 'r', encoding='utf-8') as file:
        myJSON = json.load(file)

    mygeometry = myJSON['features'][0]['geometry']
    myBBox = shape(mygeometry).bounds  # xmin, ymin, xmax, ymax

    url = "https://geoportal.jbb.gov.co/agc/rest/services/SIGAU/CensoArbol/MapServer/0/query"
    params = {
        "f": "json",
        "geometry": f"{myBBox[0]},{myBBox[1]},{myBBox[2]},{myBBox[3]}",
        "geometryType": "esriGeometryEnvelope",
        "spatialRel": "esriSpatialRelIntersects",
        "where": "1=1",
        "outFields": "*"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        geojson_data = {
            "type": "FeatureCollection",
            "features": []
        }

        for feature in data.get("features", []):
            geojson_feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [feature["geometry"]["x"], feature["geometry"]["y"]]
                },
                "properties": feature["attributes"]
            }
            geojson_data["features"].append(geojson_feature)

        with open("data/arboles.geojson", "w", encoding="utf-8") as file:
            json.dump(geojson_data, file, ensure_ascii=False, indent=4)

        return jsonify(geojson_data)
    else:
        return jsonify({"error": "Error en la solicitud"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
