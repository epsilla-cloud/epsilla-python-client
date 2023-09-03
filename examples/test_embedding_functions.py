#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pyepsilla.vectordb.utils import embedding_functions

sentences = ['This framework generates embeddings for each input sentence',
    'Sentences are passed as a list of string.',
    'The quick brown fox jumps over the lazy dog.']

# Default embedding function
default_ef = embedding_functions.DefaultEmbeddingFunction()
embeddings = default_ef.__call__(sentences)
print(embeddings)

## Specific Sentence Transformers model
## https://www.sbert.net/docs/pretrained_models.html#sentence-embedding-models/
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
embeddings = sentence_transformer_ef.__call__(sentences)
print(embeddings)

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")
embeddings = sentence_transformer_ef.__call__(sentences)
print(embeddings)
