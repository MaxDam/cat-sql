from cat.mad_hatter.decorators import tool, hook, plugin
from pydantic import BaseModel
from datetime import datetime, date

from langchain.agents import create_sql_agent 
from langchain.agents.agent_toolkits import SQLDatabaseToolkit 
from langchain.sql_database import SQLDatabase 
from langchain.agents.agent_types import AgentType
from langchain.callbacks.streaming_stdout_final_only import FinalStreamingStdOutCallbackHandler



class MySettings(BaseModel):
    required_int: int
    optional_int: int = 69
    required_str: str
    optional_str: str = "meow"
    required_date: date
    optional_date: date = 1679616000

@plugin
def settings_schema():   
    return MySettings.schema()

@tool
def get_the_day(tool_input, cat):
    """Get the day of the week. Input is always None."""

    dt = datetime.now()

    return dt.strftime('%A')

@hook
def before_cat_sends_message(message, cat):

    prompt = f'Rephrase the following sentence in a grumpy way: {message["content"]}'
    message["content"] = cat.llm(prompt)

    return message


@hook
def agent_fast_reply(fast_reply, cat) -> Dict:
    
    return_direct = True
    
    # ...
    pg_uri = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{mydatabase}"
    db = SQLDatabase.from_uri(pg_uri)

    #gpt = OpenAI(streaming=True, callbacks=[FinalStreamingStdOutCallbackHandler()], temperature=0)

    sql_db_tlk = SQLDatabaseToolkit(db=db, llm=cat._llm)

    agent_executor = create_sql_agent(
        llm=cat._llm,
        toolkit=sql_db_tlk,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )

    question = "Average rent in Chicago from Oct 2022 till Dec 2022"
    agent_executor.run(question)
    
    if return_direct:
        return { "output": response } 
    
    return fast_reply
