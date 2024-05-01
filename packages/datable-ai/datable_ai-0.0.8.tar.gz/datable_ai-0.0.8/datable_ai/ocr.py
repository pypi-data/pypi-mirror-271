import base64
from io import BytesIO

from langchain_core.messages import HumanMessage
from PIL import Image

from datable_ai.core.llm import LLM_TYPE, create_llm


# Currently only supports LLM_TYPE.ANTHROPIC
class OCR:
    def __init__(self, llm_type: LLM_TYPE, prompt_template: str) -> None:
        """
        Initialize the OCR class.

        Args:
            llm_type (LLM_TYPE): The type of language model to use.
            prompt_template (str): The prompt template for the OCR task.
        """
        self.llm_type = llm_type
        self.prompt_template = prompt_template
        self.llm = create_llm(self.llm_type)
        self.max_size = 4 * 1024 * 1024
        self.quality = 85

    def invoke(self, image_path: str):
        """
        Invoke the OCR process on the given image.

        Args:
            image_path (str): The path to the image file.

        Returns:
            The result of the OCR process.
        """
        with open(image_path, "rb") as image_file:
            compressed_image = self._compress_image(image_file)
        messages = [
            HumanMessage(
                content=[
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{compressed_image}",  # noqa: E501
                        },
                    },
                    {"type": "text", "text": self.prompt_template},
                ]
            )
        ]
        return self.llm.invoke(messages)

    def _compress_image(self, image_file):
        """
        Compress the image to reduce its size.

        Args:
            image_file: The image file object.

        Returns:
            The base64-encoded compressed image.
        """
        with Image.open(image_file) as img:
            img.thumbnail((1092, 1092))
            output_buffer = BytesIO()
            img.save(output_buffer, format="JPEG", optimize=True, quality=self.quality)
            compressed_image = output_buffer.getvalue()
            return self._get_base64_encoded_image(compressed_image)

    def _get_base64_encoded_image(self, image_data):
        """
        Get the base64-encoded representation of the image data.

        Args:
            image_data: The image data as bytes.

        Returns:
            The base64-encoded image string.

        Raises:
            ValueError: If the image compression ratio reaches its limit.
        """
        encoded_image = base64.b64encode(image_data).decode("utf-8")
        while len(encoded_image) > self.max_size:
            self.quality -= 5
            if self.quality < 5:
                raise ValueError("Image compression ratio has reached its limit")
            with Image.open(BytesIO(image_data)) as img:
                output_buffer = BytesIO()
                img.save(
                    output_buffer, format="JPEG", optimize=True, quality=self.quality
                )
                image_data = output_buffer.getvalue()
                encoded_image = base64.b64encode(image_data).decode("utf-8")
        return encoded_image
