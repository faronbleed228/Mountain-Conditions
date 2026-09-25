import json
from urllib.parse import urlencode
from urllib.request import urlopen
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class ParameterSeries(BaseModel):
    name: str
    unit: str
    data: list[float | None]


class ParameterFlag(BaseModel):
    name: str
    unit: str
    data: list[int | None]


class Parameters(BaseModel):
    dd: ParameterSeries
    dd_flag: ParameterFlag
    ff: ParameterSeries
    ff_flag: ParameterFlag
    ffx: ParameterSeries
    ffx_flag: ParameterFlag
    rr: ParameterSeries
    rr_flag: ParameterFlag
    sh: ParameterSeries
    sh_flag: ParameterFlag
    tl: ParameterSeries
    tl_flag: ParameterFlag


class Properties(BaseModel):
    station: int
    parameters: Parameters


class Geometry(BaseModel):
    type: str
    coordinates: list[float]


class Features(BaseModel):
    geometry: Geometry
    properties: Properties


class GeospehereData(BaseModel):
    timestamps: list[datetime | None]
    features: list[Features]


def geospehere_data_validation(id):
    base_url = (
        "https://dataset.api.hub.geosphere.at/"
        "v1/station/historical/klima-v2-1h"
    )
    params = {
        "parameters": "tl,tl_flag,rr,rr_flag,ff,ff_flag,ffx,ffx_flag,dd,dd_flag,sh,sh_flag",
        "station_ids": "14812",
        "start": "2024-01-01T00:00",
        "end": "2024-01-21T03:00",
        "output_format": "geojson",
    }

    url = f"{base_url}?{urlencode(params)}"
    with urlopen(url, timeout=30) as response:
        raw = response.read()

    pd_data = GeospehereData.model_validate_json(raw)
    data = json.loads(raw)

    # print(data)
    for feature in pd_data.features:
        print(feature.properties.parameters.sh.data)
