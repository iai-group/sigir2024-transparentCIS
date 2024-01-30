# Input Data

Data used in the user study can be found [here](input_data.csv) (and [here](input_mturk_format.csv) in the MTurk input format). It contains:
- ten queries selected from the TREC CAsT 2020 and 2022 datasets 
- two manually created responses for each query (perfect and imperfect)
- different variants of explanations created manually for each query (accurate and noisy)
- summaries of each response variant used in the attentiveness check in the user study

[This script](../../scripts/input_processing.py) has been used for preparing input in the MTurk format.