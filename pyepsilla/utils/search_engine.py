#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import annotations

import datetime
import json
import socket
import time
from typing import Optional, Union

class VectorRetriever:
    def __init__(
        self,
        db_client,
        table_name: str,
        primary_key_field: str,
        query_index: str = None,
        query_field: str = None,
        query_vector: Union[list, dict] = None,
        response_fields: list = None,
        limit: int = 2,
        filter: str = ""
    ):
        self._db_client = db_client
        self._table_name = table_name
        self._primary_key_field = primary_key_field
        self._query_index = query_index
        self._query_field = query_field
        self._query_vector = query_vector
        self._response_fields = response_fields
        self._limit = limit
        self._filter = filter
    
    def retrieve(self, query: str) -> list[dict]:
        # Query vectors from the table
        status_code, response = self._db_client.query(
            table_name=self._table_name,
            query_text=query,
            query_index=self._query_index,
            query_field=self._query_field,
            query_vector=self._query_vector,
            response_fields=self._response_fields,
            limit=self._limit,
            filter=self._filter,
            with_distance=True,
        )
        if status_code != 200:
            error_msg = response["message"] if "message" in response else "Unknown error"
            raise Exception(f"Failed to retrieve data from table {self._table_name}: {error_msg}")
        # Add @id from the table to each record based on the primary_key_field
        for record in response["result"]:
            # Raise exception if the primary_key_field is not found in the record
            if self._primary_key_field not in record:
                raise Exception(f"Primary key field {self._primary_key_field} not found in the response from table {self._table_name}")
            record["@id"] = record[self._primary_key_field]
        return response["result"]

class Reranker:
    def rerank(self, candidates: list[list[any]], query: str = None) -> list[any]:
        pass

class RRFReRanker(Reranker):
    def __init__(self, weights: list[float] = None, k = 50, limit = None):
        self._weights = weights
        self._k = k
        self._limit = limit

    def rerank(self, candidates: list[list[any]]) -> list[any]:
        # Use candidate["@distance"] of each candidate to rerank
        # Initialize weights if not provided
        if not self._weights:
            self._weights = [1] * len(candidates)

        # Calculate RRF scores for each candidate
        rrf_scores = {}
        for i, candidate_list in enumerate(candidates):
            weight = self._weights[i]
            for rank, candidate in enumerate(candidate_list, start=1):
                # Calculate RRF score for this candidate in this list
                rrf_score = weight / (self._k + rank)
                # Aggregate scores if candidate appears in multiple lists
                if candidate["@id"] in rrf_scores:
                    rrf_scores[candidate["@id"]]["score"] += rrf_score
                else:
                    rrf_scores[candidate["@id"]] = {"candidate": candidate, "score": rrf_score}
        
        # Sort candidates based on aggregated RRF score
        sorted_candidates = sorted(rrf_scores.values(), key=lambda x: x["score"], reverse=True)

        # Apply the limit to the final list if specified
        if self._limit is not None:
            sorted_candidates = sorted_candidates[:self._limit]

        # Return only the candidate information, discarding the scores
        return [item["candidate"] for item in sorted_candidates]

class RelativeScoreFusionReranker(Reranker):
    def __init__(self, limit: int = None):
        self._limit = limit

    def normalize_distances(self, candidates: list[dict]) -> list[dict]:
        # Extract all distances
        distances = [candidate["@distance"] for candidate in candidates]

        if len(distances) < 2 or max(distances) == min(distances):
            return [{'candidate': candidate, 'score': 1} for candidate in candidates]

        min_distance, max_distance = min(distances), max(distances)

        # Normalize distances: (distance - min_distance) / (max_distance - min_distance)
        normalized_candidates = []
        for candidate in candidates:
            normalized_score = (candidate["@distance"] - min_distance) / (max_distance - min_distance)
            normalized_candidates.append({'candidate': candidate, 'score': 1 - normalized_score})

        return normalized_candidates

    def rerank(self, candidates: list[list[dict]]) -> list[dict]:
        normalized_lists = [self.normalize_distances(candidate_list) for candidate_list in candidates]

        # Aggregate normalized scores across lists
        aggregated_scores = {}
        for candidate_list in normalized_lists:
            for item in candidate_list:
                candidate_id = item['candidate']['@id']
                if candidate_id in aggregated_scores:
                    aggregated_scores[candidate_id]['score'] += item['score']
                else:
                    aggregated_scores[candidate_id] = item

        # Sort candidates based on aggregated score
        sorted_candidates = sorted(aggregated_scores.values(), key=lambda x: x['score'], reverse=True)

        # Apply the limit to the final list if specified
        if self._limit is not None:
            sorted_candidates = sorted_candidates[:self._limit]

        # Return only the candidate information, discarding the scores
        return [item['candidate'] for item in sorted_candidates]

