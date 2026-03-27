import pandas as pd
import traceback
from query_parser import parse_query
import visualization as viz

def query_data(df: pd.DataFrame, user_query: str):

    try:

        for col in df.columns:
            if 'date' in col.lower() and df[col].dtype == 'object':
                try:
                    df[col] = pd.to_datetime(df[col])
                except Exception:
                    pass


        parsed = parse_query(user_query, df.columns.tolist())
        intent = parsed.get("intent", "unknown")
        col = parsed.get("column", None)
        groupby = parsed.get("group_by_column", None)
        metric = parsed.get("metric", None)
        sorting = parsed.get("sorting", None)

        print(f"Routing parsed intent: {parsed}")


        if intent == "dataset_overview":
            info = f"This dataset has **{len(df)} rows** and **{len(df.columns)} columns**.\n\nColumns: {', '.join(df.columns)}."
            try:
                fig = viz.overview_chart(df)
                return {"type": "both", "content": info, "figure": fig}
            except Exception as e:
                return {"type": "text", "content": info + f"\n\n(Note: Could not generate overview chart automatically.)"}

        elif intent == "missing_values":
            missing = df.isnull().sum()
            missing = missing[missing > 0]
            if len(missing) == 0:
                return {"type": "text", "content": "There are no missing values in this dataset!"}
            txt = "Count of missing values per column:\n" + "\n".join([f"- **{k}**: {v}" for k, v in missing.items()])
            return {"type": "text", "content": txt}

        elif intent == "column_types":
            types = df.dtypes.to_dict()
            txt = "Data Types mapped in Pandas:\n" + "\n".join([f"- **{k}**: {v}" for k, v in types.items()])
            return {"type": "text", "content": txt}

        elif intent == "count_rows":
            return {"type": "text", "content": f"The dataset contains a total of **{len(df):,}** rows."}

        elif intent == "max_value":
            if not col or col not in df.columns:
                return {"error": "I couldn't identify the exact column to calculate the maximum for. Make sure it's spelt correctly."}
            if not pd.api.types.is_numeric_dtype(df[col]):
                return {"error": f"The column '{col}' is not a numeric value, so I cannot find its maximum."}
                
            max_val = df[col].max()
            idx = df[col].idxmax()
            

            name_context = ""
            if 'name' in df.columns.str.lower():
                name_col = [c for c in df.columns if c.lower() == 'name'][0]
                name_context = f" (Belongs to: {df.loc[idx, name_col]})"
            elif df.columns[0] != col and df[df.columns[0]].dtype == 'object':
                 name_context = f" (Belongs to: {df.loc[idx, df.columns[0]]})"
                 
            rounded = round(max_val, 2) if isinstance(max_val, float) else max_val
            return {"type": "text", "content": f"The highest `{col}` is **{rounded}**{name_context}."}

        elif intent == "min_value":
            if not col or col not in df.columns:
                return {"error": "I couldn't identify the exact column to calculate the minimum for."}
            if not pd.api.types.is_numeric_dtype(df[col]):
                return {"error": f"The column '{col}' is not numeric."}
                
            min_val = df[col].min()
            idx = df[col].idxmin()
            
            name_context = ""
            if 'name' in df.columns.str.lower():
                name_col = [c for c in df.columns if c.lower() == 'name'][0]
                name_context = f" (Belongs to: {df.loc[idx, name_col]})"
            elif df.columns[0] != col and df[df.columns[0]].dtype == 'object':
                 name_context = f" (Belongs to: {df.loc[idx, df.columns[0]]})"
                 
            rounded = round(min_val, 2) if isinstance(min_val, float) else min_val
            return {"type": "text", "content": f"The lowest `{col}` is **{rounded}**{name_context}."}

        elif intent == "average":
            if not col or col not in df.columns:
                return {"error": "I couldn't identify the exact column to calculate the average for."}
            if not pd.api.types.is_numeric_dtype(df[col]):
                return {"error": f"The column '{col}' is not numeric. I can only calculate averages for numbers."}
                
            avg_val = df[col].mean()
            return {"type": "text", "content": f"The average `{col}` is **{round(avg_val, 2)}**."}

        elif intent == "group_by":
            if not groupby or groupby not in df.columns:
                return {"error": "I could not identify what category you want to group by in the dataset."}
            if not col or col not in df.columns:
                return {"error": "I could not identify which numerical column to calculate across the groups."}
            if not pd.api.types.is_numeric_dtype(df[col]):
                return {"error": f"Cannot execute grouped calculation because '{col}' is not numeric."}
            

            do_metric = metric.lower() if metric else "mean"
            
            try:
                if do_metric == "max":
                    res = df.groupby(groupby)[col].max()
                elif do_metric == "min":
                    res = df.groupby(groupby)[col].min()
                elif do_metric == "sum":
                    res = df.groupby(groupby)[col].sum()
                elif do_metric == "count":
                    res = df.groupby(groupby)[col].count()
                else:
                    res = df.groupby(groupby)[col].mean()
                    

                if sorting == "desc":
                    res = res.sort_values(ascending=False).head(5)
                elif sorting == "asc":
                    res = res.sort_values(ascending=True).head(5)
                    
                txt = f"Here is the `{do_metric}` of `{col}` broken down by `{groupby}`:\n"
                for idx, val in res.items():
                    rounded = round(val, 2) if isinstance(val, float) else val
                    txt += f"- **{idx}**: {rounded}\n"
                return {"type": "text", "content": txt}
                
            except Exception as e:
                return {"error": f"Could not perform Group By calculation. Error: {e}"}

        elif intent == "top_rows":
            return {"type": "text", "content": "Here is a snapshot of the top 5 rows:\n" + df.head(5).to_markdown()}


        elif intent == "chart_patient_count":
             fig = viz.chart_patient_count_by_service(df)
             if fig: return {"type": "plot", "figure": fig}
             return {"error": "Could not generate chart. Ensure the dataset has a categorical 'service' column."}
             
        elif intent == "chart_service_satisfaction":
             fig = viz.chart_satisfaction_by_service(df)
             if fig: return {"type": "plot", "figure": fig}
             return {"error": "Could not generate chart. Ensure the dataset has 'service' and 'satisfaction' columns."}
             
        elif intent == "chart_missing_values":
             fig = viz.chart_missing_values(df)
             return {"type": "plot", "figure": fig}

        else:
            return {"error": "I couldn't quite understand that. Try asking to find 'averages', 'maximum values', 'missing columns', or say 'generate a dataset overview'."}
            
    except Exception as e:
        print(traceback.format_exc())
        return {"error": f"Safe Execution Router caught a crash while analyzing your request: {str(e)}"}
