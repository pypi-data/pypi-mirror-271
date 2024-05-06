from typing import Optional, List, Dict, Any

from pydantic import BaseModel


# class PropertyObj(BaseModel):
#     type: str
#     description: Optional[str] = None
#     enum: List[str] | None = None


# class ParametersObj(BaseModel): FunctionParameters
#     type: str = "object"
#     properties: Dict[str, Dict[str, Any]]
#     required: List[str]


# class FunctionObj(BaseModel): FunctionDefinition
#     name: str
#     description: str
#     parameters: ParametersObj


# class FunctionSchema(BaseModel): ChatCompletionToolParam
#     type: str = "function"
#     function: FunctionObj
#
#     class ConfigDict:
#         exclude_none = True
