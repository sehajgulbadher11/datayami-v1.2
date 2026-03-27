import json
from utils import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def parse_query(user_query: str, columns: list) -> dict:
    user_query_lower = user_query.lower().strip()
    

    for word in ["most", "highest", "maximum", "top", "best", "largest"]:
        if word in user_query_lower:
            user_query_lower = user_query_lower.replace(word, "max")
            break
            

    if "dataset overview" in user_query_lower or "overview of the most important metrics" in user_query_lower:
        return {"intent": "dataset_overview"}
    if "missing values" in user_query_lower or "missing" in user_query_lower:
        if "chart" in user_query_lower or "plot" in user_query_lower or "visualize" in user_query_lower:
            return {"intent": "chart_missing_values"}
        return {"intent": "missing_values"}
    if "data types of the columns" in user_query_lower or ("type" in user_query_lower and "column" in user_query_lower):
        return {"intent": "column_types"}
    if "how many rows" in user_query_lower or "dataset size" in user_query_lower:
        return {"intent": "count_rows"}
        

    if "patient count by service" in user_query_lower and ("chart" in user_query_lower or "plot" in user_query_lower):
        return {"intent": "chart_patient_count"}
    if "satisfaction by service" in user_query_lower and ("chart" in user_query_lower or "plot" in user_query_lower):
        return {"intent": "chart_service_satisfaction"}
        
    system_prompt = """
    You are an intent router for a data analytics platform.
    The dataset has the following columns: {columns}
    
    Map the user's query to one of the following exact intents:
    - "max_value": finding the max, most, highest, best, top, largest of a column
    - "min_value": finding the min, lowest, smallest, worst of a column
    - "average": finding the mean, average of a column
    - "group_by": asking for a breakdown, group by, or 'by service', 'by category'. Often asks things like "Which service has the highest satisfaction score?"
    - "top_rows": asking to show data, top 5, head
    - "count_rows": asking how many rows, count of dataset
    - "chart_patient_count": asking for chart of patient count by service
    - "chart_service_satisfaction": asking for chart of satisfaction by service
    - "chart_missing_values": asking to visualize missing values
    - "dataset_overview": asking about what the dataset is about
    - "missing_values": checking if there's nulls
    - "column_types": asking types
    - "unknown": if none fit, or confusing
    
    You must extract arguments from the query if requested.
    Arguments:
    - "column": The specific column the mathematical operation (max, min, average, sum) targets. ONLY use explicitly provided columns from the list above.
    - "group_by_column": The column used to split or group the data (e.g. 'service' in 'by service')
    - "metric": If group_by, you MUST provide the metric they are calculating across groups ('mean', 'max', 'min', 'sum', 'count')
    - "sorting": If they are looking for "highest" or "lowest" among groups, return "desc" for highest, "asc" for lowest.
    
    Examples:
    "What is the average satisfaction score?" -> {{"intent": "average", "column": "satisfaction"}}
    "Which service has the highest satisfaction score?" -> {{"intent": "group_by", "group_by_column": "service", "column": "satisfaction", "metric": "mean", "sorting": "desc"}}
    "Plot patient count by service" -> {{"intent": "chart_patient_count"}}
    "give me the data with the max satisfaction rate" -> {{"intent": "max_value", "column": "satisfaction"}}

    The user's query is: "{user_query}"

    ONLY return valid JSON. Do not return markdown tags. Ensure all keys have string values or null.
    """
    
    full_prompt = ChatPromptTemplate.from_template(system_prompt)
    llm = get_llm()
    chain = full_prompt | llm | StrOutputParser()
    
    try:
        raw_response = chain.invoke({
            "columns": ", ".join(columns),
            "user_query": user_query_lower
        })
        
        start_idx = raw_response.find("{")
        end_idx = raw_response.rfind("}")
        
        if start_idx != -1 and end_idx != -1 and end_idx >= start_idx:
            raw_response = raw_response[start_idx : end_idx + 1]
            
        print(f"RAW LLM: {raw_response}")
        parsed = json.loads(raw_response)
        

        if "intent" not in parsed:
            parsed["intent"] = "unknown"
            
        return parsed
    except Exception as e:
        print(f"Query parsing error: {e}")
        return {"intent": "unknown"}
