from typing import Any, Awaitable, Callable, Dict, Optional, Sequence

from llama_index.core.bridge.langchain import BaseLanguageModel, BaseChatModel
from llama_index.llms.openai import OpenAI

#from llama_index.llms.llm import LLM

from llama_index.core.base.llms.types import (
    ChatMessage,
    ChatResponse,
    ChatResponseAsyncGen,
    ChatResponseGen,
    CompletionResponse,
    CompletionResponseAsyncGen,
    CompletionResponseGen,
    LLMMetadata,
)

from llama_index.llms.openai.utils import (
    from_openai_message,
    is_chat_model,
    is_function_calling_model,
    openai_modelname_to_contextsize,
    resolve_openai_credentials,
    to_openai_message_dicts,
)

from openai_utils import kron_openai_modelname_to_contextsize

class KronOpenAI(OpenAI):

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=kron_openai_modelname_to_contextsize(self.model),
            num_output=self.max_tokens or -1,
            is_chat_model=is_chat_model(model=self._get_model_name()),
            is_function_calling_model=is_function_calling_model(
                model=self._get_model_name()
            ),
            model_name=self.model,
        )
    
    def _complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        #print("KronOpenAI complete called")
        response = super()._complete(prompt, **kwargs)
        text = response.text
        text = text.strip()   #triples might not start at the begining of the line
        #useful triplets are before <|endoftext|>
        text = text.split("<|endoftext|>")[0]
        #remove whitespace and all characters before first ( on all lines
        texts = text.split('\n')
        #texts = [line.strip() for line in texts]
        texts = [line[line.find('('):].strip() for line in texts]
        text = '\n'.join(texts)
        print(text)
        response.text = text
        return response
