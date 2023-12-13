from cat.mad_hatter.decorators import tool, hook, plugin
from pydantic import BaseModel, Field, ValidationError, field_validator


from langchain.agents import create_sql_agent 
from langchain.agents.agent_toolkits import SQLDatabaseToolkit 
from langchain.sql_database import SQLDatabase 
from langchain.agents.agent_types import AgentType
from typing import Dict, Optional


class MySettings(BaseModel):
    conn_str: str = Field(
        title="connection string",
        #default="postgresql://postgres:postgres@host.docker.internal:5432/postgres"
        default="mysql+mysqlconnector://root:root@host.docker.internal:3306/mydb"
    )
@plugin
def settings_schema():   
    return MySettings.schema()

@plugin
def settings_schema():   
    return MySettings.schema()



@hook
def agent_fast_reply(fast_reply, cat) -> Dict:
    
    return_direct = True
    
    # Get user message
    user_message = cat.working_memory["user_message_json"]["text"]
    
    # Obtain thought from a reasoning agent
    thought = reasoning_sql_agent(cat)

    # Get prompt
    prefix = cat.mad_hatter.execute_hook("agent_prompt_prefix", '', cat=cat)

    # Get user message and chat history
    chat_history = cat.agent_manager.agent_prompt_chat_history(
        cat.working_memory["history"]
    )
    
    # Prompt
    prompt = f"""{prefix}
    You have elaborated the user's question, 
    you have searched for the answer and now you 
    have the solution in your Thought; 
    reply to the user briefly, 
    precisely and based on the context 
    of the dialogue.
    - Human: {user_message}
    - Thought: {thought}
    - AI:"""

    # Obtain final and contestual response
    response = cat.llm(prompt)
    
    # Manage response
    if return_direct:
        return { "output": response }
    
    return fast_reply


# Execute agent to get a final thought after sql query based reasoning
def reasoning_sql_agent(cat):

    # Get user message
    user_message = cat.working_memory["user_message_json"]["text"]

    # Acquire settings
    settings = cat.mad_hatter.get_plugin().load_settings()
    
    # Init database connection
    db = SQLDatabase.from_uri(settings["conn_str"])

    # Create SQL DB Toolkit
    sqldbtlk = SQLDatabaseToolkit(db=db, llm=cat._llm)

    # Create SQL Agent
    agent_executor = create_sql_agent(
        llm=cat._llm,
        toolkit=sqldbtlk,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )

    # Obtain final thought, after agent reasoning steps
    final_thought = agent_executor.run(user_message)
    return final_thought
