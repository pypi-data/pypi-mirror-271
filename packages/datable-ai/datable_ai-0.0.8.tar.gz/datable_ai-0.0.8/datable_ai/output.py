import os

import tiktoken
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import CharacterTextSplitter

from datable_ai.core.llm import LLM_TYPE, create_llm


class Output:
    """
    A class for generating output using a language model.

    Args:
        llm_type (LLM_TYPE): The type of language model to use.
        prompt_template (str): The prompt template to use for generating output.
    """

    def __init__(
        self,
        llm_type: LLM_TYPE,
        prompt_template: str,
    ) -> None:
        self.llm_type = llm_type
        self.prompt_template = prompt_template
        self.prompt = ChatPromptTemplate.from_template(self.prompt_template)
        self.llm = create_llm(self.llm_type)
        self.encoding_name = self._encoding_name()
        self.max_tokens = self._max_tokens(self.encoding_name)

    def invoke(self, **kwargs):
        """
        Generates output using the language model.

        Args:
            **kwargs: Keyword arguments to pass to the prompt template.

        Returns:
            The generated output.

        Raises:
            RuntimeError: If an error occurs while generating output.
        """
        try:
            summarized_kwargs = {}
            for key, value in kwargs.items():
                num_tokens = self._num_tokens_from_string(value)
                if num_tokens > self.max_tokens:
                    summarized_value = self._summarize(value)
                    summarized_kwargs[key] = summarized_value["output_text"]
                else:
                    summarized_kwargs[key] = value

            chain = self.prompt | self.llm | StrOutputParser()
            return chain.invoke(summarized_kwargs)
        except Exception as e:
            raise RuntimeError(f"Error invoking Output: {str(e)}") from e

    def _num_tokens_from_string(self, text: str) -> int:
        """
        Calculates the number of tokens in a string.

        Args:
            text (str): The string to calculate the number of tokens for.

        Returns:
            The number of tokens in the string.

        Raises:
            RuntimeError: If an error occurs while calculating the number of tokens.
        """
        try:
            if (
                self.llm_type == LLM_TYPE.OPENAI
                or self.llm_type == LLM_TYPE.AZURE_OPENAI
            ):
                encoding = tiktoken.encoding_for_model(self.encoding_name)
            elif self.llm_type == LLM_TYPE.ANTHROPIC:
                encoding = tiktoken.get_encoding("cl100k_base")
            else:
                encoding = tiktoken.get_encoding("gpt2")
            num_tokens = len(encoding.encode(text))
            return num_tokens
        except Exception as e:
            raise RuntimeError(f"Error calculating number of tokens: {str(e)}") from e

    def _summarize(self, long_text: str):
        """
        Summarizes a long text into a shorter text.

        Args:
            long_text (str): The long text to summarize.

        Returns:
            A dictionary containing the summarized text.

        Raises:
            RuntimeError: If an error occurs while summarizing the text.
        """
        try:
            text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=1000, chunk_overlap=50
            )
            split_docs = text_splitter.split_text(long_text)
            docs = [Document(page_content=chunk) for chunk in split_docs]
            return load_summarize_chain(
                self.llm, chain_type="map_reduce", verbose=False
            ).invoke(docs)
        except Exception as e:
            raise RuntimeError(f"Error summarizing text: {str(e)}") from e

    def _encoding_name(self):
        """
        Returns the encoding name for the language model.

        Returns:
            The encoding name for the language model.

        Raises:
            ValueError: If the language model type is unsupported.
        """
        if self.llm_type == LLM_TYPE.OPENAI:
            return os.environ.get("OPENAI_API_MODEL")
        elif self.llm_type == LLM_TYPE.AZURE_OPENAI:
            return os.environ.get("AZURE_OPENAI_API_MODEL")
        elif self.llm_type == LLM_TYPE.ANTHROPIC:
            return os.environ.get("ANTHROPIC_API_MODEL")
        else:
            raise ValueError(f"Unsupported LLM type: {self.llm_type}")

    def _max_tokens(self, model_name: str):
        """
        Returns the maximum number of tokens for the specified model.

        Args:
            model_name (str): The name of the model.

        Returns:
            The maximum number of tokens for the specified model.
        """
        model_configs = {
            "openai": {
                "gpt-4": {"max_tokens": 8000},
                "gpt-4-32k": {"max_tokens": 32000},
                "gpt-4-turbo": {"max_tokens": 128000},
                "gpt-4-turbo-2024-04-09": {},
                "gpt-4-turbo-preview": {},
                "gpt-4-0125-preview": {},
                "gpt-3.5-turbo": {},
            },
            "anthropic": {
                "claude-3-opus-20240229": {"max_tokens": 200000},
                "claude-3-sonnet-20240229": {"max_tokens": 200000},
                "claude-3-haiku-20240307": {"max_tokens": 200000},
            },
        }

        for _provider, models in model_configs.items():
            if model_name in models:
                return models[model_name].get("max_tokens", 8000)

        return 8000
