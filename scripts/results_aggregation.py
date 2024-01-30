"""Script for aggregating the output data from the user study."""
import ast

import pandas as pd

if __name__ == "__main__":
    output = pd.read_csv("results/user_study_output/output_processed.csv")

    presentation_modes = []
    response_quality = []
    additional_info_quality = []

    for id, row in output.iterrows():
        if row["answers_ids"] in ["EC" + str(i) for i in [1, 3, 5, 7]]:
            presentation_modes.append("V")
        elif row["answers_ids"] in ["EC" + str(i) for i in [2, 4, 6, 8]]:
            presentation_modes.append("T")
        else:
            presentation_modes.append("None")

        if row["answers_ids"] in ["EC" + str(i) for i in [1, 2, 5, 6, 9]]:
            response_quality.append("Good")
        else:
            response_quality.append("Flawed")

        if row["answers_ids"] in ["EC" + str(i) for i in [1, 2, 3, 4]]:
            additional_info_quality.append("Good")
        elif row["answers_ids"] in ["EC" + str(i) for i in [5, 6, 7, 8]]:
            additional_info_quality.append("Flawed")
        else:
            additional_info_quality.append("None")

    output["presentation_modes"] = presentation_modes
    output["response_quality"] = response_quality
    output["additional_info_quality"] = additional_info_quality

    metrics = [
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

    aggregated_data = pd.DataFrame(columns=output.columns)

    for id, row in output.iterrows():
        for annotation_id in range(0, 16):
            new_row = row.copy(deep=True)
            for metric in metrics + [
                "worker_ids",
                "summary_result",
                "explanation",
                "age",
                "gender",
                "education",
                "conversational_frequency",
                "voice_frequency",
                "source_usefulness",
                "warning_usefulness",
                "confidence_usefulness",
                "source_usefulness_explanation",
                "warning_usefulness_explanation",
                "confidence_usefulness_explanation",
            ]:
                new_row[metric] = list(ast.literal_eval(row[metric]))[
                    annotation_id
                ]
            # aggregated_data = aggregated_data.append(new_row, ignore_index = True)
            aggregated_data = pd.concat(
                [aggregated_data, pd.DataFrame([new_row])], ignore_index=True
            )

    aggregated_data = aggregated_data.sort_values(
        ["questions_ids", "answers_ids"], ascending=[True, True]
    )

    for metric in metrics:
        aggregated_data[metric] = aggregated_data[metric].apply(
            lambda xn: int(xn)
        )

    aggregated_data.to_csv(
        "results/user_study_output/output_processed_aggregated.csv", index=False
    )
