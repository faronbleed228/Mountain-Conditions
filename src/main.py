from errors import GeneralException
from pydantic import ValidationError
from urllib.error import HTTPError
from argparse import ArgumentParser, Namespace
from pathlib import Path

from goespehere import geospehere_data_validation
from get_coordinates import search_peaks
from read_gpx import read_gpx


def main() -> None:
    args = parse_arguments()
    try:
        read_gpx(args.gpx)
# peak = input("Enter the desired peak:")
# chosen_peak = search_peaks(peak)
# print(chosen_peak)

# geospehere_data_validation(123)
    except (ValidationError, HTTPError, GeneralException) as e:
        print(e)


def parse_arguments() -> Namespace:
    argument_parser = ArgumentParser("MountainCondition")
    argument_parser.add_argument(
        "--gpx", default=Path(__file__).resolve().parent.parent/"route.gpx",
        type=Path, help="path to route gpx file")
    args: Namespace = argument_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