class DistributionBasedScoreFusionReranker(Reranker):
    def __init__(self, scale_ranges: list[list[float]] = [], limit: int = None):
        self._limit = limit
        self._scale_ranges = scale_ranges

    def normalize_distances(self, scale: list[float], candidates: list[dict]) -> list[dict]:
        # Normalize distances: (distance - min_distance) / (max_distance - min_distance)
        normalized_candidates = []
        for candidate in candidates:
            normalized_score = max(candidate["@distance"] - scale[0], 0) / (scale[1] - scale[0])
            normalized_candidates.append({'candidate': candidate, 'score': 1 - min(1, normalized_score)})

        return normalized_candidates

    def rerank(self, candidates: list[list[dict]]) -> list[dict]:
        normalized_lists = [self.normalize_distances(self._scale_ranges[i], candidate_list) for i, candidate_list in enumerate(candidates)]

        # Aggregate normalized scores across lists
        aggregated_scores = {}
        for candidate_list in normalized_lists:
            for item in candidate_list:
                candidate_id = item['candidate']['@id']
                if candidate_id in aggregated_scores:
                    aggregated_scores[candidate_id]['score'] += item['score']
                else:
                    aggregated_scores[candidate_id] = item

        # Sort candidates based on aggregated score
        sorted_candidates = sorted(aggregated_scores.values(), key=lambda x: x['score'], reverse=True)

        # Apply the limit to the final list if specified
        if self._limit is not None:
            sorted_candidates = sorted_candidates[:self._limit]

        # Return only the candidate information, discarding the scores
        return [item['candidate'] for item in sorted_candidates]

class SearchEngine:
    def __init__(
        self,
        db_client,
    ):
        self._db_client = db_client
        self._retrievers = []
        self._reranker: Reranker = None

    def add_retriever(
        self,
        table_name: str,
        primary_key_field: str = "ID",
        query_index: str = None,
        query_field: str = None,
        query_vector: Union[list, dict] = None,
        response_fields: list = None,
        limit: int = 2,
        filter: str = ""
    ) -> SearchEngine:
        self._reranker = None
        self._retrievers.append(
            VectorRetriever(
                db_client=self._db_client,
                table_name=table_name,
                primary_key_field=primary_key_field,
                query_index=query_index,
                query_field=query_field,
                query_vector=query_vector,
                response_fields=response_fields,
                limit=limit,
                filter=filter
            )
        )
        return self

    def set_reranker(self, type: str="rrf", weights: list[float] = None, scale_ranges: list[list[int]] = [], k = 50, limit = None):
        if type == "rrf" or type == "reciprocal_rank_fusion":
            if weights is not None and len(self._retrievers) != len(weights):
                raise Exception("The length of weights should be equal to the number of retrievers")
            self._reranker = RRFReRanker(weights=weights, k=k, limit=limit)
        elif type == "rsf" or type == "relative_score_fusion":
            self._reranker = RelativeScoreFusionReranker(limit=limit)
        elif type == "dbsf" or type == "distribution_based_score_fusion":
            if len(scale_ranges) != len(self._retrievers):
                raise Exception("The length of scale_ranges should be equal to the number of retrievers")
            self._reranker = DistributionBasedScoreFusionReranker(scale_ranges, limit=limit)
        else:
            raise Exception("Invalid reranker type: " + type)
        return self

    def search(self, query: str) -> list[dict]:
        # If no retriever is added, return error
        if not self._retrievers:
            raise Exception("No retriever added to the search engine")
        # If more than one retrievers are added, must set a reranker
        if len(self._retrievers) > 1 and not self._reranker:
            raise Exception("More than one retriever added to the search engine, but no reranker is set")

        # Use ThreadPoolExecutor to run retrievers concurrently
        candidates = []
        for retriever in self._retrievers:
            candidates.append(retriever.retrieve(query))

        # Rerank candidates if reranker is set
        if self._reranker:
            candidates = self._reranker.rerank(candidates)

        return candidates
