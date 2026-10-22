import pandas as pd
import matplotlib.pyplot as plt
from filters import filter_date


def count_noise_complaint_descriptors(data_file, start_date, end_date, top_n=5):
    df = pd.read_csv(data_file, usecols=['Created Date', 'Complaint Type', 'Descriptor'])

    df = filter_date(df, start_date, end_date)

    # Filter for noise complaints
    df = df[df['Complaint Type'].str.contains('Noise', na=False)]

    # Extract month
    df['Month'] = df['Created Date'].dt.month

    # Replace missing descriptors
    df['Descriptor'] = df['Descriptor'].fillna('Unknown')

    # Count complaints for each descriptor per month
    counts = df.groupby(['Month', 'Descriptor']).size().unstack(fill_value=0)

    # Find the top N descriptors overall
    top_descriptors = counts.sum().nlargest(top_n).index

    # Keep the top descriptors and group the rest as "Other"
    counts['Other'] = counts.drop(columns='Other', errors='ignore').drop(
        columns=top_descriptors, errors='ignore'
    ).sum(axis=1) if False else 0

    other_counts = counts.drop(columns=top_descriptors, errors='ignore').sum(axis=1)
    counts = counts.reindex(columns=top_descriptors, fill_value=0)
    counts['Other'] = other_counts

    # Include all 12 months
    counts = counts.reindex(range(1, 13), fill_value=0)
    counts.index.name = 'Month'

    return counts


def plot_noise_complaint_descriptors(counts):
    # Convert counts to percentages within each month
    percentages = counts.div(counts.sum(axis=1).replace(0, 1), axis=0) * 100

    # Plot stacked percentage bars
    ax = percentages.plot(
        kind='bar',
        stacked=True,
        figsize=(14, 7),
        colormap='tab20',
        width=0.8
    )

    ax.set_xticklabels(
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        rotation=0
    )

    ax.set_xlabel('Month')
    ax.set_ylabel('Percentage of Noise Complaints (%)')
    ax.set_title('Monthly Distribution of Noise Complaint Descriptors')

    # Ensure the y-axis runs from 0 to 100%
    ax.set_ylim(0, 100)

    ax.legend(
        title='Descriptor',
        bbox_to_anchor=(1.02, 1),
        loc='upper left'
    )

    plt.tight_layout()
    plt.show()
