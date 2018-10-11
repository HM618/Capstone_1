import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np
import missingno as msno
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr
import statsmodels.api as sm
import statsmodels.formula.api as smf
# import plotly.plotly as py
# from plotly.graph_objs import *
from sklearn.preprocessing import scale
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from pandas import plotting
from statsmodels.graphics.factorplots import interaction_plot
import statsmodels.stats.diagnostic as ssd
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.diagnostic import het_goldfeldquandt
#from fancyimpute import SimpleFill, KNN,  IterativeSVD, IterativeImputer


def clean_data(dataset):
    pd.set_option('max_columns', 100)

    #load Discipline Action by Gender (DAG) data
    df_da = pd.read_excel("Discipline Action by Gender.xlsx")
    # this dataset has 16 columns len(df_da.columns) and 557 rows df_da.shape[0]

    #make changes to DAG and save as new df
    discipline_action = df_da.copy()
    cols = discipline_action.columns.tolist()
    cols = [col.replace(' ', '_') for col in cols]
    discipline_action.columns = cols
    discipline_action['Expulsion'] = discipline_action['Expulsion_With_Services'] + discipline_action['Expulsion_Without_Services']
    #Jane says: can you turn the next 8 lines into a for loop? i.e., make a list of variables you want to drop, then iterate through that list, using the 'drop' command
    discipline_action.drop('Expulsion_With_Services', inplace=True, axis=1)
    discipline_action.drop('Expulsion_Without_Services', inplace=True, axis=1)
    discipline_action.drop('Gender', inplace=True, axis=1)
    discipline_action.drop('Classroom_Removal', inplace=True, axis=1)
    discipline_action.drop('Received_One_Out_of_School_Suspension', inplace=True, axis=1)
    discipline_action.drop('Received_Multiple_Out_of_School_Suspension', inplace=True, axis=1)
    discipline_action.drop('Referrals_to_Law_Enforcement', inplace=True, axis=1)
    discipline_action.drop('Unduplicated_Count_of_Students_Disciplined', inplace=True, axis=1)
    county_obj = discipline_action.groupby('County_Name')
    #gender = df2_da.get_dummies(df2_da.Gender, prefix='Gender')
    #df2_da = df.replace(['inf', '-inf'], np.nan)
    #df2_da.dropna()

    #msno.heatmap(df2_da) to check for nan values
    #plt.show()

    #check for mulitcollinearity amongst variables
    y = discipline_action['Expulsion']
    x = discipline_action[['In_School_Suspension', 'Total_Out_of_School_Suspensions','School_Related_Arrest']]

    discipline_model = sm.OLS(endog=y, exog= x, missing='drop').fit()
    discipline_model.summary()
    # after running the above summary, decide to drop 'Referrals_to_Law_Enforcement' as it shows potential for collinearity

    discipline_action = discipline_action[['County_Code', 'County_Name', 'District_Code', 'District_Name', 'Expulsion', 'In_School_Suspension', 'Total_Out_of_School_Suspensions','School_Related_Arrest', 'Other_Action']]

    #discipline_model2 = sm.OLS(endog=y, exog= x, missing='drop').fit()
    #discipline_model2.summary(print)

    #discipline = df2_da[['County_Code', 'County Name', 'District_Code', 'District_Name', 'Gender', '']]

    #load in Graduation Stats for 2017
    df_grad = pd.read_csv('2017-Grad-District-Race.csv', encoding='ISO-8859-1')
    #df_grad.rename(columns={'Organization Name' : 'District Number'}, inplace=True)
    #select relevant variables and replace spaces with underscores
    grad = df_grad[['County Name', 'Organization Code', 'Organization Name', 'All Students Final Grad Base', 'All Students Graduates Total', 'All Students Completers Total', 'All Students Graduation Rate']]
    cols = grad.columns.tolist()
    cols = [col.replace(' ', '_') for col in cols]
    grad.columns = cols
    grad = grad.dropna()
    grad.rename(columns={'Organization_Code': 'District_Number'}, inplace=True)



    #load in PSAT/SAT scores
    df_st_results = pd.read_csv('2017 SAT PSAT Ted Results_.csv', encoding='ISO-8859-1')

    #select relevant variables and rename them
    standardized_scores = df_st_results[['Test', 'District Number', 'District Name', 'School Name', 'Overall Mean Score', 'Valid Scores']]
    cols = standardized_scores.columns.tolist()
    cols = [col.replace(' ', '_') for col in cols]
    standardized_scores.columns = cols
    standardized_scores = standardized_scores.reindex(columns=cols)
    #change data types in appropriate columns (all columns were imported as 'object' datatypes)
    standardized_scores['Overall_Mean_Score'] = standardized_scores['Overall_Mean_Score'].astype(int)
    standardized_scores = standardized_scores.dropna()



    df_mobility = pd.read_csv('2017 District Mobility .csv', encoding='ISO-8859-1')

    mobility_rates = df_mobility[['Organization Name', 'Homeless Student Mobility Rate', 'Economically Disadvantaged Student Mobility Rate', 'English Language Learners Student Mobility Rate']]
    cols = mobility_rates.columns.tolist()
    cols = [col.replace(' ', '_') for col in cols]
    mobility_rates.columns = cols
    mobility_rates = mobility_rates.dropna()


    # mobility_rates['Homeless_Student_Mobility_Rate'] = mobility_rates['Homeless_Student_Mobility_Rate'].astype(int)

    #merge
    #Jane says: similar to comment above about 'drop', can the merging be automatized? e.g., using for loop(s)? 
    df_main = standardized_scores.merge(discipline_action, on='District_Name', how='outer')
    df_main = df_main.merge(grad, on='District_Number', how='outer')
    df_main = df_main.merge(mobility_rates, on='Organization_Name', how='outer')
    #df_main = df_main.set_index('District_Number')
    df_main = df_main[['District_Number','All_Students_Graduation_Rate','Overall_Mean_Score', 'Expulsion', 'In_School_Suspension','Total_Out_of_School_Suspensions', 'Other_Action','All_Students_Final_Grad_Base','Homeless_Student_Mobility_Rate', 'Economically_Disadvantaged_Student_Mobility_Rate']]
    df_main['Grad_Rate'] = df_main['All_Students_Graduation_Rate']
    df_main['SAT_Scores'] = df_main['Overall_Mean_Score']
    df_main['Suspension'] = df_main['In_School_Suspension'] + df_main['Total_Out_of_School_Suspensions']
    df_main['Total_Eligible_Grads'] = df_main['All_Students_Final_Grad_Base']
    df_main = df_main.dropna()

