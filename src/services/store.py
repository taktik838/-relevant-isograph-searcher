from typing import Dict, Iterable, List
from integrations.tensorflow_serving.client import embed_text
from integrations.elasticsearch.client import add_entities as es_add_entities


async def add_entities(raw_entities: Iterable[Dict[str, str]]) -> None:
    texts: Iterable[str] = (
        entity['description']
        for entity in raw_entities
    )
    vectors: List[List[float]] = await embed_text(texts)
    entities = [
        {
            'description_vector': vector,
            **entity
        }
        for entity, vector in zip(raw_entities, vectors)
    ]
    es_add_entities(entities)
