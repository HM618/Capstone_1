One of the more challenging and interesting parts of this process was discovering how many variables the state's education takes into account when looking to understand its student base, and what each of them actually mean. For example, in the Graduation Rate DF there were 122 features accounted for, and intuitively at first, deciding whether or not they'd add value to my project's aim. Below are listed explanations for some of the features I was not familiar with.

DataFrame: "Category", merged into larger DF or chose to discard

Disciplinary_Action: "Other Action", merged -There are certain lawful reasons why a student can be suspended or expelled but also other actions you can take. An example would be to defer expulsion, referral for drug treatment, etc.

Standardized_Scores: "Total Students" and "Percentage Participation", discarded - Represented the number of students who took a standardized test. Our of 1371 rows, 370 included * values. This is because, by law, the state is not allowed to report its statistics if fewer than 16 students actually took the test. I was concerned that those unaccounted for would skew my results, but was assured that the student's scores are still factored into the "Overall_Mean_Score", which I did use.

Since each dataset has slightly different labels to represent the same thing, determine where commonality lies, rename appropriate categories to merge on.
(discipline_action['District_Name'] == standardized_scores['District_Name'])
(grad['Organization_Name'] == standardized_scores['District_Number'])
# Capstone_1
