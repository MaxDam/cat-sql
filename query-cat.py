from cat.mad_hatter.decorators import tool, hook, plugin
from pydantic import BaseModel
from datetime import datetime, date

from langchain.llms.base import BaseLLM
from langchain.chat_models.base import BaseChatModel

from langchain.agents import create_sql_agent 
from langchain.agents.agent_toolkits import SQLDatabaseToolkit 
from langchain.sql_database import SQLDatabase 
from langchain.agents.agent_types import AgentType
from typing import Dict, Optional
from .callbacks import NewFinalTokenHandler


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


@hook
def agent_fast_reply(fast_reply, cat) -> Dict:
    
    return_direct = True
    
    # ...
    pg_uri = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{mydatabase}"
    db = SQLDatabase.from_uri(pg_uri)

    #gpt = OpenAI(streaming=True, callbacks=[FinalStreamingStdOutCallbackHandler()], temperature=0)
    #response = cat._llm.generate(prompt, callbacks=[NewFinalTokenHandler(cat)])

    sqldbtlk = SQLDatabaseToolkit(db=db, llm=_llm)

    agent_executor = create_sql_agent(
        llm=_llm,
        toolkit=sqldbtlk,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )

    user_message = cat.working_memory["user_message_json"]["text"]
    agent_executor.run(user_message)
    
    response = ""
    if return_direct:
        return { "output": response } 
    
    return fast_reply


# Call llm with agent callback for streaming
def _llm(self, prompt: str, stream: bool = False) -> str:
    callbacks = []
    if stream:
        callbacks.append(NewFinalTokenHandler(self))

    if isinstance(self._llm, BaseLLM):
        return self._llm(prompt, callbacks=callbacks)

    if isinstance(self._llm, BaseChatModel):
        return self._llm.call_as_llm(prompt, callbacks=callbacks)
