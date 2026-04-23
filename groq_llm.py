import os
from groq import Groq
from dotenv import load_dotenv
from mcp_client import call_tool_sync

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# 🧠 INTENT DETECTION
def detect_intent(text):
    text = text.lower().strip()

    greetings = ["hi", "hello", "hey", "good morning", "good evening"]
    intro = ["i am", "my name is", "this is"]

    if text in greetings:
        return "greeting"

    if any(i in text for i in intro):
        return "intro"

    if len(text.split()) < 2:
        return "unknown"

    return "symptom"


# 🤖 MAIN FUNCTION
def get_response(conversation_text):

    last_user_input = conversation_text.split("user:")[-1].strip()

    intent = detect_intent(last_user_input)

    # 👋 GREETING
    if intent == "greeting":
        return (
            "Hello! 👩‍⚕️ I'm your AI Doctor.\n\n"
            "How are you feeling today?"
        )

    # 🙋 INTRODUCTION
    if intent == "intro":
        name = last_user_input.replace("i am", "").replace("my name is", "").strip().title()
        return (
            f"Nice to meet you {name}! 😊\n\n"
            "How can I help you today? Are you experiencing any symptoms?"
        )

    # ❓ UNKNOWN INPUT
    if intent == "unknown":
        return (
            "Could you please describe your symptoms clearly?\n"
            "For example: fever, headache, stomach pain."
        )

    # 🚨 EMERGENCY CHECK
    emergency = call_tool_sync("check_emergency", {"symptoms": last_user_input})

    if "EMERGENCY" in emergency:
        return emergency

    # 🔍 SEARCH DISEASES
    diseases = call_tool_sync("search_diseases", {"symptoms": last_user_input})

    # 🧠 DOCTOR PROMPT
    prompt = f"""
You are a professional AI doctor.

Conversation:
{conversation_text}

Latest symptoms:
{last_user_input}

Dataset:
{diseases}

STRICT RULES:

1. First explain possible cause
2. Then give simple remedy
3. Then give precaution
4. Ask ONLY ONE follow-up question

DO NOT:
- Ask too many questions
- Repeat same question
- Act like a therapist
- Respond medically to greetings or introductions

Keep response short, clear, and helpful.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400
    )

    return response.choices[0].message.content
