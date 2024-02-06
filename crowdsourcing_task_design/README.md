# User Study

## Design

Each HIT contains ten query-response pairs and consists of: 
- A) HIT instructions providing task background; 
- B) a questionnaire about worker's familiarity with conversational assistants (frequency of using a conversational assistant in general and for search;
- C) a description of the system; 
- D) ten CIS interactions; 
- E) a post-task questionnaire; and 
- F) a demographics questionnaire.

![](/task_components.png)

Part C contains a pre-use explanation of the system. It aims at improving the following competencies of the users: (1) understanding the capabilities of the system, and (2) understanding that the response is limited to 3 sentences only. We decompose part D of the user study into multiple subsections using independent CIS interactions to facilitate atomic microtask crowdsourcing. Each CIS interaction contains: 
- a) a query; 
- b) a topic familiarity questionnaire; 
- c) a system response possibly enhanced with explanations; 
- d) a corresponding attentiveness check; and 
- e) a CIS response assessment.

The screenshot of one of the tasks used in the crowdsourcing process can be found [here](/task_design.png). It presents specific questions used in the questionnaires.

## Experimental Conditions

We have defined ten experimental conditions using different variants of the response and explanations. We acknowledge that the variants for each of the transparency dimensions that we consider are not exhaustive. It is possible to investigate various UI elements to present given information, different ways to introduce noise in given components, etc. However, as the communication of response-related information has not been explored in the area of conversational search, we limit the first study in this area to the solutions that have been already proposed for similar systems leaving for future work proposing brand new solutions.

Given the large number of factors, it is out of the scope of this study to consider all possible combinations using factorial designs -- the number of conditions exceeds 200 (2 variants for response, 3 variants for each of the components of the additional information in terms of quality, 2 variants for system confidence and response limitations in terms of presentation mode gives 216 different experiments even without query randomization).

Covering all combination of factors (explanation components * quality * presentation mode) exhaustively would be unfeasible. Therefore, we select a subset of experimental conditions that best represent what we are trying to measure in our study. The selected conditions vary along three main dimensions: (i) response correctness, (ii) quality of the explanations (i.e., source, system confidence, limitations), and (iii) presentation style.

The input data and the construction of question sets is covered in details [here](../data/input/README.md).