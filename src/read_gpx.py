from pathlib import Path
import gpxpy


def read_gpx(file_name: Path):
    with file_name.open("r", encoding="utf-8") as route:
        gpx = gpxpy.parse(route)
    for track in gpx.tracks:
        print(f"Track name: {track.name}")
        for segment in track.segments:
            for point in segment.points:
                pass
