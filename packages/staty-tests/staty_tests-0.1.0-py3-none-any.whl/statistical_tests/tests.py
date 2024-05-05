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
            if len(unique_groups) == 1:  # Check if there's only one group
                print(f"Skipping {group_var} as it has only one group.")
                continue
                
            grouped_data = [data[data[group_var] == group][dependent_variable] for group in unique_groups]
            f_statistic, p_value = f_oneway(*grouped_data)
                
            # Calculate proportions of each group
            group_sizes = [len(group) for group in grouped_data]
            total_size = sum(group_sizes)
            group_labels = [f"{group_var}={group}" for group in unique_groups]  # Labels for each group
            group_proportions = [(size / total_size, label) for size, label in zip(group_sizes, group_labels)]
                
            results.append({
                'Dependent Variable': dependent_variable,
                'Group Variable': group_var,
                'F-Statistic': f_statistic,
                'P-value': p_value,
                'Proportions': group_proportions
            })
        
        # Print results in a table
        if results:
            result_table = pd.DataFrame(results)
            print("One-Way ANOVA Results:")
            print(tabulate(result_table, headers='keys', tablefmt='pretty', showindex=False))
        else:
            print("No valid group variables found to perform ANOVA.")

    def chi_square(self, var1, var2):
        # Create contingency table
        contingency_table = pd.crosstab(self.dataframe[var1], self.dataframe[var2])
        
        # Perform chi-square test
        chi2_stat, p_value, _, _ = chi2_contingency(contingency_table)
        
        # Print results
        result_table = pd.DataFrame({
            'Variable 1': [var1],
            'Variable 2': [var2],
            'Chi-Square Statistic': [chi2_stat],
            'P-value': [p_value]
        })
        print("Chi-Square Test Results:")
        print(tabulate(result_table, headers='keys', tablefmt='pretty', showindex=False))
