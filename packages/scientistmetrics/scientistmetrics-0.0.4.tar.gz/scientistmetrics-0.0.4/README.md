# scientistmetrics : python library for model metrics

## About scientistmetrics

scientistmetrics is a Python package for metrics and scoring : quantifying the quality of predictions

## Why scientistmetrics?

### Measure of association with categoricals variables

scientistmetrics provides the option for computing one of six measures of association between two nominal variables from the data given in a 2d contingency table:

* Chi - squard test : [https://en.wikipedia.org/wiki/Chi-squared_test](https://en.wikipedia.org/wiki/Chi-squared_test)
* Cramer's V : [https://en.wikipedia.org/wiki/Cram%C3%A9r%27s_V](https://en.wikipedia.org/wiki/Cram%C3%A9r%27s_V)
* Tschuprow's T : [https://en.wikipedia.org/wiki/Tschuprow%27s_T](https://en.wikipedia.org/wiki/Tschuprow%27s_T)
* G-test : [https://en.wikipedia.org/wiki/G-test](https://en.wikipedia.org/wiki/G-test)
* Phi coefficient : [https://en.wikipedia.org/wiki/Phi_coefficient](https://en.wikipedia.org/wiki/Phi_coefficient)
* Pearson contingence coefficient : [https://www.statisticshowto.com/contingency-coefficient/](https://www.statisticshowto.com/contingency-coefficient/)

### Classification metrics

scientistmetrics provides metrics for classification problem :

* accuracy score
* f1 score
* precision
* recall
* etc...

### Regression metrics

scientistmetrics provides metrics for regression problem :

* Rsquared
* Adjusted Rsquared
* Mean squared error
* etc...

### Powerset model

scientistmetrics provides a function that gives a set of all subsets model.

Notebook is availabled.

## Installation

### Dependencies

scientistmetrics requires :

```
python >=3.10
numpy >=1.26.4
pandas >=2.2.2
scikit-learn >=1.2.2
plotnine >=0.10.1
statsmodels >=0.14.0
scipy >=1.10.1
```

## User installation

You can install scientistmetrics using `pip` :

```
pip install scientistmetrics
```

## Author(s)

Duvérier DJIFACK ZEBAZE [duverierdjifack@gmail.com](mailto:duverierdjifack@gmail.com)