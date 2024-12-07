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

## Dependencies
- [Docker](https://www.docker.com/) 
- [VS Code](https://code.visualstudio.com/download)
- [VS Code Jupyter Extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)

## Usage

### Setup

> If you are using Windows or Mac, make sure Docker Desktop is running.

1. Clone this GitHub repository (git clone repo URL)

### Running the analysis

1. Navigate to the root of this project on your computer using the
   command line and enter the following command:

``` 
docker compose up --build
```

2. In the terminal, look for a URL that starts with 
`http://127.0.0.1:8888/lab?token=` 

3. From the root of the project run the following commands:

```
# Step 1: Download the dataset

python scripts/download_data.py \
    --url="https://archive.ics.uci.edu/static/public/863/maternal+health+risk.zip" \
    --write_to=data/raw

# Step 2: Splitting the data and data validation
python scripts/valid_split.py \
    --raw-data=data/raw/"Maternal Health Risk Data Set.csv" \
    --data-dest=data/processed

# Step 3: Running the EDA

python scripts/eda.py \
    --processed-training-data=data/processed/train_df.csv \
    --plot-to=results/figures \
    --table-to=results/tables

# Step 4: Fitting the models on train set
python scripts/fit_classifier.py \
    --training-data=data/processed/train_df.csv \
    --best_model_to=results/models \
    --tbl_to=results/tables

# Step 5: Evaluate the model on test set
python scripts/evaluate_classifier.py \
    --test_data=data/processed/test_df.csv \
    --best_model_from=results/models/dt_tuned_fit.pickle \
    --plot_to=results/figures \
    --tbl_to=data/processed

quarto render reports/maternal_health_classification.qmd --to html
quarto render report/maternal_health_classification.qmd --to pdf
```

### Clean up

1. To shut down the container and clean up the resources, 
type `Cntrl` + `C` in the terminal
where you launched the container, and then type `docker compose rm`

## Developer notes

### Developer dependencies
- `conda` (version 23.9.0 or higher)
- `conda-lock` (version 2.5.7 or higher)

### Adding a new dependency

1. Add the dependency to the `environment.yaml` file on a new branch.

2. Run `conda-lock -k explicit --file environment.yaml -p linux-64` to update the `conda-linux-64.lock` file.

2. Re-build the Docker image locally to ensure it builds and runs properly.

3. Push the changes to GitHub. A new Docker
   image will be built and pushed to Docker Hub automatically.
   It will be tagged with the SHA for the commit that changed the file.

4. The `docker-compose.yml` file will be updated automatically with GitHub Actions.
   
5. Send a pull request to merge the changes into the `main` branch. 

# License
The Maternal Health Risk report contained herein are licensed under the [Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License](https://creativecommons.org/licenses/by-nc-sa/4.0/). 
See the [license file](https://github.com/UBC-MDS/maternal_health_classification/blob/main/LICENSE.md) for more information. . If re-using/re-mixing please provide attribution and link to this webpage. 
The software code contained within this repository is licensed under the MIT license. See the [license file](https://github.com/UBC-MDS/maternal_health_classification/blob/main/LICENSE.md) for more information.

# References

Pima Indians Diabetes Database, https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.names, 22 Nov 2024. 

Dua, Dheeru, and Casey Graff. 2017. “UCI Machine Learning Repository.” University of California, Irvine, School of Information; Computer Sciences. http://archive.ics.uci.edu/ml.

Ahmed, M., Kashem, M.A., Rahman, M., and S. Khatun. 2020. “Review and Analysis of Risk Factor of Maternal Health in Remote Area Using the Internet of Things(IoT)” Published in Lecture Notes in Electrical Engineering, vol 632. https://doi.org/10.24432/C5DP5D.
