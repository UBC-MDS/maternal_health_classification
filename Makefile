.PHONY: all clean

all: reports/maternal_health_classification.html reports/maternal_health_classification.pdf

# Download and extract data from zip
data/raw/Maternal Health Risk Data Set.csv: scripts/download_data.py
	python scripts/download_data.py \
    	--url="https://archive.ics.uci.edu/static/public/863/maternal+health+risk.zip" \
    	--write_to=data/raw

# Splitting the data and data validation
data/processed/test_df.csv data/processed/train_df.csv data/processed/scaled_test_df.csv data/processed/scaled_train_df.csv: scripts/valid_split.py data/raw/Maternal Health Risk Data Set.csv
	python scripts/valid_split.py \
		--raw-data=data/raw/"Maternal Health Risk Data Set.csv" \
		--data-dest=data/processed

# Running the EDA
results/figures/boxplot_by_risk_level.png results/figures/countplot_of_risk_level.png results/figures/heatmap_of_the_maternal_health.png results/tables/df_describe.csv results/tables/df_info.csv results/tables/df_shape.csv: scripts/eda.py data/processed/train_df.csv
	python scripts/eda.py \
		--processed-training-data=data/processed/train_df.csv \
		--plot-to=results/figures \
		--table-to=results/tables

# Fitting the models on train set
results/models/dt_tuned_fit.pickle results/tables/summary_cv_scores.csv: scripts/fit_classifier.py data/processed/train_df.csv
	python scripts/fit_classifier.py \
		--training-data=data/processed/train_df.csv \
		--best_model_to=results/models \
		--tbl_to=results/tables

# Evaluate the model on test set
results/figures/confusion_matrix.png results/figures/decision_tree.png results/tables/confusion_matrix.csv results/tables/test_score.csv: scripts/evaluate_classifier.py \
data/processed/test_df.csv \
results/models/dt_tuned_fit.pickle
	python scripts/evaluate_classifier.py \
		--test_data=data/processed/test_df.csv \
		--best_model_from=results/models/dt_tuned_fit.pickle \
		--plot_to=results/figures \
		--tbl_to=results/tables

# build HTML and PDF report
reports/maternal_health_classification.html reports/maternal_health_classification.pdf: reports/maternal_health_classification.qmd \
reports/references.bib \
results/tables/df_describe.csv \
results/tables/df_info.csv \
results/tables/df_shape.csv \
results/figures/countplot_of_risk_level.png \
results/figures/heatmap_of_the_maternal_health.png \
results/figures/boxplot_by_risk_level.png \
results/tables/summary_cv_scores.csv \
results/models/dt_tuned_fit.pickle \
results/tables/test_score.csv \
results/tables/confusion_matrix.csv \
results/figures/confusion_matrix.png \
results/figures/decision_tree.png
	quarto render reports/maternal_health_classification.qmd --to html
	quarto render reports/maternal_health_classification.qmd --to pdf

# Clean up all the analysis
clean:
	rm -rf data/raw \
	rm -r data/processed/* \
    rm -r results/figures/* \
    rm -r results/models/* \
    rm -r results/tables/* \
    rm -rf reports/maternal_health_classification.html \
		reports/maternal_health_classification.pdf \
		reports/maternal_health_classification_files


	