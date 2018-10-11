# Predicting Graduation Rates

When I first began considering the content of this capstone project, I immediately knew that I wanted to delve into the sphere of  education. Specifically, how expenditures affect what is considered an "academically successful environment". However, I learned early on that kind of data would not be given to me this round of pursuit. Instead, I decided to investigate other factors that would potentially have very strong relationships with a school district's graduation rate. In the state of Colorado there are 181 school districts within 64 counties, serving approximately 860,000 students. In this capstone, we are exploring  


## Project Objectives

1. To accurately model graduation rates per district by building a linear regression model that utilizes graduation data, SAT/PSAT test scores, data on disciplinary action and mobility data.  

2. Provide visualizations and additional testing of a model to ensure accuracy.

2. Identify features that are the most significant predictors of graduation rates.

## Data Source

There were four datasets used to create my main_data frame:

1. District and County specific data on graduate numbers was obtained from the <a href="http://cde.state.co.us/cdereval/gradratecurrent">graduation based on race database</a>, that is reported by the CDE (Colorado Department of Education).
2. Data on <a href="http://cde.state.co.us/cdereval/mobility-stabilitycurrent">stability and mobility</a> were also taken from the CDE, who collect their data annually in October
3. <a href="http://cde.state.co.us/cdereval/suspend-expelcurrent">Disciplinary action</a> data was obtained through the CDE.
4. <a href="https://collegereadiness.collegeboard.org/sat/scores">SAT scores</a> are from reports maintained by the College Board.


## Getting to Know My Data

![](https://media.giphy.com/media/2tRoKSKZHYpWvPo9TQ/giphy.gif)

One of the more challenging and interesting parts of this process was discovering how many variables the state's education takes into account when looking to understand its student base, and what each of them actually mean. For example, in the Graduation Rate DF there were 122 features accounted for, and intuitively at first, I needed to decide whether or not they'd add value to my project's aim. Below are listed explanations for some of the features I was not familiar with and how I choose to handle them.

*DataFrame: "Category", merged into larger DF or chose to discard*

 <p><b>Disciplinary_Action: "Other Action", merged</b></br>There are certain lawful reasons why a student can be suspended or expelled but also other actions you can take. An example would be to defer expulsion, referral for drug treatment, etc.</p>

<p><b>Standardized_Scores: "Total Students" and "Percentage Participation", discarded</b><br>
Represents the number of students who took a standardized test. Out of 1371 rows, 370 included * values. This is because, by law, the state is not allowed to report its statistics if fewer than 16 students actually took the test. The student's scores are still factored into the "Overall_Mean_Score", which I did use.</p>

<p><b>District_Mobility: "BOCES", dropped</b><br> Board of cooperative education services.They are regional support entities for schools- mainly rural.</p>

<p><b>Grad_District_Rate: "All Students Final Grad Base'", merged</b><br> This is a count of all students eligible to graduate in the 12th grade, or who are ready to graduate in less than four years.</p>

<p><b>Grad_District_Rate: "All Students Completion Rate'", dropped</b><br> A ratio of students who receive a diploma after spending five or more years in a high school.</p>  

## Strategy to Create a Main_DataFrame

![](https://media.giphy.com/media/3ov9k56yg3MDP36dyM/giphy.gif)
<br>
<center>*<b>Cleaning Data</b> is a <b>profession</b>*</center>
<br>

1. Dropped redundant features or features that were inclusive of others in a single dataframe (each frame contained between 50 and 125 features, so parsing was a big deal). Used discretion when choosing to include a feature in the Main_DataFrame.
  - ran simple models of some features in question to determine if they were inclusive or collinery with another item I'd chosen.<br>
  *An example of this was when I thought that expulsion counts might be related to Referrals_to_Law_Enforcement, not Total_In_School, Total_Out_of_School_Suspensions, but it was actually only strongly correlated with Referrals_to_Law_Enforcement*<br>
  <br>

2. To simplify the initial analysis, all data was restricted to the years 2016 through 2017.

3. Used missingno matrices and heatmaps to show missing values.
<br>
 - *there was a pattern in the SAT dataset amongst missing values in Overall_Mean_Score, Total_Value_Score and Participation_Rate. Dropped Total_Value_Score and Participation_Rate and filled the missing values with the mean score.*
 <br>


4. Since each dataset has slightly different labels to represent the same thing, I determined where commonality existed and renamed the  appropriate categories to merge on.
<br>

  - *examples: <br>(discipline_action['District_Name'] == standardized_scores['District_Name'])
(grad['Organization_Name'] == standardized_scores['District_Number'])*


5. Merge my four datasets into one.


## Modeling and Evaluation
 <center><h6> The Features Explored are: 'SAT_Scores','Expulsion', 'Suspension', 'Other_Action','Total_Eligible_Grads', 'Homeless_Student_Mobility_Rate', 'Economically_Disadvantaged_Student_Mobility_Rate'</h6>

 1. With such extreme scales amongst features I standardized the data, then split it into a training and test set.

 2. Ran an OLS summary on the training set:
<br>
<img src="https://github.com/HM618/Capstone_1/blob/master/OLS%20Summary%20for%20Test%20Data.png">
<br>
- The summary suggests that most of the variance in the data is being accurately explained by the model.
- We can see here that 'Expulsion', 'Other_Action' and 'Total_Eligible_Grads' have strong, negative effects on graduation rates, though their p-values suggest completely ignoring 'expulsion' wouldn't necessarily be valuable.  


3. Ran an OLS summary on the test set:
<br>
<img src="https://github.com/HM618/Capstone_1/blob/master/OLS%20Summary%20for%20Test%20Data.png">
<br>
- This summary also seems to account for a large portion of the variance.
- The model confirms that 'Expulsion', 'Other_Action' and 'Total_Eligible_Grads' have strong negative relationships, and that the three should possibly be excluded in future tests for detecting an influencer of a school district's rate of graduation.


4. Fit the model to the training data and then return the y-intercept, beta coefficients and the predicted values
<br>
  - The y intercept is 0.676856142824749
  - The coefficients for each feature are: [ 2.74816975e-04,  1.52176905e-03, -2.09931960e-05,  4.10003043e-06, 5.83668691e-07,  4.66255613e-02, -6.49864122e-01]
  - The predicted y values based on our test model are: [0.64944435, 0.76904813, 0.79943727, ... 0.87213939, 0.87480383, 0.75804832]
<br>

5. Plot points just to be sure...
<br>
<img src="https://github.com/HM618/Capstone_1/blob/master/Grad%20Rates.png">
<br>
6. Running an RMSE function on our predicted and true values yields a root mean squared error of 0.10397958142050694, which is inline with what our summaries suggest above.

## Conclusions and Future Work

![](https://media.giphy.com/media/EszqkvmqQY13y/giphy.gif)

With our model seemingly justified in its computations and results, I can conclude that while SAT Scores, the amount of expulsions that occur, and the mobility rates of those economically disadvantaged or homeless are strong predictors for graduation rates in a district.

While my model was seemingly very good I'd like to go back through and start with one data set at a time and done a more thorough job of cleaning and aggregating prior to merging the four sets into one. I also would like to see what would've happened if I didn't drop so many features just by looking through them, and instead ran lasso regression models to tell me which I should get rid of.
