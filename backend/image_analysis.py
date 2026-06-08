import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
from backend.rag import (
    search_documents
)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(
    api_key=api_key
)

vision_model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def analyze_image(image_path):

    try:

        image = Image.open(
            image_path
        )

        prompt = """
Analyze this support-related screenshot.

Identify:

1. Error message
2. Application name if visible
3. Likely issue
4. Keywords for troubleshooting

Return concise text.
"""

        response = vision_model.generate_content(
            [prompt, image]
        )

        return response.text

    except Exception as e:

        return f"Error: {str(e)}"
    
def analyze_and_search(
    image_path
):

    analysis = analyze_image(
        image_path
    )

    docs = search_documents(
        analysis
    )

    context = "\n\n".join(
        docs
    )

    return (
        f"Analysis:\n\n"
        f"{analysis}\n\n"
        f"Relevant KB:\n\n"
        f"{context[:2000]}"
    )