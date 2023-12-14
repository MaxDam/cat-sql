from langchain.agents import create_sql_agent, create_json_agent
#from langchain.agents import create_csv_agent
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit 
from langchain.sql_database import SQLDatabase 
from langchain.agents.agent_types import AgentType
from .settings import datasources
from cat.log import log


# Execute agent to get a final thought, based on the type 
def reasoning_agent(cat):

    # Acquire settings
    settings = cat.mad_hatter.get_plugin().load_settings()
    
    # Get user message
    user_message = cat.working_memory["user_message_json"]["text"]

    # Get agent type
    datasource_type = settings["ds_type"]
    agent_type = datasources[datasource_type]["agent_type"]

    # Execute agent based on the type
    if agent_type == "sql":
        return _reasoning_sql_agent(cat, user_message, settings)
    if agent_type == "csv":
        return _reasoning_csv_agent(cat, user_message, settings)
    if agent_type == "json":
        return _reasoning_json_agent(cat, user_message, settings)
    
    return ""


# Execute sql agent
def _reasoning_sql_agent(cat, user_message, settings):

    # Create connection string
    datasource_type = settings["ds_type"]
    connection_string = datasources[datasource_type]["conn_str"].format(**settings)
    log.warning(f"Connection string: {connection_string}")

    # Create sql connection
    try:
        db = SQLDatabase.from_uri(connection_string)

        # Create SQL DB Toolkit
        sqldbtlk = SQLDatabaseToolkit(db=db, llm=cat._llm)

        # Create SQL Agent
        agent_executor = create_sql_agent(
            llm=cat._llm,
            toolkit=sqldbtlk,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )
    except Exception as e:
        log.error(f"Failed to create SQL connection: {e}")
        return f"it was not possible to connect to the selected data source: {e}"

    # Obtain final thought, after agent reasoning steps
    final_thought = agent_executor.run(user_message)
    return final_thought


# Execute csv agent
def _reasoning_csv_agent(cat, user_message, settings):

    # Get csv file path
    csv_file_path = settings["host"]
    delimiter = settings["extra"] if settings["extra"].strip() else ";"

    # Create CSV
    try:
        #agent_executor = create_csv_agent(cat._llm, csv_file_path, verbose=True)
        agent_executor = create_csv_agent(cat._llmllm, csv_file_path, pandas_kwargs={'delimiter': delimiter}, verbose=True)
    except Exception as e:
        log.error(f"Failed to create SQL connection: {e}")
        return f"it was not possible to connect to the selected data source: {e}"

    # Obtain final thought, after agent reasoning steps
    final_thought = agent_executor.run(user_message)
    return final_thought


# Execute json agent
def _reasoning_json_agent(cat, user_message, settings):

    # Get csv file path
    json_file_path = settings["host"]

    # Create CSV
    try:
        agent_executor = create_json_agent(cat._llm, json_file_path, verbose=True)
    except Exception as e:
        log.error(f"Failed to create SQL connection: {e}")
        return f"it was not possible to connect to the selected data source: {e}"

    # Obtain final thought, after agent reasoning steps
    final_thought = agent_executor.run(user_message)
    return final_thought
