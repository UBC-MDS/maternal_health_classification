import os
import altair as alt
import pandas as pd

def create_heatmap(df_corr, plot_to):
    """Creates and saves a heatmap of correlations."""
    correlation_matrix = df_corr.corr().abs().round(2).reset_index().melt(
        id_vars='index', var_name='Variable', value_name='Correlation'
    )

    heatmap = alt.Chart(correlation_matrix).mark_rect().encode(
        x=alt.X('Variable:N', title='', sort=None),
        y=alt.Y('index:N', title='', sort=None),
        color=alt.Color('Correlation:Q', scale=alt.Scale(scheme='viridis'), title='Correlation')
    ).properties(
        width=600, height=400
    )

    text = alt.Chart(correlation_matrix).mark_text(baseline='middle').encode(
        x=alt.X('Variable:N', sort=None, axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('index:N', sort=None),
        text=alt.Text('Correlation:Q', format='.2f'),
        color=alt.condition('datum.Correlation > 0.5', alt.value('white'), alt.value('black'))
    ).properties(
        title="Heatmap of the Maternal Health"
    )

    final_chart = heatmap + text
    final_chart.save(os.path.join(plot_to, "heatmap_of_the_maternal_health.png"), scale_factor=2.0)


def create_countplot(df_eda, plot_to):
    """Creates and saves a countplot of risk levels."""
    chart = alt.Chart(df_eda).mark_bar(color='steelblue').encode(
        x=alt.X('RiskLevel', title='Risk Level', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('count()', title='Count'),
        color=alt.Color('RiskLevel:N', title='Risk Level')
    ).properties(
        title="Countplot of Risk Level",
        width=300, height=300
    )

    chart.save(os.path.join(plot_to, "countplot_of_risk_level.png"), scale_factor=2.0)


def create_boxplots(df_eda, plot_to):
    """Creates and saves boxplots for each feature grouped by risk levels."""
    columns = [col for col in df_eda.columns.tolist() if col != 'RiskLevel']
    boxplots = [
        alt.Chart(df_eda).mark_boxplot(extent='min-max').encode(
            x=alt.X('RiskLevel:N', title='Risk Level', axis=alt.Axis(labelAngle=0)),
            y=alt.Y(f'{col}:Q', title=col),
            color='RiskLevel:N'
        ).properties(
            title=f'Boxplot of {col} by RiskLevel',
            width=300, height=200
        )
        for col in columns
    ]

    boxplot_chart = alt.vconcat(*boxplots).resolve_scale(
        color='independent', y='independent'
    )
    boxplot_chart.save(os.path.join(plot_to, "boxplot_by_risk_level.png"), scale_factor=2.0)


def save_data_summaries(df_eda, df_corr, table_to):
    """Saves dataset summaries (info, describe, shape) to CSV files."""
    df_info = pd.DataFrame({
        "Column": df_eda.columns,
        "Non-Null Count": [df_eda[col].count() for col in df_eda.columns],
        "Data Type": [df_eda[col].dtype for col in df_eda.columns]
    })
    df_info.to_csv(os.path.join(table_to, "df_info.csv"), index=False)

    df_describe = df_corr.describe().transpose()
    df_describe.to_csv(os.path.join(table_to, "df_describe.csv"), index=False)

    df_shape = pd.DataFrame({"Metric": ["Rows", "Columns"], "Value": [df_eda.shape[0], df_eda.shape[1]]})
    df_shape.to_csv(os.path.join(table_to, "df_shape.csv"), index=False)
