import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

dfControl= pd.read_excel("ABTesti-StudyCase/ABTesti/ab_testing.xlsx","Control Group")
dfTest= pd.read_excel("ABTesti-StudyCase/ABTesti/ab_testing.xlsx","Test Group")
dfControl.head()
dfTest.head()
dfControl.describe().T
dfTest.describe().T
dfControl["group"]="Control"
dfTest["group"]="Test"
df= pd.concat([dfControl,dfTest],axis=0,ignore_index=True)

## Hipotezi Tanımlama

# H0 : M1 = M2   Maximum Bidding ve average bidding arasında fark yoktur
# H1 : M1!= M2   fark vardır
df.groupby("group").agg({"Purchase": "mean"})

## Varsayım kontrol
## 1. Normallik
# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır.
# p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ
test_stat, pvalue = shapiro(df.loc[df["group"] == "Control", "Purchase"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))   # p-value = 0.5891
test_stat, pvalue = shapiro(df.loc[df["group"] == "Test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))   # p-value = 0.1541
## H0 reddilmez- Normal dağılım vardır

## Varyans Homojenliği
# H0: Varyanslar homojendir.
# H1: Varyanslar homojen Değildir.
# p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ

test_stat, pvalue = levene(df.loc[df["group"] == "Control", "Purchase"],
                           df.loc[df["group"] == "Test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))   # p-value = 0.1083
# H0 reddedilemez. Dağılım homojendir

## Varsayımlar sağlandığı için parametrik yöntem uygulanacak.
test_stat, pvalue = ttest_ind(df.loc[df["group"] == "Control", "Purchase"],
                              df.loc[df["group"] == "Test", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#  p-value = 0.3493 H0 reddedilemez.
#   Maximum Bidding ve average bidding arasında fark yoktur









