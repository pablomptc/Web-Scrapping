import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

df = pd.read_csv ("Asociación.csv")

frequent_itemsets = apriori(df > 0, min_support = 0.06, use_colnames = True)
rules = association_rules (frequent_itemsets, metric = "confidence", min_threshold = 0.8)
rules = association_rules (frequent_itemsets, metric = "lift", min_threshold = 1)
rules.to_csv ("asociation.csv")
