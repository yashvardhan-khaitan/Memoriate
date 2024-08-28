import weaviate
import os
from weaviate.classes.config import Configure

headers = {
    "X-HuggingFace-Api-Key": os.getenv("HUGGINGFACE_APIKEY"),
}

client = weaviate.connect_to_local(headers=headers)

client.collections.create(
    "DemoCollection",
    vectorizer_config=[
        Configure.NamedVectors.text2vec_huggingface(
            name="title_vector",
            source_properties=["title"],
            model="sentence-transformers/all-MiniLM-L6-v2",
        )
    ],
    # Additional parameters not shown
)

client.close()