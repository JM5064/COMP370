import argparse
import pandas as pd

from task1 import count_noise_complaint_descriptors, plot_noise_complaint_descriptors
from task2 import count_condition_by_location, plot_dirty_condition_by_location


if __name__ == "__main__":
    # borough_complaints.py -i <the input csv file> -s <start date> -e <end date> [-o <output file>]
    # python A5/borough_complaints.py -i data/311_Service_Requests_from_2010_to_Present_20250928_small.csv -s 1/1/2024 -e 12/31/2024 -o data/results.csv

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", type=str, help="<the input csv file>", required=True)
    parser.add_argument("-s", type=str, help="<start date>", required=True)
    parser.add_argument("-e", type=str, help="<end date>", required=True)
    parser.add_argument("-o", type=str, help="<output file>", required=False)

    args = parser.parse_args()

    start_date = pd.to_datetime(args.s)
    end_date = pd.to_datetime(args.e)

    # if args.o is not None:
    #     counts.to_csv(args.o, index=False)

    noise_complaint_descriptor_counts = count_noise_complaint_descriptors(args.i, start_date, end_date)
    plot_noise_complaint_descriptors(noise_complaint_descriptor_counts)

    dirty_condition_counts = count_condition_by_location(args.i, start_date, end_date)
    plot_dirty_condition_by_location(dirty_condition_counts)


