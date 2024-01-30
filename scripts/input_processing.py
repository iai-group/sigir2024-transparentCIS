"""Script for creating the input data for the user study."""
import random

import pandas as pd

if __name__ == "__main__":
    data = pd.read_csv("data/input/input_data.csv")

    question_set_data_mturk_dict_final = []

    for experimental_condition in [str(i) for i in range(1,11)]:
        question_set = ["EC" + experimental_condition] * 10

        responses_to_add = []
        sources_to_add = []
        sources_links_to_add = []
        limitations_to_add = []
        certainties_to_add = []
        summaries_to_add = []
        summaries_scores_to_add = []

        for row_id, row in data.iterrows():
            experimental_cond = question_set[row_id]
            response = ""

            if experimental_cond in ["EC1", "EC2", "EC5", "EC6", "EC9"]:
                response = row["Response good"]
                summaries_columns = [
                    row["Summary GC"],
                    row["Summary GI1"],
                    row["Summary GI2"],
                ]
            else:
                response = row["Response bad"]
                summaries_columns = [
                    row["Summary BC"],
                    row["Summary BI1"],
                    row["Summary BI2"],
                ]

            summaries_scores = [1, 0, 0]
            summaries = {}
            for summary_score, summary_column in zip(
                summaries_scores, summaries_columns
            ):
                summaries[summary_column] = summary_score

            summaries_keys = list(summaries.keys())
            random.shuffle(summaries_keys)
            summaries_shuffled = [
                (key, summaries[key]) for key in summaries_keys
            ]

            summaries_to_add.append(summaries_keys)
            summaries_scores_to_add.append(
                [summaries[key] for key in summaries_keys]
            )

            if experimental_cond in ["EC1", "EC2", "EC3", "EC4"]:
                sources_to_add.append(row["Source"])
                sources_links_to_add.append(row["Source link"])
            elif experimental_cond in ["EC5", "EC6", "EC7", "EC8"]:
                sources_to_add.append(row["Source noise"])
                sources_links_to_add.append(row["Source link noise"])
            else:
                sources_to_add.append("")
                sources_links_to_add.append("")

            system_certainty_bad = 20 * int(row["Certainty bad"])
            system_certainty_good = 20 * int(row["Certainty good"])

            if experimental_cond in ["EC1", "EC2"]:
                limitations_to_add.append("")
                if experimental_cond == "EC2":
                    certainties_to_add.append("")
                    response += (
                        " "
                        + "The system confidence in the provided response is "
                        + str(system_certainty_good)
                        + "%."
                    )
                else:
                    certainties_to_add.append(row["Certainty good"])
            elif experimental_cond in ["EC3", "EC4"]:
                if experimental_cond == "EC4":
                    limitations_to_add.append("")
                    certainties_to_add.append("")
                    response += (
                        " "
                        + str(row["Response with limitation"])
                        + " the system confidence in the provided response is "
                        + str(system_certainty_bad)
                        + "%."
                    )
                else:
                    limitations_to_add.append(row["Limitation"])
                    certainties_to_add.append(row["Certainty bad"])
            elif experimental_cond in ["EC5", "EC6"]:
                if experimental_cond == "EC6":
                    limitations_to_add.append("")
                    certainties_to_add.append("")
                    response += (
                        " "
                        + str(row["Response with limitation noise"])
                        + " the system confidence in the provided response is "
                        + str(system_certainty_bad)
                        + "%."
                    )
                else:
                    limitations_to_add.append(row["Limitation noise"])
                    certainties_to_add.append(row["Certainty bad"])
            elif experimental_cond in ["EC7", "EC8"]:
                if experimental_cond == "EC8":
                    limitations_to_add.append("")
                    certainties_to_add.append("")
                    response += (
                        " "
                        + str(row["Response with limitation noise"])
                        + " the system confidence in the provided response is "
                        + str(system_certainty_good)
                        + "%."
                    )
                else:
                    limitations_to_add.append(row["Limitation noise"])
                    certainties_to_add.append(row["Certainty good"])
            else:
                limitations_to_add.append("")
                certainties_to_add.append("")

            responses_to_add.append(response)

        question_set_data = pd.DataFrame(
            {
                "experimental_cond": question_set,
                "query_id": list(range(1, 11)),
                "query": list(data["Query"]),
                "response": responses_to_add,
                "sources": sources_to_add,
                "source_links": sources_links_to_add,
                "limitations": limitations_to_add,
                "certainty": certainties_to_add,
                "sources": sources_to_add,
                "summaries": summaries_to_add,
                "summaries_scores": summaries_scores_to_add,
            }
        )

        question_set_data = question_set_data.sample(frac=1)
        # question_set_data.to_csv(
        #     "qs" + experimental_condition + ".csv", index=False
        # )

        question_set_data_mturk_dict = {}

        for column in question_set_data.columns:
            question_set_data_mturk_dict[column] = str(
                list(question_set_data[column])
            )

        question_set_data_mturk_dict_final.append(question_set_data_mturk_dict)

    question_set_data_mturk = pd.DataFrame(question_set_data_mturk_dict_final)
    question_set_data_mturk.to_csv(
        "data/input/input_mturk_format.csv", index=False
    )
