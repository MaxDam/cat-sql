from cat.mad_hatter.decorators import tool, hook, plugin
from typing import Dict
from .query_agent import QueryCatAgent #, reasoning_agent
from cat.log import log

@hook
def agent_fast_reply(fast_reply, cat) -> Dict:
    
    return_direct = True
    
    # Instantiate query agent
    query_agent = QueryCatAgent(cat)

    # If is in training mode acquire data
    if query_agent.training_mode:
        response = query_agent.add_training_data()
        return { "output": response }

    # Obtain thought from a reasoning agent
    thought = query_agent.get_reasoning_agent()
    
    # Obtain final and contestual response
    response = query_agent.get_final_output(thought)
    
    # Manage response
    if return_direct:
        return { "output": response }
    
    return fast_reply

# training start intent
@tool(return_direct=True)
def start_training_intent(input, cat):
    """strart training mode"""
    cat.working_memory[QueryCatAgent.TRAINING_KEY] = True
    return "Start training mode"

# training stop intent
@tool(return_direct=True)
def stop_training_intent(input, cat):
    """stop training mode"""
    cat.working_memory[QueryCatAgent.TRAINING_KEY] = True
    return "Stop training mode"
