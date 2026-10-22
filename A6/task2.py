import pandas as pd
import matplotlib.pyplot as plt
from filters import filter_date


def count_condition_by_location(data_file, start_date, end_date, top_n=10):
    df = pd.read_csv(
        data_file,
        usecols=['Created Date', 'Complaint Type', 'Location Type']
    )

    # Convert Created Date to datetime
    df['Created Date'] = pd.to_datetime(df['Created Date'], errors='coerce')

    # Filter by date range
    df = filter_date(df, start_date, end_date)

    # Filter for Dirty Condition complaints
    df = df[df['Complaint Type'] == 'Dirty Condition'].copy()

    # Replace missing location types
    df['Location Type'] = df['Location Type'].fillna('Unknown')

    # Count complaints by location type
    counts = df['Location Type'].value_counts()

    # Keep the top N location types and group the rest as Other
    if top_n is not None and len(counts) > top_n:
        other_count = counts.iloc[top_n:].sum()
        counts = counts.iloc[:top_n].copy()
        counts['Other'] = other_count

    # Return a DataFrame
    counts.index.name = 'Location Type'
    counts.name = 'Complaint Count'

    return counts


def plot_dirty_condition_by_location(counts):
    # Plot complaint counts by location type
    ax = counts.plot(
        kind='bar',
        figsize=(12, 6),
        color='steelblue',
        width=0.8
    )

    ax.set_xlabel('Location Type')
    ax.set_ylabel('Number of Dirty Condition Complaints')
    ax.set_title('Dirty Condition Complaints by Location Type')

    # Display count labels above each bar
    ax.bar_label(ax.containers[0], fmt='%d', padding=3)

    # Rotate labels for readability
    ax.tick_params(axis='x', labelrotation=45)

    plt.tight_layout()
    plt.show()