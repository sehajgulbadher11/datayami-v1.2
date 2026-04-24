import json
from utils import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def rewrite_query(user_query: str, df) -> str:
    """
    Rewrites a vague user query into a structured, precise query 
    by leveraging the dataframe schema and sample data.
    """
    
    # Extract schema and sample context
    columns = list(df.columns)
    dtypes = df.dtypes.astype(str).to_dict()
    schema_info = "\n".join([f"- {col} ({dtype})" for col, dtype in dtypes.items()])
    
    try:
        sample_data = df.head(3).to_markdown()
    except Exception:
        sample_data = df.head(3).to_string()
        
    system_prompt = """
    You are an expert data analyst assistant. 
    Your job is to rewrite the user's vague query into a highly specific, logical, 
    and structured question that a Pandas DataFrame agent can easily execute.
    
    Dataset Schema (Column Name and Type):
    {schema_info}
    
    Sample Data (Top 3 Rows):
    {sample_data}
    
    RULES:
    1. If the user's query is already clear and specific, just return it as is but ensure column names match exactly.
    2. Convert vague requests like "sales?" to "What is the total sum of the 'sales' column?"
    3. If the user asks for a chart or plot, keep that intent in the query (e.g., "Create a bar chart showing patient count by service").
    4. Only reference columns that actually exist in the schema. Do NOT hallucinate columns.
    5. Ensure the rewritten query specifies whether to calculate max, min, average, sum, or count if applicable.
    6. Return ONLY the rewritten query as plain text. Do NOT wrap it in quotes or markdown.
    7. Do not include any reasoning or conversational filler.
    """
    
    full_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{user_query}")
    ])
    
    llm = get_llm()
    chain = full_prompt | llm | StrOutputParser()
    
    try:
        rewritten_query = chain.invoke({
            "schema_info": schema_info,
            "sample_data": sample_data,
            "user_query": user_query
        })
        
        print(f"Original: {user_query}")
        print(f"Rewritten: {rewritten_query}")
        return rewritten_query.strip()
    except Exception as e:
        print(f"Query rewriting error: {e}")
        return user_query
