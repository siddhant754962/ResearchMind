
from agents import (
    llm,
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)

def main():
    print("\n=== Testing Groq LLM ===")
    response = llm.invoke("Explain RAG in two sentences.")
    print(response.content)
    print("LLM passed!")

    print("\n=== Testing Search Agent ===")
    search_agent = build_search_agent()
    result = search_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": "Find recent developments in data analytics."
            }
        ]
    })
    print(result["messages"][-1].content)
    print("Search agent completed!")

    print("\n=== Testing Reader Agent ===")
    reader_agent = build_reader_agent()
    result = reader_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": "Read https://example.com and summarize it."
            }
        ]
    })
    print(result["messages"][-1].content)
    print("Reader agent completed!")

    print("\n=== Testing Writer Chain ===")
    report = writer_chain.invoke({
        "topic": "Applications of AI in data analytics",
        "research": (
            "AI helps automate data analysis. "
            "Source: https://example.com"
        ),
    })
    print(report)

    print("\n=== Testing Critic Chain ===")
    review = critic_chain.invoke({"report": report})
    print(review)

if __name__ == "__main__":
    main()
