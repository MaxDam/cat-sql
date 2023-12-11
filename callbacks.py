
from langchain.callbacks.streaming_stdout_final_only import FinalStreamingStdOutCallbackHandler


class NewFinalTokenHandler(FinalStreamingStdOutCallbackHandler):

    def __init__(self, stray):
        self.stray = stray
        
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.super().on_llm_new_token(token, **kwargs)
        self.stray.send_ws_message(token, msg_type="chat_token")
