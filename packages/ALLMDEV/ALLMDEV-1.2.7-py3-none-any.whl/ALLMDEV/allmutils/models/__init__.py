from typing import Type

from allmutils.domain.enumerables import AvailableModels
from allmutils.models.abstract import AbstractModel
from allmutils.models.azure_llama2 import AzureLlama2Model
from allmutils.models.azure_mistral import AzureMistralModel
from allmutils.models.azure_openai import AzureOpenAIModel
from allmutils.models.vertexai_gemini import VertexAIGeminiModel
from allmutils.models.vertexai_palm import VertexAIPalmModel
from allmutils.models.vertexai_gemma import VertexAIGemmaModel

__all__ = [
    "AzureOpenAIModel",
    "AzureLlama2Model",
    "AzureMistralModel",
    "VertexAIPalmModel",
    "VertexAIGeminiModel",
    "VertexAIGemmaModel",
    "get_available_models"
]


def get_available_models() -> dict[str, Type[AbstractModel]]:
    return {
        AvailableModels.AZURE_OPENAI_MODEL: AzureOpenAIModel,
        AvailableModels.AZURE_LLAMA2_MODEL: AzureLlama2Model,
        AvailableModels.AZURE_MISTRAL_MODEL: AzureMistralModel,
        AvailableModels.VERTEXAI_PALM2_MODEL: VertexAIPalmModel,
        AvailableModels.VERTEXAI_GEMINI_MODEL: VertexAIGeminiModel,
        AvailableModels.VERTEXAI_GEMMA_MODEL: VertexAIGemmaModel,
    }

