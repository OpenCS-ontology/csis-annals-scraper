# from scrapper_vol1 import DriverWrapper_Volume_1
# from scrape import DriverWrapper
from scrape import DriverWrapper, DriverWrapper_Volume_1
from doi import CrossRefClient
import pandas as pd
import argparse
import os
import yaml
import shutil


def tuple_type(strings):
    # https://stackoverflow.com/questions/33564246/passing-a-tuple-as-command-line-argument
    strings = strings.replace("(", "").replace(")", "")
    volumes = tuple(map(int, strings.split(",")))
    if len(volumes) == 2:
        volumes = tuple(range(volumes[0], volumes[1] + 1))
    else:
        volumes = tuple(set(volumes))

    return volumes


def return_config(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)


def main():
    parser = argparse.ArgumentParser(description='Program scraping https://annals-csis.org/')
    parser.add_argument('--volumes', type=tuple_type, default=tuple(range(1, 33)),
                        help='Indices of volumes to scrape. A list of integers or a range of integers represented by a tuple of 2 integers. \
                    If the input is a list of integers, any duplicates will be removed. If the input is a tuple of 2 integers, \
                    it will be interpreted as an inclusive range of integers, and all integers within that range will be included in the final list.')
    parser.add_argument('--config', type=str, default='scrape_config.yaml',
                        help='Path to config file, default `scrape_config.yaml`')
    args = parser.parse_args()

    config = return_config(args.config)

    for volume in args.volumes:
        output_path = config['output_path'] + str(volume)

        if os.path.exists(output_path):
            shutil.rmtree(output_path)

        os.mkdir(output_path)
        if volume == 1:
            scraper = DriverWrapper_Volume_1(output_path=output_path)
        else:

            scraper = DriverWrapper(output_path=output_path)

        page_to_scrape = config['base_webpage'] + f'Volume_{volume}'
        print(page_to_scrape)
        print(f"Scraping Volume {volume}, {page_to_scrape}")
        scraper.traverse_papers(page_to_scrape, str(volume))


if __name__ == "__main__":
    main()
