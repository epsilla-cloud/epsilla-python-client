#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pyepsilla.vectordb.utils import embedding_functions


sentences = ["This is an example sentence", "Each sentence is converted"]

# default
default_ef = embedding_functions.DefaultEmbeddingFunction()
embeddings = sentence_transformer_ef.__call__(sentences)
print(embeddings)

## Specific Sentence Transformers model
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
embeddings = sentence_transformer_ef.__call__(sentences)
print(embeddings)