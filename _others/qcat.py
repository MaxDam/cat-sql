from langchain.llms.base import BaseLLM
from langchain.chat_models.base import BaseChatModel
from .agent_callbacks import NewFinalTokenHandler

class QCat:

    def __init__(self, cat):
        self.cat = cat
        self._llm = cat._llm

    def llm(self, prompt: str, stream: bool = False) -> str:
        callbacks = []
        if stream:
            callbacks.append(NewFinalTokenHandler(self.cat))

        if isinstance(self.cat._llm, BaseLLM):
            return self.cat._llm(prompt, callbacks=callbacks)

        if isinstance(self.cat._llm, BaseChatModel):
            return self.cat._llm.call_as_llm(prompt, callbacks=callbacks)
