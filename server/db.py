import weaviate
import weaviate.classes.config as wc
import os
import weaviate.classes.query as wq
import json

#def insertStory(message):
headers = {
    "X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY")
}
 
client = weaviate.connect_to_local(headers=headers)

def createDB():
    
    client.collections.create(
        name="stories",
        properties=[
            wc.Property(name="story", data_type=wc.DataType.TEXT),
            wc.Property(name="userID", data_type=wc.DataType.INT),
            wc.Property(name="userName", data_type=wc.DataType.TEXT),
            wc.Property(name="serverID", data_type=wc.DataType.INT),
            wc.Property(name="serverName", data_type=wc.DataType.TEXT),
            wc.Property(name="messageID", data_type=wc.DataType.INT)
        ],
        # Define the vectorizer module
        vectorizer_config=wc.Configure.Vectorizer.text2vec_openai(),
        # Define the generative module
        generative_config=wc.Configure.Generative.openai()
    )

    client.close()

def insertStory(message, messageID, userID, userName, serverID, serverName):

    stories = client.collections.get("stories")
    insert_story = stories.data.insert(
        properties={
            "story": message,
            "userID": userID,
            "userName": userName,
            "serverID": serverID,
            "serverName": serverName,
            "messageID": messageID
        }                 
    )

    print(insert_story)
    client.close()
    return insert_story

def queryDB(storyQuery):

    stories = client.collections.get("stories")
    response = stories.query.near_text(
        query=storyQuery, limit=1, return_metadata=wq.MetadataQuery(distance=True)
    )
    print(response.objects)

    client.close()

# Remove when done
def deleteDB():

    client.collections.delete("stories")
    client.close()
