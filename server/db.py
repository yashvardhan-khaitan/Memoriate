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
            wc.Property(name="messageID", data_type=wc.DataType.INT, skip_vectorization=True),
            wc.Property(name="image_urls", data_type=wc.DataType.TEXT_ARRAY, skip_vectorization=True)
        ],
        # Define the vectorizer module
        vectorizer_config=wc.Configure.Vectorizer.text2vec_openai(),
        # Define the generative module
        generative_config=wc.Configure.Generative.openai()
    )

    client.close()

def insertStory(message, messageID, userID, userName, serverID, serverName, image_urls):

    client = weaviate.connect_to_local(headers=headers)

    stories = client.collections.get("stories")
    insert_story = stories.data.insert(
        properties={
            "story": message,
            "userID": userID,
            "userName": userName,
            "serverID": serverID,
            "serverName": serverName,
            "messageID": messageID,
            "image_urls": image_urls
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
        query=storyQuery
    )

    print(response)
    # Extract user stories
    user_stories = []
    for o in response.objects:
        if len(o.properties["image_urls"]) != 0:
            user_stories.append({o.properties["story"]: o.properties["image_urls"]})
        else:
            user_stories.append(o.properties["story"])

    print(user_stories)

    # Create prompt for summarization and send to Cerebras
    prompt = f"""Summarize the following stories or image captions and attach any image urls if found: {user_stories}. Remove any irrelevant stories that may not be related to the prompt: {storyQuery}"""
    chat_completion = cerb_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama3.1-70b"
    )

    client.close()
    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content
    
# Remove when done
def deleteDB():
    client = weaviate.connect_to_local(headers=headers)
    client.collections.delete("stories")
    client.close()