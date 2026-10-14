
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY is missing from .env")

llm = ChatOpenAI(
    model="openrouter/free",
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    temperature=0,
    max_retries=1,
    timeout=60,
)

try:
    print("Testing OpenRouter...", flush=True)
    response = llm.invoke(
        "Reply with exactly: RESEARCHMIND WORKS"
    )
    print("SUCCESS:", response.content, flush=True)

except Exception as e:
    print("FAILED:", type(e).__name__, str(e), flush=True)
