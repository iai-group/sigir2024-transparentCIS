# Pilot Study

We ran a pilot study, where HITs corresponded to three experimental conditions selected from the 10 described in Table~\ref{tab:experimental_conditions}: 
- EC3 - responses contain flaws that are communicated to the user without any noise in a visual format, 
- EC4 - responses contain flaws that are communicated to the user without any noise in a textual format,
- EC7 - responses contain flaws that are communicated to the user with noise in a visual format.
We selected experimental conditions to encompass border cases, featuring variations in both the presentation mode of explanations (EC3 vs. EC4) and the quality explanations (EC3 vs. EC7). The chosen conditions deliberately involve imperfect responses to simulate the most natural scenarios. 

Each HIT was completed by five unique crowd workers, earning a USD 3 reward for each submission. The reward was estimated based on the time needed by an expert to complete the task and the federal minimum wage in the US (USD 7.25 per hour). In the overall feedback for the tasks, crowd workers primarily expressed concerns about the length of the task and the payment which was accordingly increased in the large-scale data collection.

Input for the pilot study can be found [here](input/) (and [here](input/mturk_format/) in the MTurk input format). Data collected during this pilot can be found [here](output/mturk_output/) in the MTurk output format (and [here](output/processed/) preprocessed).

## Power Analysis

We performed a power analysis, by employing one-way ANOVA with the experimental condition as an independent variable and user-reported response usefulness as a dependent variable. The script available [here](https://waseda.app.box.com/v/SIGIR2016PACK) has been used for running the power analysis (*future.sample.1wayanova*). The script uses m=2 (2 variants/experimental conditions), and n=5 (5 workers looking at each variant of the query-response pair).

| HITs | F | P-value | Power analysis result |
| --- | --- | --- | --- | 
| EC3 + EC4 | 2.145 | 0.146 | 16 |
| EC3 + EC7 | 0.578 |  0.44 | 56 |


The results indicate that 16 workers are required to observe a statistically significant effect of explanation quality on the perceived usefulness of system responses, whereas 56 workers are required for a statistically significant effect of the explanation presentation mode. Considering four additional pairs of experimental conditions with varying presentation modes, we expect that gathering data from 14 unique workers per HIT (56 from power analysis divided by 4 pairs of conditions) is adequate to observe a statistically significant effect of presentation mode across all ten experimental conditions. Despite variations in other aspects of the response in the experimental conditions not used in the pilot, we opted for this simplification due to the substantially higher costs associated with involving 42 additional crowd workers (resulting in almost four times the cost). However, recognizing that noise in explanations is more dependent on other aspects of system response and their variation between experimental conditions, we decided to increase the number of unique workers per HIT to 16 following the results of power analysis on data from EC3 and EC7.