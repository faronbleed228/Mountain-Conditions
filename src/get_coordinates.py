from urllib.request import urlopen, Request
from urllib.parse import urlencode
from pydantic import BaseModel, Field, model_validator, TypeAdapter, ValidationError
from errors import GeneralException
import json


class PeakCandidate(BaseModel):
    display_name: str
    category: str
    type: str
    lat: float
    lon: float
    extratags: dict[str, str] = Field(default_factory=dict)

    @model_validator(mode="after")
    def peak_validator(self) -> "PeakCandidate":
        if self.type != "peak":
            raise ValidationError
        if self.category != "natural":
            raise ValidationError
        return self


def search_peaks(peak_input: str) -> PeakCandidate:
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": peak_input,
        "countrycodes": "at",
        "format": "jsonv2",
        "extratags": "1",
        "limit": "10",
    }
    url = f"{base_url}?{urlencode(params)}"
    request = Request(url, headers={"User-Agent": "MountainConditions/0.1"})
    with urlopen(request, timeout=50) as responce:
        data = json.load(responce)
    print(data)
    candidates: list[PeakCandidate] = TypeAdapter(
        list[PeakCandidate]).validate_python(data)
    peak_index = 0
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) < 1:
        raise GeneralException(
            "Could find given peak. Please check your input and try again.")
    if len(candidates) > 1:
        print("System found several peak candidates with this name. Please make a choice")
    while len(candidates) > 1:
        for index, candidate in enumerate(candidates):
            print(f"{index}:{candidate.display_name}. Type:({candidate.type})")
        try:
            chosen_peak = int(input(
                f"Choose peak from candidates 0-{len(candidates)}:"))
            peak_index = int(chosen_peak)
            candidates[peak_index]
        except (ValueError, IndexError):
            print(f"Please input correct index 0-{len(candidates)}")
        else:
            break
    return candidates[peak_index]
