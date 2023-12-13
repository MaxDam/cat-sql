from cat.mad_hatter.decorators import tool, hook, plugin
from typing import Dict
from .query_agent import reasoning_sql_agent
from cat.log import log

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



