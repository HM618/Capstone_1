# Predicting Graduation Rates

When I first began considering the content of this capstone project, I immediately knew that I wanted to delve into the sphere of  education. Specifically, how expenditures affect what is considered an "academically successful environment". However, I learned early on that kind of data would not be given to me this round of pursuit. Instead, I decided to investigate other factors that would potentially have very strong relationships with a school district's graduation rate. In the state of Colorado there are 181 school districts within 64 counties, serving approximately 860,000 students. In this capstone, we are exploring  


### Project Objectives

1. To accurately model graduation rates per district by building a linear regression model that utilizes graduation data, SAT/PSAT test scores, data on disciplinary action and mobility data.  

2. Provide visualizations and additional testing of the model at ensure accuracy.

2. Identify features that are the most significant predictors of graduation rates.

### Data Source

There were four datasets used to create my main_data frame:

1. District and County specific data on graduate numbers was obtained from the graduation based on race database, that is reported by the CDE (<a href="http://cde.state.co.us/cdereval/gradratecurrent">Colorado Department of Education</a>).
2. Data on <a href="http://cde.state.co.us/cdereval/mobility-stabilitycurrent">stability and mobility</a> were also taken from CDE, who collect their data annually in October
3. <a href="http://cde.state.co.us/cdereval/suspend-expelcurrent">Disciplinary action</a> data is obtained through the CDE.
4. <a href="https://collegereadiness.collegeboard.org/sat/scores">SAT scores</a> are from reports maintained by the College Board.

Methods


### Getting to Know My Data

One of the more challenging and interesting parts of this process was discovering how many variables the state's education takes into account when looking to understand its student base, and what each of them actually mean. For example, in the Graduation Rate DF there were 122 features accounted for, and intuitively at first, deciding whether or not they'd add value to my project's aim. Below are listed explanations for some of the features I was not familiar with and how I choose to handle them.

*DataFrame: "Category", merged into larger DF or chose to discard*

 <p><b>Disciplinary_Action: "Other Action", merged</b></br>There are certain lawful reasons why a student can be suspended or expelled but also other actions you can take. An example would be to defer expulsion, referral for drug treatment, etc.</p>

<p><b>Standardized_Scores: "Total Students" and "Percentage Participation", discarded</b><br>
Represented the number of students who took a standardized test. Out of 1371 rows, 370 included * values. This is because, by law, the state is not allowed to report its statistics if fewer than 16 students actually took the test. The student's scores are still factored into the "Overall_Mean_Score", which I did use.</p>

<p><b>District_Mobility: "Organization_Name", dropped</b><br> after merge with main_data - BOCES Board of cooperative education services.They are regional support entities for schools- mainly rural.</p>

<p><b>Grad_District_Rate: "All Students Final Grad Base'", merged</b><br> This is a count of all eligible students to graduate in the 12th grade, or who are ready to graduate in less than four years.</p>

<p><b>Grad_District_Rate: "All Students Completion Rate'", dropped</b><br> A ratio of students who receive a diploma after spending five or more years in a high school.</p>  

### Strategy to Create a Main_DataFrame

1. Dropped redundant features or features that were inclusive of others in a single dataframe (each frame contained between 50 and 125 features, so parsing was a big deal). Used discretion when choosing to include a feature in the Main_DataFrame.
  - ran simple models of some features of question to determine if they were inclusive or collinery with another item I'd chosen.<br>
  *An example of this was when I thought that expulsion counts would be related to Referrals_to_Law_Enforcement but not Total_In_School or Total_Out_of_School_Suspensions*<br>
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

6. With such extreme scales amongst features I standardized the data, then split it into a training and test set.

### Modeling

 Ran an OLS summary on the training set:
<br>
<img src="/Users/haven/galvanize/capstone_1/OLS Summary for Train Data.png">
