import plotly.express as px
import pandas as pd

def _apply_dark_theme(fig):

    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def overview_chart(df: pd.DataFrame):


    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if len(numeric_cols) > 0 and len(cat_cols) > 0:
        cat_col = cat_cols[0]
        num_col = numeric_cols[0]
        cdf = df.groupby(cat_col, as_index=False)[num_col].mean()
        fig = px.bar(cdf, x=cat_col, y=num_col, title=f"Average {num_col} by {cat_col}",
                     color_discrete_sequence=['#c026d3', '#6b21a8', '#3b82f6', '#ec4899'])
    elif len(numeric_cols) >= 2:
        fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], title=f"{numeric_cols[0]} vs {numeric_cols[1]}",
                         color_discrete_sequence=['#c026d3'])
    else:

        row_count = pd.DataFrame({"Metric": ["Total Rows"], "Value": [len(df)]})
        fig = px.bar(row_count, x="Metric", y="Value", title="Dataset Size",
                     color_discrete_sequence=['#3b82f6'])
                     
    return _apply_dark_theme(fig)

def chart_missing_values(df: pd.DataFrame):

    missing = df.isnull().sum().reset_index()
    missing.columns = ['Column', 'Missing Values']
    fig = px.bar(missing, x='Column', y='Missing Values', title="Missing Values per Column",
                 color_discrete_sequence=['#ec4899'])
    return _apply_dark_theme(fig)

def chart_patient_count_by_service(df: pd.DataFrame):

    if 'service' in df.columns.str.lower():

        col = [c for c in df.columns if c.lower() == 'service'][0]
        cdf = df[col].value_counts().reset_index()
        cdf.columns = [col, 'Count']
        fig = px.bar(cdf, x=col, y='Count', title="Patient Count by Service",
                     color_discrete_sequence=['#3b82f6', '#c026d3'])
        return _apply_dark_theme(fig)
    else:
        return None

def chart_satisfaction_by_service(df: pd.DataFrame):

    cols_lower = df.columns.str.lower()
    if 'service' in cols_lower and 'satisfaction' in cols_lower:
        serv_col = [c for c in df.columns if c.lower() == 'service'][0]
        sat_col = [c for c in df.columns if c.lower() == 'satisfaction'][0]
        cdf = df.groupby(serv_col, as_index=False)[sat_col].mean()
        fig = px.bar(cdf, x=serv_col, y=sat_col, title="Average Satisfaction by Service",
                     color_discrete_sequence=['#c026d3'])
        return _apply_dark_theme(fig)
    else:
        return None
