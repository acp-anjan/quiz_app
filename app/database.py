from bson import ObjectId
from pymongo import MongoClient
from app.config import get_environment_settings

# Get configuration
settings = get_environment_settings()


client = MongoClient(settings.MONGODB_STRING)
db = client["quiz_app"]
quiz_collection = db["quizzes"]


def fetch_topics():
    topics = []
    try:
        for topic in quiz_collection.find():
            topics.append({
                "_id": str(topic["_id"]),
                "topic": topic["topic"],
                "topic_detail": topic["topic_detail"]
            })
    except Exception as e:
        print(f"Error fetching topics: {e}")
        return {"error": "Failed to fetch topics"}
    return topics

async def fetch_quizzes_by_topic(topic_id):
    quizzes = []
    try:
        # Find the topic by ID
        topic = quiz_collection.find_one({"_id": ObjectId(topic_id)})
        if not topic:
            return {"error": f"Topic with ID {topic_id} not found"}

        # Extract quizzes from the topic
        for quiz in topic.get("quiz_list", []):
            quizzes.append({
                "quiz_title": quiz["quiz_title"],
                "difficulty": quiz["difficulty"],
                "time": quiz["time"],
                "category": quiz["category"],
                "_id": str(quiz["_id"])
            })
    except Exception as e:
        print(f"Error fetching quizzes: {e}")
        return {"error": "Failed to fetch quizzes"}
    return quizzes

async def fetch_questions_by_quiz_id(topic_id, quiz_id):
    topic = quiz_collection.find_one({"_id": ObjectId(topic_id)})
    if topic:
        for quiz in topic["quiz_list"]:
            if str(quiz["_id"]) == quiz_id:
                return quiz["questions"]
    return []   


def get_quizzes_metadata():
    quizzes = []
    for quiz in quiz_collection.find():
        quiz["_id"] = str(quiz["_id"])
        quizzes.append({
            "_id": quiz["_id"],
            "title": quiz["title"],
            "category": quiz["category"],
            "difficulty": quiz["difficulty"]
        })
    return quizzes

def get_quiz_questions(quiz_id):
    for quiz in quiz_collection.find({"_id": ObjectId(quiz_id)}):
        return quiz["questions"]
    return []