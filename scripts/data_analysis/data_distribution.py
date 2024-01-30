import collections
from typing import List

import matplotlib.pyplot as plt
import pandas as pd


def process_data_for_distribution_plot(
    response_dimensions: List[str], data_df: pd.DataFrame, main_feature: str
):
    """Processes the data for the distribution plot.

    Args:
        response_dimensions: The response dimensions used in a user study.
        data_df: Dataframe containing the results from a user study.

    Returns:
        A dictionary containing the data for the distribution plot.
    """
    values_per_query = collections.defaultdict(dict)

    for value in list(set(list(data_df[main_feature]))):
        for response_dimension in response_dimensions:
            query_sub_df = data_df[data_df[main_feature] == value]
            query_response_dimension_values = list(
                query_sub_df[response_dimension]
            )
            values_per_query[value][
                response_dimension
            ] = query_response_dimension_values

    return values_per_query


if __name__ == "__main__":
    aggregated_data = pd.read_csv(
        "results/user_study_output/output_processed_aggregated.csv"
    )

    for feature in [
        "source_usefulness",
        "warning_usefulness",
        "confidence_usefulness",
        "conversational_frequency",
        "voice_frequency",
    ]:
        f = [
            int(d.replace("option_", ""))
            for d in list(aggregated_data[feature])
        ]
        aggregated_data[feature] = f

    response_dimensions = [
        "familiarity",
        "interest",
        "search_prob",
        "relevance",
        "correctness",
        "completeness",
        "comprehensiveness",
        "conciseness",
        "serendipity",
        "coherence",
        "factuality",
        "fairness",
        "readability",
        "satisfaction",
        "usefulness",
    ]

    feature = "questions_ids"
    values_per_query = process_data_for_distribution_plot(
        response_dimensions, aggregated_data, feature
    )

    n_col = 5
    fig, axs = plt.subplots(3, n_col, figsize=(15, 9))

    for id, response_dimension in enumerate(response_dimensions):
        boxplot_data = []

        for value in range(1, 11):
            boxplot_data.append(
                values_per_query[value][response_dimension],
            )

        axs[int(id / n_col)][id % n_col].boxplot(boxplot_data)
        axs[int(id / n_col)][id % n_col].set_xlabel("Query ID")
        axs[int(id / n_col)][id % n_col].set_ylabel(
            "Worker Self-Reported Rating"
        )
        axs[int(id / n_col)][id % n_col].set_title(
            response_dimension.replace(
                "search_prob", "search probability"
            ).title()
        )

    fig.tight_layout(pad=1.0)
    plt.figure(dpi=2000)
    fig.savefig("results/quantitative_analysis/data_distribution.png")
