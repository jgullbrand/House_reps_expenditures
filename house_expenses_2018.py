from matplotlib import pyplot as plt
import pandas as pd
import glob

files = glob.glob('data_files/2018*.csv')

data_files = []
for file in files:
	data = pd.read_csv(file)
	data_files.append(data)

data_2018 = pd.concat(data_files).reset_index(drop=True)	
#print(data_2018.head()) # prints first 5 rows

#Totals Grouped by member, expense category and quarters
member_totals = data_2018.groupby('OFFICE').AMOUNT.sum() # gives the total expenses for each member of the House
category_totals = data_2018.groupby('CATEGORY').AMOUNT.sum().reset_index() # gives the total expenses for each category
quarter_totals = data_2018.groupby('QUARTER').AMOUNT.sum() # gives the total expenses for each quarter

#Data filtered by Quarter
q1_data = data_2018[data_2018.QUARTER == 'Q1'].groupby('CATEGORY').AMOUNT.sum().reset_index()
q2_data = data_2018[data_2018.QUARTER == 'Q2'].groupby('CATEGORY').AMOUNT.sum().reset_index()
q3_data = data_2018[data_2018.QUARTER == 'Q3'].groupby('CATEGORY').AMOUNT.sum().reset_index()


#Pie Chart for category totals
def print_pie_chart():
	sort_category_totals = category_totals.sort_values(by=['AMOUNT'], ascending=False)
	plt.pie(sort_category_totals['AMOUNT'])
	plt.legend(sort_category_totals['CATEGORY'], loc = "upper left")
	plt.axis('equal')
	plt.title('Top Expense Categories for the US House of Reps (Q1, Q2, Q3 2018)')
	plt.show() # displays chart
	plt.close('all') # this clears out the previous plot in case I decide to include other charts below


# table_Q1_Q3_increase.csv - Amounts for Q1 and Q3 and the percentage increase
def calc_percent_increase():
	comparison_Q1_Q3 = q1_data.merge(q3_data, on='CATEGORY', suffixes=['_Q1', '_Q3'])
	comparison_Q1_Q3['percent_increase'] = comparison_Q1_Q3.apply(lambda row: round((row.AMOUNT_Q3 - row.AMOUNT_Q1)/row.AMOUNT_Q1,3), axis=1)

	percent_increase_df = comparison_Q1_Q3[['CATEGORY', 'AMOUNT_Q1', 'AMOUNT_Q3', 'percent_increase']]
	percent_increase_df.columns = ["Expense Category", "Q1 Total Expenses", "Q3 Total Expenses", "% Increase in Total Expenses"] #renaming the columns
	percent_increase_df = percent_increase_df.sort_values(by=['% Increase in Total Expenses'], ascending=False).reset_index(drop=True)
	percent_increase_df.to_csv('table_Q1_Q3_increase.csv')


# table_Q1_Q3_expense_proportions.csv - The proportion of expenses based on categories from Q1 to Q3
def calc_proportions():
	q1_sum = q1_data.AMOUNT.sum()

	def q1_calc_percentage(num):
		return round(num/q1_sum,3)
	q1_data['Q1_percentage_of_total'] = q1_data['AMOUNT'].apply(q1_calc_percentage)

	q3_sum = q3_data.AMOUNT.sum()
	def q3_calc_percentage(num):
		return round(num/q3_sum,3)
	q3_data['Q3_percentage_of_total'] = q3_data['AMOUNT'].apply(q3_calc_percentage)

	comparison_Q1_Q3_percentage = q1_data.merge(q3_data, on='CATEGORY', suffixes=['_Q1', '_Q3'])
	comparison_Q1_Q3_percentage['percent_difference_of_total'] = comparison_Q1_Q3_percentage.apply(lambda row: round(row.Q3_percentage_of_total - row.Q1_percentage_of_total,3), axis=1)
	comparison_Q1_Q3_percentage = comparison_Q1_Q3_percentage[['CATEGORY', 'Q1_percentage_of_total', 'Q3_percentage_of_total', 'percent_difference_of_total']]
	comparison_Q1_Q3_percentage.columns = ["Expense Category", "Q1 - percentage of total expenses", "Q3 - percentage of total expenses", "change in proportion of expenses"] #renaming the columns
	comparison_Q1_Q3_percentage = comparison_Q1_Q3_percentage.sort_values(by=["change in proportion of expenses"], ascending=False).reset_index(drop=True)
	comparison_Q1_Q3_percentage.to_csv('table_Q1_Q3_expense_proportions.csv')


# Top 3 Spenders (cumulative of Q1, Q2, Q3)
def top_three_cum():
	top_member_totals = data_2018.groupby('OFFICE').AMOUNT.sum().reset_index()
	top_three_spenders = top_member_totals.sort_values(by=['AMOUNT'], ascending=False).head(3).reset_index()
	print(top_three_spenders)


# Top 3 spenders (Based on Q3)
def top_three_q3():
	q1_top_member_total = data_2018[data_2018.QUARTER == 'Q1'].groupby('OFFICE').AMOUNT.sum().reset_index()
	q3_top_member_total = data_2018[data_2018.QUARTER == 'Q3'].groupby('OFFICE').AMOUNT.sum().reset_index()
	merged_data_Q1_Q3 = q1_top_member_total.merge(q3_top_member_total, on='OFFICE', suffixes=['_Q1', '_Q3'])
	merged_data_Q1_Q3 = merged_data_Q1_Q3[['OFFICE', 'AMOUNT_Q1', 'AMOUNT_Q3']] # removing other columns
	merged_data_Q1_Q3['total_amount_increase'] = merged_data_Q1_Q3.apply(lambda row: round((row.AMOUNT_Q3 - row.AMOUNT_Q1),3), axis=1)
	merged_data_Q1_Q3['percent_increase'] = merged_data_Q1_Q3.apply(lambda row: round((row.AMOUNT_Q3 - row.AMOUNT_Q1)/row.AMOUNT_Q1,3), axis=1)
	top_three_spenders_q3 = merged_data_Q1_Q3.sort_values(by=['AMOUNT_Q3'], ascending=False).head(3).reset_index(drop=True)
	top_three_spenders_q3.to_csv('Q3_top_three_spenders.csv')
	print(top_three_spenders_q3)


# print_pie_chart()
# calc_percent_increase()
# calc_proportions()
# top_three_cum()
# top_three_q3()
