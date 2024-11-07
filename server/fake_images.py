from db import insertStory
import openai
import json
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

BYTESCALE_ENDPOINT_URL = "https://api.bytescale.com/v2/accounts/kW15biq/uploads/url"
BYTESCALE_API_HEADER = "Bearer secret_kW15biq5wSjoR662EDZYbxDuuE5B"

client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

stories = [
    {"message": "Spent the day relaxing across Berlin. Unforgettable experience!", "messageId": "1", "userId": "7", "userName": "Casey Rodriguez"},
    {"message": "Just returned from Seoul where we spent our days dancing. Fantastic memories!", "messageId": "2", "userId": "8", "userName": "Jamie Martinez"},
    {"message": "Can't believe we spent the last week relaxing in Golden Gate Bridge. Best trip ever!", "messageId": "3", "userId": "9", "userName": "Chris Hernandez"},
    {"message": "Spent the day hanging out across Berlin. Unforgettable experience!", "messageId": "4", "userId": "3", "userName": "Taylor Hernandez"},
    {"message": "Spent the day dancing across Thailand. Unforgettable experience!", "messageId": "5", "userId": "4", "userName": "Casey Davis"},
    {"message": "A group of us went biking in Seoul. It was absolutely amazing!", "messageId": "6", "userId": "23", "userName": "Sam Jones"},
    {"message": "Spent the day swimming across Sydney. Unforgettable experience!", "messageId": "7", "userId": "2", "userName": "Casey Johnson"},
    {"message": "Just got back from a crazy night in Dubai where we were partying until dawn!", "messageId": "8", "userId": "1", "userName": "Chris Davis"},
    {"message": "We finally made it to the top of the Berlin Wall, and the view was breathtaking!", "messageId": "9", "userId": "10", "userName": "Emily Lee"},
    {"message": "After dancing the night away in Seoul, we stumbled upon a hidden karaoke bar that was out of this world!", "messageId": "10", "userId": "11", "userName": "Michael Brown"},
    {"message": "I'm still pinching myself after spending a week in Golden Gate Bridge, it was truly a dream come true!", "messageId": "11", "userId": "12", "userName": "Sarah Taylor"},
    {"message": "We took a detour to the Thai countryside and discovered a hidden waterfall that was pure magic!", "messageId": "12", "userId": "13", "userName": "David Kim"},
    {"message": "After biking through the streets of Seoul, we stopped at a quaint little café and had the most delicious coffee!", "messageId": "13", "userId": "14", "userName": "Jessica Martin"},
    {"message": "I'm still reeling from the stunning views of Sydney Harbour, it was like nothing I've ever seen before!", "messageId": "14", "userId": "15", "userName": "Kevin White"},
    {"message": "We stumbled upon a secret underground club in Dubai that was the wildest party I've ever been to!", "messageId": "15", "userId": "16", "userName": "Laura Lee"},
    {"message": "After a long day of exploring Berlin, we treated ourselves to a delicious currywurst and it was love at first bite!", "messageId": "16", "userId": "17", "userName": "James Davis"},
    {"message": "We took a day trip to the nearby town of Potsdam and discovered a beautiful palace that was steeped in history!", "messageId": "17", "userId": "18", "userName": "Amanda Brown"},
    {"message": "I'm still dreaming of the delicious Korean BBQ we had in Seoul, it was the perfect way to cap off our trip!", "messageId": "18", "userId": "19", "userName": "Christopher Lee"},
    {"message": "We spent a lazy day lounging on the beach in Sydney and it was the perfect way to unwind!", "messageId": "19", "userId": "20", "userName": "Elizabeth Kim"},
    {"message": "After a crazy night in Dubai, we stumbled upon a beautiful mosque that was a peaceful oasis in the midst of chaos!", "messageId": "20", "userId": "21", "userName": "Matthew White"},
    {"message": "We took a cooking class in Berlin and learned how to make traditional German dishes like schnitzel and sauerbraten!", "messageId": "21", "userId": "22", "userName": "Natalie Taylor"},
    {"message": "I'm still in awe of the stunning architecture of the Golden Gate Bridge, it's truly a marvel of engineering!", "messageId": "22", "userId": "23", "userName": "Brian Lee"},
    {"message": "We spent a day exploring the trendy neighborhoods of Berlin and discovered some amazing street art!", "messageId": "23", "userId": "24", "userName": "Rebecca Brown"},
    {"message": "After a long day of traveling, we treated ourselves to a delicious Thai massage and it was pure bliss!", "messageId": "24", "userId": "25", "userName": "Kevin Kim"},
    {"message": "We took a scenic drive along the coast of Sydney and stopped at some of the most beautiful beaches I've ever seen!", "messageId": "25", "userId": "26", "userName": "Jessica White"},
    {"message": "I'm still reeling from the stunning views of the Dubai skyline, it was like nothing I've ever seen before!", "messageId": "26", "userId": "27", "userName": "Michael Taylor"},
    {"message": "We spent a day exploring the historic neighborhoods of Berlin and discovered some amazing museums and galleries!", "messageId": "27", "userId": "28", "userName": "Amanda Lee"},
    {"message": "After a long day of traveling, we treated ourselves to a delicious German beer and it was the perfect way to cap off our trip!", "messageId": "28", "userId": "29", "userName": "Christopher Brown"},
    {"message": "We took a day trip to the nearby town of Potsdam and discovered a beautiful palace that was steeped in history!", "messageId": "29", "userId": "30", "userName": "Elizabeth Kim"},
    {"message": "I'm still dreaming of the delicious Korean BBQ we had in Seoul, it was the perfect way to cap off our trip!", "messageId": "30", "userId": "31", "userName": "Matthew White"},
    {"message": "We spent a lazy day lounging on the beach in Sydney and it was the perfect way to unwind!", "messageId": "31", "userId": "32", "userName": "Natalie Taylor"},
    {"message": "After a crazy night in Dubai, we stumbled upon a beautiful mosque that was a peaceful oasis in the midst of chaos!", "messageId": "32", "userId": "33", "userName": "Brian Lee"},
    {"message": "We took a cooking class in Berlin and learned how to make traditional German dishes like schnitzel and sauerbraten!", "messageId": "33", "userId": "34", "userName": "Rebecca Brown"},
    {"message": "I'm still in awe of the stunning architecture of the Golden Gate Bridge, it's truly a marvel of engineering!", "messageId": "34", "userId": "35", "userName": "Kevin Kim"},
    {"message": "We spent a day exploring the trendy neighborhoods of Berlin and discovered some amazing street art!", "messageId": "35", "userId": "36", "userName": "Jessica White"},
    {"message": "After a long day of traveling, we treated ourselves to a delicious Thai massage and it was pure bliss!", "messageId": "36", "userId": "37", "userName": "Michael Taylor"},
    {"message": "We took a scenic drive along the coast of Sydney and stopped at some of the most beautiful beaches I've ever seen!", "messageId": "37", "userId": "38", "userName": "Amanda Lee"},
    {"message": "I'm still reeling from the stunning views of the Dubai skyline, it was like nothing I've ever seen before!", "messageId": "38", "userId": "39", "userName": "Christopher Brown"},
    {"message": "We spent a day exploring the historic neighborhoods of Berlin and discovered some amazing museums and galleries!", "messageId": "39", "userId": "40", "userName": "Elizabeth Kim"},
    {"message": "After a long day of traveling, we treated ourselves to a delicious German beer and it was the perfect way to cap off our trip!", "messageId": "40", "userId": "41", "userName": "Matthew White"},
    {"message": "We took a day trip to the nearby town of Potsdam and discovered a beautiful palace that was steeped in history!", "messageId": "41", "userId": "42", "userName": "Natalie Taylor"},
    {"message": "I'm still dreaming of the delicious Korean BBQ we had in Seoul, it was the perfect way to cap off our trip!", "messageId": "42", "userId": "43", "userName": "Brian Lee"},
    {"message": "We spent a lazy day lounging on the beach in Sydney and it was the perfect way to unwind!", "messageId": "43", "userId": "44", "userName": "Rebecca Brown"},
    {"message": "After a crazy night in Dubai, we stumbled upon a beautiful mosque that was a peaceful oasis in the midst of chaos!", "messageId": "44", "userId": "45", "userName": "Kevin Kim"},
    {"message": "We took a cooking class in Berlin and learned how to make traditional German dishes like schnitzel and sauerbraten!", "messageId": "45", "userId": "46", "userName": "Jessica White"},
    {"message": "I'm still in awe of the stunning architecture of the Golden Gate Bridge, it's truly a marvel of engineering!", "messageId": "46", "userId": "47", "userName": "Michael Taylor"},
    {"message": "We spent a day exploring the trendy neighborhoods of Berlin and discovered some amazing street art!", "messageId": "47", "userId": "48", "userName": "Amanda Lee"},
    {"message": "After a long day of traveling, we treated ourselves to a delicious Thai massage and it was pure bliss!", "messageId": "48", "userId": "49", "userName": "Christopher Brown"},
    {"message": "We took a scenic drive along the coast of Sydney and stopped at some of the most beautiful beaches I've ever seen!", "messageId": "49", "userId": "50", "userName": "Elizabeth Kim"}
]

for story_index in range(len(stories)):
    print(story_index)
    print(stories[story_index])
    message = stories[story_index]['message']
    print(message)
    response = client.images.generate(
        model="dall-e-3",
        prompt=message,
        size="1024x1024",
        quality="standard",
        n=1
    )

    image_url = response.data[0].url
    print(image_url)

    # Upload image to Bytescale
    res = requests.post(
        BYTESCALE_ENDPOINT_URL, 
        headers={"Authorization": BYTESCALE_API_HEADER, "Content-Type":"application/json"},
        data=json.dumps({
            "url": image_url
    }))

    print(res.json())

    hosted_url = res.json().get('fileUrl')
    print(hosted_url)
    
    # add the hosted url to the story as an array
    stories[story_index]['image_url'] = [hosted_url]
    insertStory(message, int(stories[story_index]['messageId']), int(stories[story_index]['userId']), stories[story_index]['userName'], 12, "test-server-name", stories[story_index]['image_url'])

pretty_json = json.dumps(stories, indent=4)

with open("stories.json", "w") as outfile:
    outfile.write(pretty_json)
    
print(pretty_json)