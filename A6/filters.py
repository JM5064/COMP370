import pandas as pd


def filter_date(df, start_date, end_date):
    # Format date
    df["Created Date"] = pd.to_datetime(df["Created Date"])

    one_day = pd.Timedelta(days=1)

    filtered_df = df[df["Created Date"].between(start_date, end_date + one_day)]

    return filtered_df