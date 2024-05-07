# Statistical Tests

Statistical Tests is a Python library for performing common statistical tests such as one-way ANOVA and chi-square test.

## Installation

You can install the library via pip:


## Usage

```python
from statistical_tests.tests import StatisticalTests
import pandas as pd

# Create an instance of StatisticalTests with your dataframe
dataframe = pd.read_csv('your_data.csv')
tests = StatisticalTests(dataframe)

# Perform one-way ANOVA
tests.one_way_anova('dependent_variable', 'group_variable1', 'group_variable2')

# Perform chi-square test
tests.chi_square('variable1', 'variable2', 'variable3')
