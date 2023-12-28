from cat.mad_hatter.decorators import tool, hook, plugin
from typing import Dict
from .query_agent import QueryCatAgent #, reasoning_agent
from cat.log import log

@hook
def agent_fast_reply(fast_reply, cat) -> Dict:
    
    return_direct = True
    
    # Instantiate query agent
    query_agent = QueryCatAgent(cat)

    # Obtain thought from a reasoning agent
    thought = query_agent.get_reasoning_agent()
    
    # Obtain final and contestual response
    response = query_agent.get_final_output(thought)
    
    # Manage response
    if return_direct:
        return { "output": response }
    
    return fast_reply
