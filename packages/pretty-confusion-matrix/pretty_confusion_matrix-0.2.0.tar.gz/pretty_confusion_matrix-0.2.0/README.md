# Confusion Matrix in Python
Plot a pretty confusion matrix (like Matlab) in python using seaborn and matplotlib

Created on Mon Jun 25 14:17:37 2018
@author: Wagner Cipriano - wagnerbhbr


This module get a pretty print confusion matrix from a NumPy matrix or from 2 NumPy arrays (`y_test` and `predictions`).

## Installation
```bash
pip install pretty-confusion-matrix
```

## Get Started

Examples:
```python
import numpy as np
import pandas as pd
from pretty_confusion_matrix import pp_matrix

array = np.array([[13,  0,  1,  0,  2,  0],
                  [0, 50,  2,  0, 10,  0],
                  [0, 13, 16,  0,  0,  3],
                  [0,  0,  0, 13,  1,  0],
                  [0, 40,  0,  1, 15,  0],
                  [0,  0,  0,  0,  0, 20]])

# get pandas dataframe
df_cm = pd.DataFrame(array, index=range(1, 7), columns=range(1, 7))
# colormap: see this and choose your more dear
cmap = 'PuRd'
pp_matrix(df_cm, cmap=cmap)
```
![alt text](https://raw.githubusercontent.com/khuyentran1401/pretty-print-confusion-matrix/master/Screenshots/Conf_matrix_default.png)

```python
import numpy as np
from pretty_confusion_matrix import pp_matrix_from_data

y_test = np.array([1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2,
                  3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5])
predic = np.array([1, 2, 4, 3, 5, 1, 2, 4, 3, 5, 1, 2, 3, 4, 4, 1, 4, 3, 4, 5, 1, 2, 4, 4, 5, 1, 2, 4, 4, 5, 1, 2, 4, 4, 5, 1, 2, 4, 4, 5, 1, 2, 3, 3, 5, 1, 2, 3, 3, 5, 1, 2,
                  3, 4, 4, 1, 2, 3, 4, 1, 1, 2, 3, 4, 1, 1, 2, 3, 4, 1, 1, 2, 4, 4, 5, 1, 2, 4, 4, 5, 1, 2, 4, 4, 5, 1, 2, 4, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5])

pp_matrix_from_data(y_test, predic)
```

![alt text](https://raw.githubusercontent.com/khuyentran1401/pretty-print-confusion-matrix/master/Screenshots/Conf_matrix_default_2.png)



## References:
### 1. MATLAB confusion matrix:

a) [Plot Confusion](https://www.mathworks.com/help/nnet/ref/plotconfusion.html)
   
b) [Plot Confusion Matrix Using Categorical Labels](https://www.mathworks.com/help/examples/nnet/win64/PlotConfusionMatrixUsingCategoricalLabelsExample_02.png)



### 2. Examples and more on Python:

  a) [How to plot confusion matrix with string axis rather than integer in python](https://stackoverflow.com/questions/5821125/how-to-plot-confusion-matrix-with-string-axis-rather-than-integer-in-python/51176855#51176855)
  
  b) [Plot-scikit-learn-classification-report](https://stackoverflow.com/questions/28200786/how-to-plot-scikit-learn-classification-report)
  
  c) [Plot-confusion-matrix-with-string-axis-rather-than-integer-in-Python](https://stackoverflow.com/questions/5821125/how-to-plot-confusion-matrix-with-string-axis-rather-than-integer-in-python)
  
  d) [Seaborn heatmap](https://www.programcreek.com/python/example/96197/seaborn.heatmap)
  
  e) [Sklearn-plot-confusion-matrix-with-labels](https://stackoverflow.com/questions/19233771/sklearn-plot-confusion-matrix-with-labels/31720054)

  f) [Model-selection-plot-confusion-matrix](http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html#sphx-glr-auto-examples-model-selection-plot-confusion-matrix-py)

