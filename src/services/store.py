from typing import Dict, Iterable, List
from integrations.tensorflow_serving.client import embed_text
from integrations.elasticsearch import client as es_api


async def add_entities(raw_entities: Iterable[Dict[str, str]]) -> None:
    texts: List[str] = [
        entity['description']
        for entity in raw_entities
    ]
    vectors: List[List[float]] = await embed_text(texts)
    entities = [
        {
            'description_vector': vector,
            **entity
        }
        for entity, vector in zip(raw_entities, vectors)
    ]
    await es_api.add_entities(entities)


async def update_entity(url: str, new_description: List[str]) -> None:
    new_vector: List[List[float]] = await embed_text(new_description)
    await es_api.update(url, new_description, new_vector[0])
