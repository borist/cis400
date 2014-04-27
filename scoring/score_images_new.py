from __future__ import division

import sys
import csv
import numpy as np
import pandas as pd
import statsmodels.api as sm


def run_regression(csv_url):
    """
    helpful links:
    http://blog.yhathq.com/posts/logistic-regression-and-python.html
    http://statsmodels.sourceforge.net/stable/examples/generated/example_discrete.html?highlight=multinomial
    """

    # Load data
    data = pd.read_csv(csv_url)
    print data

    x_cols = data.columns[2:]
    #x_cols = data.columns[2:4]

    # run the regression
    mn_logit = sm.MNLogit(data['overall_score'], data[x_cols])
    results = mn_logit.fit()

    # inspect the results
    print results.summary()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "usage: python score_images.py <merged manual and auto scores>.csv"

    run_regression(sys.argv[1])
