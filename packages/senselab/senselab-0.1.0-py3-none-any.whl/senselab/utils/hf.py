"""This module provides the implementation of Hugging Face utilities."""

import os
from typing import Optional

from huggingface_hub import HfApi
from pydantic import BaseModel, field_validator


class HFModel(BaseModel):
    """Hugging Face model."""
    model_id: str
    revision: str = "main"

    @field_validator('model_id')
    def validate_model_id(cls, value: str) -> str:
        """Validate the model_id."""
        if not value:
            raise ValueError("model_id cannot be empty")
        if not os.path.isfile(value) and not _check_hf_repo_exists(value, "model", None):
            raise ValueError("model_id is not a valid Hugging Face model")
        return value    

def _check_hf_repo_exists(repo_id: str, repo_type: str, token: Optional[str] = None) -> bool:
    """Private function to check if a Hugging Face repository exists."""
    api = HfApi()
    try:
        repo_refs = api.list_repo_refs(repo_id=repo_id, repo_type=repo_type, token=token)
        if repo_refs.branches:
            return True
    except Exception as e:
        raise RuntimeError(f"An error occurred: {e}")
    return False