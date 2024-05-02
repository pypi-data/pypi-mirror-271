import os
from enum import Enum

import openai
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import AzureChatOpenAI, ChatOpenAI


class LLM_TYPE(str, Enum):
    """
    Enum representing the supported LLM types.
    """

    OPENAI = "OPENAI"
    AZURE_OPENAI = "AZURE_OPENAI"
    ANTHROPIC = "ANTHROPIC"


def create_llm(llm_name: LLM_TYPE) -> BaseChatModel:
    """
    Create an instance of the specified LLM type.

    Args:
        llm_name (LLM_TYPE): The type of LLM to create.

    Returns:
        BaseChatModel: An instance of the specified LLM type.

    Raises:
        ValueError: If an unsupported LLM type is provided.
    """
    if llm_name == LLM_TYPE.OPENAI:
        return _create_chat_openai(
            model_name=os.getenv("OPENAI_API_MODEL"),
            temperature=0.1,
        )
    elif llm_name == LLM_TYPE.AZURE_OPENAI:
        return _create_azure_chat_openai(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            temperature=0.1,
        )
    elif llm_name == LLM_TYPE.ANTHROPIC:
        return _create_chat_anthropic(
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            model_name=os.getenv("ANTHROPIC_API_MODEL"),
            temperature=0.1,
        )
    else:
        raise ValueError(f"Unsupported LLM type: {llm_name}")


def _create_chat_openai(model_name: str, temperature: float) -> ChatOpenAI:
    """
    Create an instance of ChatOpenAI.

    Args:
        model_name (str): The name of the OpenAI model to use.
        temperature (float): The temperature value for the model.

    Returns:
        ChatOpenAI: An instance of ChatOpenAI.
    """
    openai.api_type = "openai"
    return ChatOpenAI(
        model_name=model_name,
        temperature=temperature,
        streaming=True,
        client=openai.chat.completions,
    )


def _create_azure_chat_openai(
    api_key: str,
    azure_endpoint: str,
    openai_api_version: str,
    deployment_name: str,
    temperature: float,
) -> AzureChatOpenAI:
    """
    Create an instance of AzureChatOpenAI.

    Args:
        api_key (str): The Azure OpenAI API key.
        azure_endpoint (str): The Azure OpenAI endpoint.
        openai_api_version (str): The OpenAI API version.
        deployment_name (str): The name of the Azure OpenAI deployment.
        temperature (float): The temperature value for the model.

    Returns:
        AzureChatOpenAI: An instance of AzureChatOpenAI.
    """
    openai.api_type = "azure"
    return AzureChatOpenAI(
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        openai_api_version=openai_api_version,
        deployment_name=deployment_name,
        temperature=temperature,
        streaming=True,
        client=openai.chat.completions,
    )


def _create_chat_anthropic(
    anthropic_api_key: str, model_name: str, temperature: float
) -> ChatAnthropic:
    """
    Create an instance of ChatAnthropic.

    Args:
        anthropic_api_key (str): The Anthropic API key.
        model_name (str): The name of the Anthropic model to use.
        temperature (float): The temperature value for the model.

    Returns:
        ChatAnthropic: An instance of ChatAnthropic.
    """
    return ChatAnthropic(
        anthropic_api_key=anthropic_api_key,
        model=model_name,
        temperature=temperature,
        streaming=True,
    )