### I would suggest adding an-  if '__name__' == '__main__':
###  This may make the script a little cleaner

#turn dataset into flat viewable object
main_data = pd.read_excel('output.xlsx')

y = main_data['Grad_Rate'].values
X = main_data[['SAT_Scores','Expulsion', 'Suspension', 'Other_Action','Total_Eligible_Grads', 'Homeless_Student_Mobility_Rate', 'Economically_Disadvantaged_Student_Mobility_Rate']].values

#standardize the data since each feature is scaled differently

standardize = StandardScaler()
X_standardized = standardize.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X,y)

train_model = sm.OLS(endog=y_train, exog= X_train, missing='drop').fit()
train_model.summary()

test_model = sm.OLS(endog=y_test, exog= X_test, missing='drop').fit()
test_model.summary()

linreg = LinearRegression()

#fit model to training data
linreg.fit(X_train, y_train)

# get and print the y intercept
print('The y intercept is', linreg.intercept_)
# get and print the coefficients of features in the order they appear in df
print('The coefficients for each feature are:', linreg.coef_)
#assign column names to a variable for easy access
features = ['SAT_Scores','Expulsion', 'Suspension', 'Other_Action','Total_Eligible_Grads', 'Homeless_Student_Mobility_Rate', 'Economically_Disadvantaged_Student_Mobility_Rate']
#bring the features are their respective coefficients together
zip(features, linreg.coef_)

y_predicted = linreg.predict(X_test)
#print('The predicted y values based on our test model are:', y_predicted)

#get the RMSE (ie square root of the variance of the residuals)
print('Our rmse is', np.sqrt(metrics.mean_squared_error(y_test, y_predicted)))

X_plot = np.arange(0,len(y_test))
fig = plt.figure(figsize=(8,8))
fig.suptitle('Predicted versus True Rates')
plt.scatter(X_plot,y_test,c='b')
plt.scatter(X_plot,y_predicted, c='m', alpha=0.5)
plt.ylabel('Graduation Rates')
plt.show()
