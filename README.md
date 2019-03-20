## Data analysis & visualization - House of Representatives expenditures

I analyzed expenses for members of the US House of Representatives to see how priorities adjusted during an election year (2018). As shown below, during the start of the reelection period (Q3 of 2018) the expense priorities shifted. The three categories that had the most significant increase from Q1 to Q3 were 1) Printing & Reproduction, 2) Franked Mail (mail to their constituents) and 3) Travel. This shift in priorities is due to the election year where the US House Members are focused on getting reelected for another 2 years.

The data I used for this project is from projects.propublica.org, which is based on expenditure reports published directly from the House. I downloaded the three most current data files for 2018 (Q1-2018, Q2-2018, Q3-2018). Unfortunately, data for Q4 2018 is not yet available. It would have been helpful to have Q4 data to analyze if the trends I outlined continued through election day. 

After organizing the data, I created a pie chart to give an overview of expenses categories. The top three categories include: 
- Personnel compensation (accounts for over 75% of total expenses)
- Rent, Communication, Utilities
- Travel 

![chart_expense_categories](https://user-images.githubusercontent.com/40340806/54649502-db7a3780-4a80-11e9-8eda-fa5f9102c39e.png)


The code snippet below shows how I merged the Q1 & Q3 data, found the percent increase for each cateogory, and then cleaned up the column names and sorted the data. The table below shows a cleaned up version of the output.

```python
comparison_Q1_Q3 = q1_data.merge(q3_data, on='CATEGORY', suffixes=['_Q1', '_Q3'])
comparison_Q1_Q3['percent_increase'] = comparison_Q1_Q3.apply(lambda row: round((row.AMOUNT_Q3 - row.AMOUNT_Q1)/row.AMOUNT_Q1,3), axis=1)

percent_increase_df = comparison_Q1_Q3[['CATEGORY', 'AMOUNT_Q1', 'AMOUNT_Q3', 'percent_increase']]
percent_increase_df.columns = ["Expense Category", "Q1 Total Expenses", "Q3 Total Expenses", "% Increase in Total Expenses"]
percent_increase_df = percent_increase_df.sort_values(by=['% Increase in Total Expenses'], ascending=False).reset_index(drop=True)
```

This table shows the % change in total expenses from Q1 to Q3. The top three expense cateogires (based on % change in the total expenses) are 1) Printing & Reproduction, 2) Franked Mail (mail to their constituents) and 3) Travel

![Screen Shot 2019-03-20 at 9 19 28 AM](https://user-images.githubusercontent.com/40340806/54687329-b540b000-4af1-11e9-8ae1-7c039b000536.png)


This table shows the how the individual expense cateogry each represent a portion of the total expenses from Q1 to Q3. The top three expense cateogires (based on overall % change in the total propotion of expenses) are 1) Printing & Reproduction, 2) Franked Mail (mail to their constituents) and 3) Travel

![Screen Shot 2019-03-20 at 9 55 03 AM](https://user-images.githubusercontent.com/40340806/54689647-55003d00-4af6-11e9-8892-2f4ef8dc0366.png)


The top 3 spenders for Quarter 3 in 2018 were Tom MacArthur, Steve Knight, Randy Hultgren. All three of these former congressman had a very tight race in their elections, but all ended up losing. These very close reelection campaigns in Q3 2018 account for the spike in expenses.

![Screen Shot 2019-03-20 at 10 15 13 AM](https://user-images.githubusercontent.com/40340806/54691380-86c6d300-4af9-11e9-9111-26c10754d38d.png)
