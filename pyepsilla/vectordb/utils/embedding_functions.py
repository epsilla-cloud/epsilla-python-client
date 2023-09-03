#!/usr/bin/env python
# -*- coding:utf-8 -*-

from typing import Optional, Union, Sequence, Any, Dict, List, Mapping, cast
from typing_extensions import Literal, TypedDict, Protocol

from pathlib import Path
import os, tarfile, requests, importlib
import numpy as np
import numpy.typing as npt


##
Documents = List[str]
Vector = Union[Sequence[float], Sequence[int]]
Embedding = Vector
Embeddings = List[Embedding]

class EmbeddingFunction(Protocol):
    def __call__(self, texts: Documents) -> Embeddings:
        ...


class SentenceTransformerEmbeddingFunction(EmbeddingFunction):
    # Since we do dynamic imports we have to type this as Any
    models: Dict[str, Any] = {}

    # for a full list of options:
    # https://www.sbert.net/docs/pretrained_models.html#sentence-embedding-models/
    # https://huggingface.co/sentence-transformers,
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        device: str = "cpu",
        normalize_embeddings: bool = False,
    ):
        if model_name not in self.models:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError:
                raise ValueError(
                    "The sentence_transformers python package is not installed. Please install it with `pip install sentence_transformers`"
                )
            self.models[model_name] = SentenceTransformer(model_name, device=device)
        self._model = self.models[model_name]
        self._normalize_embeddings = normalize_embeddings

    def __call__(self, texts: Documents) -> Embeddings:
        return self._model.encode(
            list(texts),
            convert_to_numpy=True,
            normalize_embeddings=self._normalize_embeddings,
        ).tolist()


class Text2VecEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model_name: str = "shibing624/text2vec-base-chinese"):
        try:
            from text2vec import SentenceModel
        except ImportError:
            raise ValueError(
                "The text2vec python package is not installed. Please install it with `pip install text2vec`"
            )
        self._model = SentenceModel(model_name_or_path=model_name)

    def __call__(self, texts: Documents) -> Embeddings:
        return self._model.encode(list(texts), convert_to_numpy=True).tolist()  # type: ignore # noqa E501


# implements the same functionality as "all-MiniLM-L6-v2" from sentence-transformers.
class ONNXMiniLM_L6_V2(EmbeddingFunction):
    MODEL_NAME = "all-MiniLM-L6-v2"
    DOWNLOAD_PATH = Path.home() / ".cache" / "onnx_models" / MODEL_NAME
    EXTRACTED_FOLDER_NAME = "onnx"
    ARCHIVE_FILENAME = "onnx.tar.gz"
    MODEL_DOWNLOAD_URL = (
        "https://config.epsilla.com/onnx.tar.gz"
    )
    tokenizer = None
    model = None


    def __init__(self) -> None:
        try:
            self.ort = importlib.import_module("onnxruntime")
        except ImportError:
            raise ValueError(
                "The onnxruntime python package is not installed. Please install it with `pip install onnxruntime`"
            )
        try:
            self.Tokenizer = importlib.import_module("tokenizers").Tokenizer
        except ImportError:
            raise ValueError(
                "The tokenizers python package is not installed. Please install it with `pip install tokenizers`"
            )
        try:
            self.tqdm = importlib.import_module("tqdm").tqdm
        except ImportError:
            raise ValueError(
                "The tqdm python package is not installed. Please install it with `pip install tqdm`"
            )

    def _download(self, url: str, fname: str, chunk_size: int = 1024) -> None:
        resp = requests.get(url, stream=True)
        total = int(resp.headers.get("content-length", 0))
        with open(fname, "wb") as file, self.tqdm(
            desc=str(fname),
            total=total,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in resp.iter_content(chunk_size=chunk_size):
                size = file.write(data)
                bar.update(size)

    def _normalize(self, v: npt.NDArray) -> npt.NDArray:
        norm = np.linalg.norm(v, axis=1)
        norm[norm == 0] = 1e-12
        return v / norm[:, np.newaxis]

    def _forward(self, documents: List[str], batch_size: int = 32) -> npt.NDArray:
        self.tokenizer = cast(self.Tokenizer, self.tokenizer)
        self.model = cast(self.ort.InferenceSession, self.model)
        all_embeddings = []
        for i in range(0, len(documents), batch_size):
            batch = documents[i : i + batch_size]
            encoded = [self.tokenizer.encode(d) for d in batch]
            input_ids = np.array([e.ids for e in encoded])
            attention_mask = np.array([e.attention_mask for e in encoded])
            onnx_input = {
                "input_ids": np.array(input_ids, dtype=np.int64),
                "attention_mask": np.array(attention_mask, dtype=np.int64),
                "token_type_ids": np.array(
                    [np.zeros(len(e), dtype=np.int64) for e in input_ids],
                    dtype=np.int64,
                ),
            }
            model_output = self.model.run(None, onnx_input)
            last_hidden_state = model_output[0]
            input_mask_expanded = np.broadcast_to(
                np.expand_dims(attention_mask, -1), last_hidden_state.shape
            )
            embeddings = np.sum(last_hidden_state * input_mask_expanded, 1) / np.clip(
                input_mask_expanded.sum(1), a_min=1e-9, a_max=None
            )
            embeddings = self._normalize(embeddings).astype(np.float32)
            all_embeddings.append(embeddings)
        return np.concatenate(all_embeddings)

    def _init_model_and_tokenizer(self) -> None:
        if self.model is None and self.tokenizer is None:
            self.tokenizer = self.Tokenizer.from_file(
                os.path.join(
                    self.DOWNLOAD_PATH, self.EXTRACTED_FOLDER_NAME, "tokenizer.json"
                )
            )
            self.tokenizer.enable_truncation(max_length=256)
            self.tokenizer.enable_padding(pad_id=0, pad_token="[PAD]", length=256)
            self.model = self.ort.InferenceSession(
                os.path.join(
                    self.DOWNLOAD_PATH, self.EXTRACTED_FOLDER_NAME, "model.onnx"
                )
            )

    def __call__(self, texts: Documents) -> Embeddings:
        self._download_model_if_not_exists()
        self._init_model_and_tokenizer()
        res = cast(Embeddings, self._forward(texts).tolist())
        return res

    def _download_model_if_not_exists(self) -> None:
        onnx_files = [
            "config.json",
            "model.onnx",
            "special_tokens_map.json",
            "tokenizer_config.json",
            "tokenizer.json",
            "vocab.txt",
        ]
        extracted_folder = os.path.join(self.DOWNLOAD_PATH, self.EXTRACTED_FOLDER_NAME)
        onnx_files_exist = True
        for f in onnx_files:
            if not os.path.exists(os.path.join(extracted_folder, f)):
                onnx_files_exist = False
                break
        if not onnx_files_exist:
            os.makedirs(self.DOWNLOAD_PATH, exist_ok=True)
            if not os.path.exists(
                os.path.join(self.DOWNLOAD_PATH, self.ARCHIVE_FILENAME)
            ):
                self._download(
                    url=self.MODEL_DOWNLOAD_URL,
                    fname=os.path.join(self.DOWNLOAD_PATH, self.ARCHIVE_FILENAME),
                )
            with tarfile.open(
                name=os.path.join(self.DOWNLOAD_PATH, self.ARCHIVE_FILENAME),
                mode="r:gz",
            ) as tar:
                tar.extractall(path=self.DOWNLOAD_PATH)


def DefaultEmbeddingFunction() -> Optional[EmbeddingFunction]:
    return ONNXMiniLM_L6_V2()

