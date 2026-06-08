import os
from dotenv import load_dotenv
from backend.rag import (
    search_documents_with_scores
)
import google.generativeai as genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


def get_chat_response(user_message):

    try:

        relevant_docs = search_documents_with_scores(
            user_message
        )

        if not relevant_docs:

            return (
                "I could not find any relevant "
                "information in the knowledge base."
            )
        best_distance = (
            relevant_docs[0]["distance"]
            )

        if best_distance < 0.5:

            confidence = "High"

        elif best_distance < 1.0:

            confidence = "Medium"

        else:

            confidence = "Low"
        context = "\n\n".join(
            doc["text"]
            for doc in relevant_docs
        )

        prompt = f"""
You are SmartAssist AI.

You are an enterprise IT support assistant.

STRICT RULES:

1. Use ONLY information from context.
2. Never invent information.
3. Never use outside knowledge.
4. If answer is not found, say:

I could not find this information in the company knowledge base.

Context:

{context}

Question:

{user_message}
"""

        response = model.generate_content(
            prompt
        )

        sources = set()

        for doc in relevant_docs:

            sources.add(
                doc["source"]
            )

        source_text = "\n".join(
            [
                f"• {source}"
                for source in sources
            ]
        ) 
        if confidence == "High":

            confidence_html = "🟢 HIGH"

        elif confidence == "Medium":

            confidence_html = "🟡 MEDIUM"

        else:

            confidence_html = "🔴 LOW"

        return f"""
        {response.text}

        ---
        🎯 {confidence_html}
        📚 Sources

        {source_text}
        """

    except Exception as e:

        error = str(e)

        if "429" in error:

            return (
                "⚠ Gemini API quota exceeded.\n\n"
                "The knowledge base is working, "
                "but the AI service has temporarily "
                "reached its limit. Please try again later."
            )

        return f"Error: {error}"