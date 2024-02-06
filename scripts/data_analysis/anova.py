import argparse
from collections import defaultdict
from typing import List, Tuple

import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm


def effect_size(
    data_df: pd.DataFrame, aov_table: pd.DataFrame
) -> Tuple[List[float], List[str]]:
    """Calculates the effect size for each parameter.

    Args:
        aov_table: Pd.DataFrame containing the ANOVA table.
        data_df: Dataframe containing the data.

    Returns:
        A tuple containing the effect size and the size.
    """
    w2facts = []
    sizes = []
    for id, row in aov_table.iterrows():
        w2fact = round((row['df'] * (row['F'] - 1)) / (row['df'] * (row['F'] - 1) + len(data_df)), 3)
        w2facts.append(w2fact)
        if w2fact >= 0.14:
            size = 'L'
        elif w2fact >= 0.06 and w2fact < 0.14:
            size = 'M'
        elif w2fact >= 0.00 and w2fact < 0.06:
            size = 'S'
        else:
            size = '-'
        sizes.append(size)
    return w2facts, sizes


def one_way_anova(
    data_df: pd.DataFrame,
    answer_feature: List[str],
    independent_variable: str,
):
    """Runs a one-way ANOVA test.

    Args:
        data_df: Dataframe containing the data.
        answer_feature: Answer feature.
        independent_variable: Independent variable.
    """
    dataframe = pd.DataFrame({independent_variable: list(data_df[independent_variable]),
                            answer_feature: list(data_df[answer_feature])})

    formula = answer_feature + ' ~ C(' + independent_variable + ') '
    model = ols(formula, dataframe).fit()
    aov_table = anova_lm(model, typ=2)

    w2facts, sizes = effect_size(data_df, aov_table)
    aov_table['w2facts'] = w2facts
    aov_table['sizes'] = sizes

    for _, row in aov_table.iterrows():
        if row.name != 'Residual':
            param = row.name.replace('C(', '').replace(')', '').replace('answers_ids', 'answer condition').replace('questions_ids', 'question').lower()
            fvalue = round(row['F'], 3)
            pvalue = round(row['PR(>F)'], 3)
            if pvalue <= 0.05:
                return  str(answer_feature), '\\textbf{' + str(param) + '}', '\\bfseries' + str(pvalue) + ' { (' + str(row['sizes']) + ')}'
            else:
                return str(answer_feature), str(param), str(pvalue) + ' { (' + str(row['sizes']) + ')}'


def two_way_anova (data_df, answer_feature, first_independent_variable, second_independent_variable):
    dataframe = pd.DataFrame({first_independent_variable: list(data_df[first_independent_variable]),
                                second_independent_variable: list(data_df[second_independent_variable]),
                                answer_feature: list(data_df[answer_feature])})

    formula = answer_feature + ' ~ C(' + first_independent_variable + ') + C(' + second_independent_variable + ') + C(' + first_independent_variable + '):C(' + second_independent_variable + ')'
    model = ols(formula, dataframe).fit()
    aov_table = anova_lm(model, typ=2)

    w2facts, sizes = effect_size(data_df, aov_table)
    aov_table['w2facts'] = w2facts
    aov_table['sizes'] = sizes

    # print(aov_table.round(3))

    for _, row in aov_table.iterrows():
        if row.name != 'Residual':
            param = row.name.replace('C(', '').replace(')', '').replace('answers_ids', 'answer condition').replace('questions_ids', 'question').lower()
            fvalue = round(row['F'], 3)
            pvalue = round(row['PR(>F)'], 3)

            if ":" in param:
                if pvalue <= 0.05:
                    return str(answer_feature), str(param), '\\textbf{' + str(pvalue) + ' (' + str(row['sizes']) + ')}'
                else:
                    return str(answer_feature), str(param), str(pvalue) + ' (' + str(row['sizes']) + ')'


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

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--type",
        help="Argument type is required. Select 'one-way' or 'two-way'.",
    )
    args = parser.parse_args()

    if args.type == "one-way":
        print("All conditions (EC1–EC10)")

        features = [
            "usefulness",
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
            "source_usefulness",
            "confidence_usefulness",
            "warning_usefulness",
        ]

        for independent_var in [
            "response_quality",
            "additional_info_quality",
            "presentation_modes",
            "questions_ids",
            "familiarity",
            "interest",
            "search_prob",
            "conversational_frequency",
            "voice_frequency",
        ]:
            pvalues = {}
            for feature in features:
                _, _, pvalue = one_way_anova(
                    aggregated_data, feature, independent_var
                )
                pvalues[feature] = pvalue
            print(
                independent_var.replace("_", " ")
                + " & "
                + " & ".join(list(pvalues.values()))
                + " \\\\"
            )
        print(len(aggregated_data))
        print("Only conditions with explanations (EC1–EC8)")

        aggregated_data_ec1_8 = aggregated_data[
            (aggregated_data["answers_ids"] != "EC9")
            & (aggregated_data["answers_ids"] != "EC10")
        ]

        for independent_var in [
            "response_quality",
            "additional_info_quality",
            "presentation_modes",
        ]:
            pvalues = {}
            for feature in features:
                _, _, pvalue = one_way_anova(
                    aggregated_data_ec1_8, feature, independent_var
                )
                pvalues[feature] = pvalue
            print(
                independent_var.replace("_", " ")
                + " & "
                + " & ".join(list(pvalues.values()))
                + " \\\\"
            )
        print(len(aggregated_data_ec1_8))

    elif args.type == "two-way":
        print("Interactions with Query")

        for independent_var in [
            "response_quality",
            "additional_info_quality",
            "presentation_modes",
            "conversational_frequency",
            "voice_frequency",
            "familiarity",
            "interest",
            "search_prob",
        ]:
            pvalues = defaultdict(list)
            for feature in [
                "usefulness",
                "satisfaction",
                "source_usefulness",
                "confidence_usefulness",
                "warning_usefulness",
            ]:
                feature, indep_var, pvalue = two_way_anova(
                    aggregated_data, feature, independent_var, "questions_ids"
                )
                pvalues[feature] = pvalue
            print(
                independent_var.replace("_", " ")
                + " & "
                + " & ".join(list(pvalues.values()))
                + " \\\\"
            )

        print("Interactions with Topic Familiarity")

        for independent_var in [
            "response_quality",
            "additional_info_quality",
            "presentation_modes",
        ]:
            for feature in [
                "usefulness",
                "satisfaction",
                "source_usefulness",
                "confidence_usefulness",
                "warning_usefulness",
            ]:
                feature, indep_var, pvalue = two_way_anova(
                    aggregated_data, feature, independent_var, "familiarity"
                )
                pvalues[feature] = pvalue
            print(
                independent_var.replace("_", " ")
                + " & "
                + " & ".join(list(pvalues.values()))
                + " \\\\"
            )

    else:
        raise ValueError(
            "Argument type is required and must be either 'one-way' or 'two-way'"
        )
