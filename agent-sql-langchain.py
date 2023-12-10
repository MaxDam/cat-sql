pip install langchain 
pip install openai
pip install psycopg2

from langchain.llms.openai import OpenAI 
from langchain.agents import AgentExecutor 
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_sql_agent 
from langchain.agents.agent_toolkits import SQLDatabaseToolkit 
from langchain.sql_database import SQLDatabase 
from langchain.agents.agent_types import AgentType
from langchain.callbacks.streaming_stdout_final_only import FinalStreamingStdOutCallbackHandler


pg_uri = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{mydatabase}"
db = SQLDatabase.from_uri(pg_uri)

OPENAI_API_KEY = "your OpenAI key"

#gpt = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo')
gpt = OpenAI(streaming=True, callbacks=[FinalStreamingStdOutCallbackHandler()], temperature=0)

toolkit = SQLDatabaseToolkit(db=db, llm=gpt)

agent_executor = create_sql_agent(
    llm=gpt,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

question = "Average rent in Chicago from Oct 2022 till Dec 2022"
agent_executor.run(question)

