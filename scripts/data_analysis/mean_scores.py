from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def add_bar_labels(ax, bar, labels) -> None:
    """Add labels to the top of the bars in a bar plot.

    Args:
        ax: The axis of the plot.
        bar: The bars in the plot.
        labels: The labels to add to the bars.
    """
    for rect, bar_mean in zip(bar, labels):
        height = rect.get_height()
        ax.text(
            rect.get_x() + rect.get_width() / 2.0,
            1.01 * height,
            str(round(bar_mean, 2)),
            ha="center",
            va="bottom",
            fontsize=14,
        )


def get_mean_usefulness_scores(
    dist_variable_variants: List[str],
    dist_variable: str,
    data_cond_variants: List[str],
    data_cond_variable: str,
    resp_dim: str,
    data_df: pd.DataFrame,
) -> Dict[str, Dict[str, float]]:
    """Gets the mean usefulness scores for explanations.

    Args:
        dist_variable_variants: Variants of the distribution variable.
        dist_variable: Distribution variable.
        data_cond_variants: Variants of the data condition variable.
        data_cond_variable: Data condition variable.
        resp_dim: Response dimension.
        data_df: Dataframe containing the results from a user study.

    Returns:
        A dictionary containing the mean usefulness scores for explanations.
    """
    means = {}
    means["All data"] = {}
    for value in dist_variable_variants:
        sub_df = data_df[data_df[dist_variable] == value]
        if len(sub_df) > 0:
            response_dimension_values = list(sub_df[resp_dim])
            means["All data"][value] = sum(response_dimension_values) / len(
                response_dimension_values
            )

    if data_cond_variable == "response_quality":
        sub_label = " Response"
    elif data_cond_variable == "additional_info_quality":
        sub_label = " Additional Info"

    for data_cond_variant in data_cond_variants:
        data_df_sub = data_df[data_df[data_cond_variable] == data_cond_variant]
        means[data_cond_variant + sub_label] = {}

        for value in dist_variable_variants:
            sub_df = data_df_sub[data_df_sub[dist_variable] == value]
            if len(sub_df) > 0:
                response_dimension_values = list(sub_df[resp_dim])
                means[data_cond_variant + sub_label][value] = sum(
                    response_dimension_values
                ) / len(response_dimension_values)

    return means


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

    aggregated_data = aggregated_data.replace({np.nan: "None"})

    # Mean response usefulness scores for explanations with different levels of accuracy

    plt.rcParams.update({"font.size": 11})

    resp_dim = "usefulness"
    barWidth = 0.25
    fig, ax = plt.subplots(figsize=(7, 3))

    means = get_mean_usefulness_scores(
        ["Good", "Flawed", "None"],
        "additional_info_quality",
        ["Good", "Flawed"],
        "response_quality",
        resp_dim,
        aggregated_data,
    )

    br1 = np.arange(len(list(means.keys())))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]

    plt.ylim(2, 4)

    print(means)

    bar_1_values = [var_means["Good"] for var_means in means.values()]
    bar1 = plt.bar(
        br1,
        bar_1_values,
        color="sandybrown",
        width=barWidth,
        edgecolor="gray",
        label="Accurate",
    )
    add_bar_labels(ax, bar1, bar_1_values)

    bar_2_values = [var_means["Flawed"] for var_means in means.values()]
    bar2 = plt.bar(
        br2,
        bar_2_values,
        color="bisque",
        width=barWidth,
        edgecolor="gray",
        label="Noisy",
    )
    add_bar_labels(ax, bar2, bar_2_values)

    bar_3_values = [var_means["None"] for var_means in means.values()]
    bar3 = plt.bar(
        br3,
        bar_3_values,
        color="silver",
        width=barWidth,
        edgecolor="gray",
        label="None",
    )
    add_bar_labels(ax, bar3, bar_3_values)

    plt.xticks(
        [0.25, 1.25, 2.35],
        ["All data", "Perfect response", "Imperfect response"],
        fontsize=14,
    )

    plt.legend(
        loc="lower right",
        fontsize=13,
        title="Explanations quality",
        title_fontsize=13,
    )
    plt.show()

    fig.savefig(
        "results/quantitative_analysis/mean_scores/means_usefulness_explanation_quality.png"
    )

    # Mean response usefulness scores for explanations with different presentation modes

    plt.rcParams.update({"font.size": 11})

    resp_dim = "usefulness"
    barWidth = 0.25
    fig, ax = plt.subplots(figsize=(7, 3))

    dist_variable_variants = ["T", "V", "None"]
    dist_variable = "presentation_modes"

    data_cond_variants = ["Good", "Flawed"]
    data_cond_variable = "additional_info_quality"

    means = get_mean_usefulness_scores(
        dist_variable_variants,
        dist_variable,
        data_cond_variants,
        data_cond_variable,
        resp_dim,
        aggregated_data,
    )

    br1 = np.arange(len(list(means.keys())))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2[:1]]

    plt.ylim(2, 4)

    bar_1_values = [var_means["T"] for var_means in means.values()]
    bar1 = plt.bar(
        br1,
        bar_1_values,
        color="#dfc27d",
        width=barWidth,
        edgecolor="grey",
        label="Textual",
    )
    add_bar_labels(ax, bar1, bar_1_values)

    bar_2_values = [var_means["V"] for var_means in means.values()]
    bar2 = plt.bar(
        br2,
        bar_2_values,
        color="#80cdc1",
        width=barWidth,
        edgecolor="grey",
        label="Visual",
    )
    add_bar_labels(ax, bar2, bar_2_values)

    bar_3_values = [means["All data"]["None"]]
    print(bar_3_values)
    bar3 = plt.bar(
        br3,
        bar_3_values,
        color="silver",
        width=barWidth,
        edgecolor="grey",
        label="None",
    )
    add_bar_labels(ax, bar3, bar_3_values)

    plt.xticks(
        [0.25, 1.1, 2.2],
        ["All data", "Accurate explanations", "Noisy explanations"],
        fontsize=14,
    )

    plt.legend(
        loc="lower right",
        fontsize=13,
        title="Presentation mode",
        title_fontsize=13,
    )
    plt.show()

    fig.savefig(
        "results/quantitative_analysis/mean_scores/means_usefulness_explanation_presentation.png"
    )

    # Mean explanation ratings for explanations with different levels of accuracy

    plt.rcParams.update({"font.size": 11})

    barWidth = 0.33
    fig, ax = plt.subplots(figsize=(5.5, 3))

    dist_variable_variants = ["Good", "Flawed"]
    dist_variable = "additional_info_quality"
    means = {}

    means["Source Revealment"] = {}
    for value in dist_variable_variants:
        sub_df = aggregated_data[aggregated_data[dist_variable] == value]
        if len(sub_df) > 0:
            response_dimension_values = list(sub_df["source_usefulness"])
            means["Source Revealment"][value] = sum(
                response_dimension_values
            ) / len(response_dimension_values)

    means["Confidence Revealment"] = {}
    for value in dist_variable_variants:
        sub_df = aggregated_data[aggregated_data[dist_variable] == value]
        if len(sub_df) > 0:
            response_dimension_values = list(sub_df["confidence_usefulness"])
            means["Confidence Revealment"][value] = sum(
                response_dimension_values
            ) / len(response_dimension_values)

    br1 = np.arange(len(list(means.keys())))
    br2 = [x + barWidth for x in br1]

    plt.ylim(2, 4)

    print(means)

    bar_1_values = [var_means["Good"] for var_means in means.values()]
    bar1 = plt.bar(
        br1,
        bar_1_values,
        color="sandybrown",
        width=barWidth,
        edgecolor="gray",
        label="Accurate",
    )
    add_bar_labels(ax, bar1, bar_1_values)

    bar_2_values = [var_means["Flawed"] for var_means in means.values()]
    bar2 = plt.bar(
        br2,
        bar_2_values,
        color="bisque",
        width=barWidth,
        edgecolor="gray",
        label="Noisy",
    )
    add_bar_labels(ax, bar2, bar_2_values)

    plt.xticks(
        [r + barWidth / 2 for r in range(len(list(means.keys())))],
        ["Source", "Confidence"],
        fontsize=14,
    )

    plt.legend(
        loc="lower right",
        fontsize=13,
        title="Explanations quality",
        title_fontsize=13,
    )
    plt.show()

    fig.savefig(
        "results/quantitative_analysis/mean_scores/means_explanation_ratings_explanation_quality.png"
    )

    # Mean explanation ratings for explanations with different presentation modes

    plt.rcParams.update({"font.size": 11})

    barWidth = 0.33
    fig, ax = plt.subplots(figsize=(5.5, 3))

    dist_variable_variants = ["T", "V"]
    dist_variable = "presentation_modes"
    means = {}

    means["Limitation Revealment"] = {}
    for value in dist_variable_variants:
        sub_df = aggregated_data[aggregated_data[dist_variable] == value]
        if len(sub_df) > 0:
            response_dimension_values = list(sub_df["warning_usefulness"])
            means["Limitation Revealment"][value] = sum(
                response_dimension_values
            ) / len(response_dimension_values)

    means["Confidence Revealment"] = {}
    for value in dist_variable_variants:
        sub_df = aggregated_data[aggregated_data[dist_variable] == value]
        if len(sub_df) > 0:
            response_dimension_values = list(sub_df["confidence_usefulness"])
            means["Confidence Revealment"][value] = sum(
                response_dimension_values
            ) / len(response_dimension_values)

    br1 = np.arange(len(list(means.keys())))
    br2 = [x + barWidth for x in br1]

    plt.ylim(2, 4)

    print(means)

    bar_1_values = [var_means["T"] for var_means in means.values()]
    bar1 = plt.bar(
        br1,
        bar_1_values,
        color="#dfc27d",
        width=barWidth,
        edgecolor="gray",
        label="Textual",
    )
    add_bar_labels(ax, bar1, bar_1_values)

    bar_2_values = [var_means["V"] for var_means in means.values()]
    bar2 = plt.bar(
        br2,
        bar_2_values,
        color="#80cdc1",
        width=barWidth,
        edgecolor="gray",
        label="Visual",
    )
    add_bar_labels(ax, bar2, bar_2_values)

    plt.xticks(
        [r + barWidth / 2 for r in range(len(list(means.keys())))],
        ["Limitation", "Confidence"],
        fontsize=14,
    )

    plt.legend(
        loc="lower right",
        fontsize=13,
        title="Presentation mode",
        title_fontsize=13,
    )
    plt.show()

    fig.savefig(
        "results/quantitative_analysis/mean_scores/means_explanation_ratings_explanation_presentation.png"
    )
