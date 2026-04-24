import pandas as pd
import traceback
from query_parser import rewrite_query
import visualization as viz
from utils import get_llm
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

def execute_dataframe_agent(df: pd.DataFrame, query: str, chat_history: list = None) -> dict:
    """
    Executes a user query on the pandas DataFrame using LangChain's Pandas Agent.
    """
    try:
        # 1. Clean up dates immediately if possible
        for col in df.columns:
            if 'date' in col.lower() and df[col].dtype == 'object':
                try:
                    df[col] = pd.to_datetime(df[col])
                except Exception:
                    pass
                    
        # 2. Add conversation memory context
        history_context = ""
        if chat_history and len(chat_history) > 1:
            history_context = "\nRecent Conversation History:\n"
            # Get last 4 messages excluding the current one
            for msg in chat_history[-5:-1]:
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                if isinstance(content, str):
                    history_context += f"{role.capitalize()}: {content}\n"
        
        # 3. Rewrite query for specificity
        full_query = history_context + "\nCurrent Question: " + query
        structured_query = rewrite_query(full_query, df)
        
        # Check for chart requests explicitly to route to UI immediately
        lower_sq = structured_query.lower()
        if "chart" in lower_sq or "plot" in lower_sq or "visualize" in lower_sq or "graph" in lower_sq:
            # We will handle specialized charts if requested, else we just return a text response telling them to use UI toggles
            if "missing" in lower_sq:
                fig = viz.chart_missing_values(df)
                return {"type": "plot", "content": "Here is the missing values chart:", "figure": fig}
            elif "patient count by service" in lower_sq:
                fig = viz.chart_patient_count_by_service(df)
                if fig: return {"type": "plot", "content": "Here is the patient count by service:", "figure": fig}
            elif "satisfaction by service" in lower_sq:
                fig = viz.chart_satisfaction_by_service(df)
                if fig: return {"type": "plot", "content": "Here is the satisfaction by service:", "figure": fig}
            else:
                return {
                    "type": "text", 
                    "content": "To generate custom charts, please use the 'Chart Settings' toggle in the sidebar or main view and select your X and Y columns."
                }
                
        # Handle Dataset overview
        if "dataset overview" in lower_sq or "overview of the most important metrics" in lower_sq:
             info = f"This dataset has **{len(df)} rows** and **{len(df.columns)} columns**.\n\nColumns: {', '.join(df.columns)}."
             try:
                 fig = viz.overview_chart(df)
                 return {"type": "both", "content": info, "figure": fig}
             except Exception as e:
                 return {"type": "text", "content": info + f"\n\n(Could not generate overview chart automatically.)"}

        llm = get_llm()
        
        # 4. Create the Pandas DataFrame Agent
        # We add schema info manually to the prefix, even though the agent does df.head()
        columns = list(df.columns)
        dtypes = df.dtypes.astype(str).to_dict()
        schema_info = "\n".join([f"- {col} ({dtype})" for col, dtype in dtypes.items()])
        
        prefix = f"""
        You are a world-class data analyst Python agent. Your job is to answer user queries by writing and executing Python code on a pandas dataframe `df`.
        
        IMPORTANT RULES for ACCURACY:
        1. NO HALLUCINATIONS: ONLY use columns that exist in the dataframe. Here is the schema:
        {schema_info}
        
        2. MISSING VALUES: Account for missing/NaN values in your calculations (use `.dropna()` or `na_rm=True` equivalents if needed).
        3. EXACT NUMBERS: Return precise numerical answers. 
        4. TWO-STEP VALIDATION: Before giving your final answer, double check your code logic ensures the answer targets what was asked.
        5. DO NOT ATTEMPT TO GENERATE PLOTS OR IMAGES. Provide text/tabular data only.
        
        Answer exactly what is asked. Keep your final response clean and professional. Do NOT return code in your final Answer unless asked.
        """
        
        agent = create_pandas_dataframe_agent(
            llm, 
            df, 
            verbose=True, 
            allow_dangerous_code=True,
            prefix=prefix,
            max_iterations=5
        )
        
        # 5. Execute Agent
        print(f"Executing Agent with structured query: {structured_query}")
        result = agent.invoke(structured_query)
        output = result.get("output", "")
        
        return {"type": "text", "content": output}
        
    except Exception as e:
        print(traceback.format_exc())
        return {"error": f"Agent encountered an error while processing: {str(e)}"}

def query_data(df: pd.DataFrame, user_query: str, chat_history: list = None):
    """
    Wrapper for backward compatibility with app.py.
    """
    return execute_dataframe_agent(df, user_query, chat_history)

