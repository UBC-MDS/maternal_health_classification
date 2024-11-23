# Maternal Health Classification
authors: Shannon Pflueger, Nelli Hovhannisyan, Joseph Lim

# About
In this project we are comparing multiple classification models to predict pregnant women's maternal health risk as low, medium or high from their health data. With our chosen model
we aim to identify some key indicators that predict higher maternal health risk. In rural communities where it is costly and difficult to provide consistent medical care, having a method to predict 
maternal health risk from minimally invasive methods could be greatly beneficial in improving health outcomes for mothers and babies alike.
After some initial exploration of classification models we settled on the Decision Tree algorithm for its easily interpretable model and relatively high accuracy score. 
Based on this Decision Tree model a key indicator of increased maternal health risk was blood sugar. The decision tree our model built based on the dataset suggests that blood sugar higher than 7.95 mmol/l
is correlated with a high maternal health risk. However, the model does seem to struggle with classifying low vs. medium maternal health risk.
While this is a great first step the model accuracy is not accurate enough to be used in a medical context yet. More research and modelling (perhaps with different models) should be done before deploying this technology in rural communities.
Additionally, it should be noted that since this dataset contains health data only from Pima Indians the model have may learned a bias specific to unknown genetic factors present in this sample. Thus, a much larger dataset with a diverse sample 
should be used to train the model before it is utilized in any communities.

The dataset used in this project was originally from the Pima Indians Diabetes Database. The dataset was sourced from the UCI Machine Learning Repository (Dua and Graff 2017) and can be found [here](https://archive.ics.uci.edu/dataset/863/maternal+health+risk), 
or more specifically [this file](https://archive.ics.uci.edu/static/public/863/maternal+health+risk.zip).
Classification for each observation in the dataset was done with help from Dr. Shirin Shabnam.

# Report
A link to our report will be added here when it is finished in a few weeks!

# License
The Maternal Health Risk report contained herein are licensed under the [Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License](https://creativecommons.org/licenses/by-nc-sa/4.0/). 
See the [license file](https://github.com/UBC-MDS/maternal_health_classification/blob/main/LICENSE.md) for more information. . If re-using/re-mixing please provide attribution and link to this webpage. 
The software code contained within this repository is licensed under the MIT license. See the [license file](https://github.com/UBC-MDS/maternal_health_classification/blob/main/LICENSE.md) for more information.

# References

Pima Indians Diabetes Database, https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.names, 22 Nov 2024. 

Dua, Dheeru, and Casey Graff. 2017. “UCI Machine Learning Repository.” University of California, Irvine, School of Information; Computer Sciences. http://archive.ics.uci.edu/ml.

Ahmed, M., Kashem, M.A., Rahman, M., and S. Khatun. 2020. “Review and Analysis of Risk Factor of Maternal Health in Remote Area Using the Internet of Things(IoT)” Published in Lecture Notes in Electrical Engineering, vol 632. https://doi.org/10.24432/C5DP5D.
