import weaviate
import weaviate.classes.config as wc
import os
import weaviate.classes.query as wq

#def insertStory(message):
headers = {
        "X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY")
    }  # Replace with your OpenAI API key
 
def createDB():
    
    client = weaviate.connect_to_local(headers=headers)

    client.collections.create(
        name="stories",
        properties=[
            wc.Property(name="story", data_type=wc.DataType.TEXT),
        ],
        # Define the vectorizer module
        vectorizer_config=wc.Configure.Vectorizer.text2vec_openai(),
        # Define the generative module
        generative_config=wc.Configure.Generative.openai()
    )

    client.close()

def insertStory(message):
    client = weaviate.connect_to_local(headers=headers)

    stories = client.collections.get("stories")
    stories.data.insert(properties={"story": message})
    client.close()

def queryDB(storyQuery):
    client = weaviate.connect_to_local(headers=headers)
    stories = client.collections.get("stories")
    response = stories.query.near_text(
        query=storyQuery, limit=1, return_metadata=wq.MetadataQuery(distance=True)
    )
    print(response.objects)

    client.close()