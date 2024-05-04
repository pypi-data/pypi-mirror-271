from scipy.stats import f_oneway, chi2_contingency
import pandas as pd
from itertools import combinations
from tabulate import tabulate

class StatisticalTests:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def one_way_anova(self, dependent_variable, *group_variables):
        # Drop rows with NaN values in the dependent variable and group variables
        data = self.dataframe[[dependent_variable, *group_variables]].dropna()
        
        # Perform one-way ANOVA for each group variable
        results = []
        for group_var in group_variables:
            unique_groups = data[group_var].unique()
            if len(unique_groups) > 1:  # Check if there's more than one group
                grouped_data = [data[data[group_var] == group][dependent_variable] for group in unique_groups]
                f_statistic, p_value = f_oneway(*grouped_data)
                results.append([group_var, f_statistic, p_value])
            else:
                print(f"Skipping {group_var} as it has only one group.")
        
        # Print results in a table
        if results:
            result_table = pd.DataFrame(results, columns=['Group Variable', 'F-Statistic', 'P-value'])
            print("One-Way ANOVA Results:")
            print(tabulate(result_table, headers='keys', tablefmt='pretty', showindex=False))
        else:
            print("No valid group variables found to perform ANOVA.")

    def chi_square(self, *variables):
        # Create all possible pairs of variables
        pairs = combinations(variables, 2)
        
        # Perform chi-square test for each pair
        results = []
        for var1, var2 in pairs:
            # Create contingency table
            contingency_table = pd.crosstab(self.dataframe[var1], self.dataframe[var2])
            
            # Perform chi-square test
            chi2_stat, p_value, _, _ = chi2_contingency(contingency_table)
            results.append([var1, var2, chi2_stat, p_value])
        
        # Print results in a table
        if results:
            result_table = pd.DataFrame(results, columns=['Variable 1', 'Variable 2', 'Chi-Square Statistic', 'P-value'])
            print("Chi-Square Test Results:")
            print(tabulate(result_table, headers='keys', tablefmt='pretty', showindex=False))
        else:
            print("No valid pairs of variables found to perform chi-square test.")
