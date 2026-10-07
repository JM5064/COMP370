import argparse
import pandas as pd
import time


def count_borough_complaints(data_file, start_date, end_date):
    df = pd.read_csv(data_file, usecols=['Created Date', 'Complaint Type', 'Borough'])

    # Formate date
    df["Created Date"] = pd.to_datetime(df["Created Date"])

    filtered_df = df[df["Created Date"].between(start_date, end_date)]

    counts_df = (
        filtered_df
        .value_counts(["Complaint Type", "Borough"])
        .reset_index(name="count")
    )

    return counts_df



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

    counts = count_borough_complaints(args.i, start_date, end_date)

    print(counts)
    if args.o is not None:
        counts.to_csv(args.o, index=False)


