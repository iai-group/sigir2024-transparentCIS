"""Script for processing the output data from the user study."""
import ast

import pandas as pd

if __name__ == "__main__":
    file_name = "results/user_study_output/mturk_output.csv"
    output_raw = pd.read_csv(file_name)
    final_df = pd.DataFrame()
    output_raw = output_raw.fillna(" ")

    for experimental_condition in [str(i) for i in range(1, 11)]:
        output = output_raw[
            output_raw["Input.experimental_cond"]
            == str(["EC" + experimental_condition] * 10)
        ]
        if len(output) > 0:
            summary = [[] for _ in range(10)]

            familiarity = [[] for _ in range(10)]
            interest = [[] for _ in range(10)]
            search_prob = [[] for _ in range(10)]

            relevance = [[] for _ in range(10)]
            correctness = [[] for _ in range(10)]
            completeness = [[] for _ in range(10)]
            comprehensiveness = [[] for _ in range(10)]
            conciseness = [[] for _ in range(10)]
            serendipity = [[] for _ in range(10)]
            coherence = [[] for _ in range(10)]
            factuality = [[] for _ in range(10)]
            fairness = [[] for _ in range(10)]
            readability = [[] for _ in range(10)]
            satisfaction = [[] for _ in range(10)]
            usefulness = [[] for _ in range(10)]
            explanation = [[] for _ in range(10)]

            conversational_frequency = []
            voice_frequency = []

            source_usefulness = []
            warning_usefulness = []
            confidence_usefulness = []

            source_usefulness_explanation = []
            warning_usefulness_explanation = []
            confidence_usefulness_explanation = []

            age = []
            education = []
            gender = []

            p_clicked_details = []
            p_clicked_links = []

            for row_id, row in output.iterrows():
                for option in ["option_" + str(i) for i in range(1, 7)]:
                    if row["Answer.education." + option] == True:
                        education.append(option)

                for option in ["option_" + str(i) for i in range(1, 6)]:
                    if row["Answer.age." + option] == True:
                        age.append(option)
                    if row["Answer.gender." + option] == True:
                        gender.append(option)
                    if row["Answer.conversational_frequency." + option] == True:
                        conversational_frequency.append(option)
                    if row["Answer.voice_frequency." + option] == True:
                        voice_frequency.append(option)

                for option in ["option_" + str(i) for i in range(1, 5)]:
                    if row["Answer.source_usefulness." + option] == True:
                        source_usefulness.append(option)
                    if row["Answer.warning_usefulness." + option] == True:
                        warning_usefulness.append(option)
                    if row["Answer.confidence_usefulness." + option] == True:
                        confidence_usefulness.append(option)

                source_usefulness_explanation.append(
                    row["Answer.source_usefulness_explanation"]
                )
                warning_usefulness_explanation.append(
                    row["Answer.warning_usefulness_explanation"]
                )
                confidence_usefulness_explanation.append(
                    row["Answer.confidence_usefulness_explanation"]
                )

            additional_info_df = pd.DataFrame(
                {
                    "conversational_frequency": conversational_frequency,
                    "voice_frequency": voice_frequency,
                    "source_usefulness": source_usefulness,
                    "warning_usefulness": warning_usefulness,
                    "confidence_usefulness": confidence_usefulness,
                    "source_usefulness_explanation": source_usefulness_explanation,
                    "warning_usefulness_explanation": warning_usefulness_explanation,
                    "confidence_usefulness_explanation": confidence_usefulness_explanation,
                    "age": age,
                    "gender": gender,
                    "education": education,
                }
            )

            # print(additional_info_df)

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

            for row_id, row in output.iterrows():
                questions = ast.literal_eval(row["Input.query"])
                question_ids = ast.literal_eval(row["Input.query_id"])
                for question, question_id in zip(questions, question_ids):
                    for metric in metrics:
                        for option in ["option_" + str(i) for i in range(1, 5)]:
                            if (
                                row[
                                    "Answer."
                                    + metric
                                    + "_"
                                    + str(question_id)
                                    + "."
                                    + option
                                ]
                                == True
                            ):
                                globals()[metric][question_id - 1].append(
                                    option.replace("option_", "")
                                )

                    for option in ["s_" + str(i) for i in range(1, 4)]:
                        if (
                            row[
                                "Answer.summary_"
                                + str(question_id)
                                + "."
                                + option
                            ]
                            == True
                        ):
                            summary[question_id - 1].append(
                                option.replace("s_", "")
                            )

                    explanation[question_id - 1].append(
                        row["Answer.explanation_" + str(question_id)]
                    )

            # print(output['Input.query'])
            # print(list(output['Input.query'])[0])
            questions = ast.literal_eval(list(output["Input.query"])[0])

            worker_ids = []
            for worker_id in output["WorkerId"]:
                worker_ids.append(worker_id)

            results_df = pd.DataFrame(
                {
                    "questions_ids": ast.literal_eval(
                        list(output["Input.query_id"])[0]
                    ),
                    "questions": questions,
                    "answers": ast.literal_eval(
                        list(output["Input.response"])[0]
                    ),
                    "answers_ids": ast.literal_eval(
                        list(output["Input.experimental_cond"])[0]
                    ),
                    "summaries": ast.literal_eval(
                        list(output["Input.summaries"])[0]
                    ),
                    "summaries_scores": ast.literal_eval(
                        list(output["Input.summaries_scores"])[0]
                    ),
                    "summary_result": summary,
                    "worker_ids": [worker_ids] * 10,
                    "familiarity": familiarity,
                    "interest": interest,
                    "search_prob": search_prob,
                    "relevance": relevance,
                    "correctness": correctness,
                    "completeness": completeness,
                    "comprehensiveness": comprehensiveness,
                    "conciseness": conciseness,
                    "serendipity": serendipity,
                    "coherence": coherence,
                    "factuality": factuality,
                    "fairness": fairness,
                    "readability": readability,
                    "satisfaction": satisfaction,
                    "usefulness": usefulness,
                    "satisfaction": satisfaction,
                    "explanation": explanation,
                    "conversational_frequency": [
                        list(additional_info_df["conversational_frequency"])
                    ]
                    * len(summary),
                    "voice_frequency": [
                        list(additional_info_df["voice_frequency"])
                    ]
                    * len(summary),
                    "source_usefulness": [
                        list(additional_info_df["source_usefulness"])
                    ]
                    * len(summary),
                    "warning_usefulness": [
                        list(additional_info_df["warning_usefulness"])
                    ]
                    * len(summary),
                    "confidence_usefulness": [
                        list(additional_info_df["confidence_usefulness"])
                    ]
                    * len(summary),
                    "source_usefulness_explanation": [
                        list(
                            additional_info_df["source_usefulness_explanation"]
                        )
                    ]
                    * len(summary),
                    "warning_usefulness_explanation": [
                        list(
                            additional_info_df["warning_usefulness_explanation"]
                        )
                    ]
                    * len(summary),
                    "confidence_usefulness_explanation": [
                        list(
                            additional_info_df[
                                "confidence_usefulness_explanation"
                            ]
                        )
                    ]
                    * len(summary),
                    "age": [list(additional_info_df["age"])] * len(summary),
                    "gender": [list(additional_info_df["gender"])]
                    * len(summary),
                    "education": [list(additional_info_df["education"])]
                    * len(summary),
                    # "p_clicked_details": output['Answer.p_clicked_details'][0],
                    # "p_clicked_links": output['Answer.p_clicked_links'][0],
                    # "pilot_study_feedback": [list(output['Answer.pilot_study_feedback'])] * 10,
                }
            )

            results_df = results_df.sort_values("questions_ids")
            final_df = pd.concat([final_df, results_df], ignore_index=True)
            # final_df = final_df.append(results_df)

    final_df.to_csv("results/user_study_output/output_processed.csv")
