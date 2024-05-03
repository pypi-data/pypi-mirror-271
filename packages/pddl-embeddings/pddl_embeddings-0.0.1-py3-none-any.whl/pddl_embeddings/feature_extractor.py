from typing import List, Dict

import torch
import numpy as np
from transformers import AutoModel, AutoTokenizer


class FeatureExtractor:
    _device = None
    _model = None
    _tokenizer = None

    def __init__(self, model_id: str, device: str = 'cpu'):
        self._device = device
        self._tokenizer = AutoTokenizer.from_pretrained(model_id)
        self._model = AutoModel.from_pretrained(model_id).to(device)

    def _pooling(self, model_outputs: torch.Tensor, tokenized_inputs: Dict, strategy: str = "cls") -> np.ndarray:
        if strategy == "cls":
            embeddings = model_outputs[:, 0]
        elif strategy == "mean":
            embeddings = torch.sum(
                model_outputs * tokenized_inputs["attention_mask"][:, :, None], dim=1) / torch.sum(tokenized_inputs["attention_mask"])
        else:
            raise NotImplementedError
        return embeddings.detach().cpu().numpy()

    def embed(self, inputs: List[str]) -> np.ndarray:
        tokenized_inputs = self._tokenizer(inputs, padding=True, return_tensors="pt")
        tokenized_inputs = {k: v.to(self._device) for k, v in tokenized_inputs.items()}
        model_outputs = self._model(**tokenized_inputs).last_hidden_state
        embeddings = self._pooling(model_outputs, tokenized_inputs)
        return embeddings
