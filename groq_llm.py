import os
from groq import Groq
from dotenv import load_dotenv
from mcp_client import call_tool_sync

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def is_greeting(text):
    greetings = ["hi", "hello", "hey", "good morning", "good evening"]
    return any(g == text.lower().strip() for g in greetings)


def get_response(conversation_text):

    last_user_input = conversation_text.split("user:")[-1].strip()

    # 👋 Greeting handling
    if is_greeting(last_user_input):
        return (
            "Hello! 👩‍⚕️ I'm your AI Doctor.\n\n"
            "How are you feeling today?\n"
            "Please tell me your symptoms so I can help you."
        )

    # 🚨 Emergency check
    emergency = call_tool_sync("check_emergency", {"symptoms": last_user_input})

    if "EMERGENCY" in emergency:
        return emergency

    # 🛑 If not enough info
    if len(last_user_input.split()) < 2:
        return (
            "Could you please describe your symptoms in more detail?\n"
            "For example: fever, stomach pain, headache, etc."
        )

    # 🔍 Search dataset
    diseases = call_tool_sync("search_diseases", {"symptoms": last_user_input})

    # 🧠 Doctor prompt
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
- Use dataset for greetings

Keep response short, clear, and helpful.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400
    )

    return response.choices[0].message.content