from db import insertStory

stories = [
    {"message": "Spent the day relaxing across Berlin. Unforgettable experience!", "messageId": "1", "userId": "7", "userName": "Casey Rodriguez"},
    {"message": "Just returned from Seoul where we spent our days dancing. Fantastic memories!", "messageId": "2", "userId": "8", "userName": "Jamie Martinez"},
    {"message": "Can't believe we spent the last week relaxing in Golden Gate Bridge. Best trip ever!", "messageId": "3", "userId": "9", "userName": "Chris Hernandez"},
    {"message": "Spent the day hanging out across Berlin. Unforgettable experience!", "messageId": "4", "userId": "3", "userName": "Taylor Hernandez"},
    {"message": "Spent the day dancing across Thailand. Unforgettable experience!", "messageId": "5", "userId": "4", "userName": "Casey Davis"},
    {"message": "A group of us went biking in Seoul. It was absolutely amazing!", "messageId": "6", "userId": "23", "userName": "Sam Jones"},
    {"message": "Spent the day swimming across Sydney. Unforgettable experience!", "messageId": "7", "userId": "2", "userName": "Casey Johnson"},
    {"message": "Just got back from a crazy night in Dubai where we were partying until dawn!", "messageId": "8", "userId": "1", "userName": "Chris Davis"}
]

for story in stories:
    insertStory(story['message'], int(story['messageId']), int(story['userId']), story['userName'], 12, "test-server-name", [])