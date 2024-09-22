import weaviate
import weaviate.classes.config as wc
import os
import weaviate.classes.query as wq
import json
from cerebras.cloud.sdk import Cerebras

#def insertStory(message):
headers = {
    "X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY")
}
 
def createDB():
    
    client = weaviate.connect_to_local(headers=headers)

    client.collections.create(
        name="stories",
        properties=[
            wc.Property(name="story", data_type=wc.DataType.TEXT),
            wc.Property(name="userID", data_type=wc.DataType.INT, skip_vectorization=True),
            wc.Property(name="userName", data_type=wc.DataType.TEXT),
            wc.Property(name="serverID", data_type=wc.DataType.INT, skip_vectorization=True),
            wc.Property(name="serverName", data_type=wc.DataType.TEXT, skip_vectorization=True),
            wc.Property(name="messageID", data_type=wc.DataType.INT, skip_vectorization=True)
        ],
        # Define the vectorizer module
        vectorizer_config=wc.Configure.Vectorizer.text2vec_openai(),
        # Define the generative module
        generative_config=wc.Configure.Generative.openai()
    )

    client.close()

def insertStory(message, messageID, userID, userName, serverID, serverName):

    client = weaviate.connect_to_local(headers=headers)

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

def summarizeDB(storyQuery):

    # Cerebras client
    cerb_client = Cerebras(
        api_key=os.getenv("CEREBRAS_API_KEY"),
    )

    # Weaviate client
    client = weaviate.connect_to_local(headers=headers)

    # Get stories from Weaviate
    stories = client.collections.get("stories")
    response = stories.generate.near_text(
        query=storyQuery, 
        limit=3
    )

    # Extract user stories
    user_stories = []
    for o in response.objects:
        user_stories.append(o.properties["story"])

    # Create prompt for summarization and send to Cerebras
    prompt = f"""Summarize the following stories in a paragraph: {user_stories}"""
    chat_completion = cerb_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama3.1-8b"
    )

    client.close()
    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content
    
# Remove when done
def deleteDB():
    client = weaviate.connect_to_local(headers=headers)
    client.collections.delete("stories")
    client.close()

# if __name__ == "__main__": 
#     summarizeDB("How was RAG Night?")