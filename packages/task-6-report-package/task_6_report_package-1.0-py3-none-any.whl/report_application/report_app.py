import typing
from datetime import datetime
import os
from argparse import ArgumentParser

# constants
FORMAT_STR = "%H:%M:%S.%f"
MAX_LINES = 15


def read_file(directory_path, file):
    file_path = os.path.join(directory_path, file)
    if file is None:
        raise ValueError("File is not provided.")
    try:
        with (open(file_path, "r") as file):
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        raise FileNotFoundError("File not found. Please check the file path.")


def racer_data_processing(source_data_racers):
    separate_data_racers = [
        data_racer.split('_')
        for data_racer in source_data_racers
    ]
    keys = ['abbr', 'name', 'team']
    dict_separate_data_racers = [dict(zip(keys, item)) for item in separate_data_racers]
    return dict_separate_data_racers


def time_data_processing(time_data):
    separate_time_data = [
        data_string.split('_')
        for line in time_data
        for data_string in line.split("\n")
    ]
    dict_separate_time_data = [{'abbr': item[0][:3], 'time': item[1]} for item in separate_time_data]
    return dict_separate_time_data


def subtract_times(start_time, end_time):
    start_lap = datetime.strptime(start_time, FORMAT_STR)
    end_lap = datetime.strptime(end_time, FORMAT_STR)
    time_lap = str(abs(end_lap - start_lap))[:-3]
    return time_lap


def process_file_data(directory_path: str, file_name: str, processor: typing.Callable) -> dict[str, dict]:
    crude_data = read_file(directory_path, file_name)
    data = processor(crude_data)
    return {item.get('abbr'): item for item in data}


def build_report(directory_path):

    racer_dict = process_file_data(directory_path, "abbreviations.txt", racer_data_processing)
    start_dict = process_file_data(directory_path, "start.log", time_data_processing)
    end_dict = process_file_data(directory_path, "end.log", time_data_processing)

    report = []
    for abbr in set(racer_dict) & set(start_dict) & set(end_dict):
        start_time, end_time = start_dict[abbr].get('time', ''), end_dict[abbr].get('time', '')
        time_lap = subtract_times(start_time, end_time)
        report.append({
            'name': racer_dict[abbr].get('name', ''),
            'team': racer_dict[abbr].get('team', ''),
            'best_lap_time': time_lap,
        })

    report = sorted(report, key=lambda x: x['best_lap_time'])
    return report


def print_report(report, desc=False):
    if desc:
        report = report[::-1]
    for line, racer_data in enumerate(report, 1):
        print(f"{line}. {racer_data['name']:<30}\t| {racer_data['team']:<30}\t| {racer_data['best_lap_time']}")
        if (desc and line == len(report) - MAX_LINES) or (not desc and line == MAX_LINES):
            print("-" * 85)


def parse_arguments():
    parser = ArgumentParser(description='Command Line Interface')
    parser.add_argument('--files', type=str, help='Specify the path to the file')
    parser.add_argument('--driver', type=str, help='Input a racer name')
    parser.add_argument('--desc', action='store_true', help='Sort the report in descending order')
    return parser.parse_args()


def cli():
    args = parse_arguments()
    result = build_report(args.files)
    if args.driver:
        for data_driver in build_report(args.files):
            if args.driver == data_driver["name"]:
                print_report([data_driver])
    else:
        print_report(result, desc=args.desc)


if __name__ == '__main__':
    cli()
