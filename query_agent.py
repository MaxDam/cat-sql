from langchain.agents import create_sql_agent 
from langchain.agents.agent_toolkits import SQLDatabaseToolkit 
from langchain.sql_database import SQLDatabase 
from langchain.agents.agent_types import AgentType
from .settings import connections
from cat.log import log


# Execute agent to get a final thought after sql query based reasoning
def reasoning_sql_agent(cat):

    # Get user message
    user_message = cat.working_memory["user_message_json"]["text"]

    # Init database connection
    db = get_sql_database(cat)

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


# Return database connection
def get_sql_database(cat):
    # Acquire settings
    settings = cat.mad_hatter.get_plugin().load_settings()
    
    # Create connection string
    database_type = settings["database_type"]
    connection_string = connections[database_type].format(**settings)
    log.warning(f"Connection string: {connection_string}")

    # Create and return sql connection
    db = SQLDatabase.from_uri(connection_string)
    return db