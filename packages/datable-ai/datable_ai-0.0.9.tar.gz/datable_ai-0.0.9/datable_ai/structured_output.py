from typing import Any, Dict, List, Optional, Type

from langchain_core.pydantic_v1 import BaseModel, Field, create_model

from datable_ai.core.llm import LLM_TYPE, create_llm


class StructuredOutput:
    """
    A class for generating structured output using a language model.

    Args:
        llm_type (LLM_TYPE): The type of language model to use.
        prompt_template (str): The prompt template to use for generating output.
        output_fields (List[Dict[str, Any]]): A list of dictionaries representing the fields of the structured output.
    """

    def __init__(
        self,
        llm_type: LLM_TYPE,
        prompt_template: str,
        output_fields: List[Dict[str, Any]],
    ) -> None:
        self.llm_type = llm_type
        self.prompt_template = prompt_template
        self.output_fields = output_fields
        self.llm = create_llm(self.llm_type)
        self.output_model = self._create_dynamic_model()

    def invoke(self, **kwargs) -> str:
        """
        Generates structured output using the language model.

        Args:
            **kwargs: Keyword arguments to pass to the prompt template.

        Returns:
            The generated structured output as a JSON string.
        """
        prompt = self.prompt_template.format(**kwargs)
        return (
            self.llm.with_structured_output(self.output_model)
            .invoke(prompt)
            .json(ensure_ascii=False)
        )

    def _create_dynamic_model(self) -> Type[BaseModel]:
        """
        Creates a dynamic Pydantic model based on the output fields.

        Returns:
            A Pydantic model representing the structured output.
        """
        field_definitions = {}

        for field in self.output_fields:
            field_name = field["name"]
            field_type = field["type"]
            field_description = field.get("description", "")

            field_definitions[field_name] = (
                field_type,
                Field(description=field_description),
            )

        return create_model(
            "Output",
            **field_definitions,
            __base__=BaseModel,
            __module__=__name__,
            __doc__="A model representing the output of the LLM",
        )

    # For the Optional import in this file, there is a possibility of using it inside the `create_model` function.
    # Therefore, a dummy function is created to utilize the Optional import within this file.
    def _dummy(self, _: Optional[str]) -> str:
        pass
