
from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain,
)


def run_research_pipeline(topic: str) -> dict:
    topic = topic.strip()

    if not topic:
        raise ValueError("Research topic cannot be empty.")

    state = {
        "topic": topic,
        "search_results": "",
        "scraped_content": "",
        "report": "",
        "feedback": "",
    }

    # Step 1: Search
    print("\n" + "=" * 60)
    print("STEP 1 - SEARCH AGENT")
    print("=" * 60)

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
            (
                "user",
                f"Find recent, reliable and detailed information about: "
                f"{topic}. Use the web_search tool and preserve source URLs."
            )
        ]
    })

    state["search_results"] = search_result["messages"][-1].content
    print(state["search_results"])

    # Step 2: Read a source
    print("\n" + "=" * 60)
    print("STEP 2 - READER AGENT")
    print("=" * 60)

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"Research topic: {topic}\n\n"
                "Select one relevant URL from these search results and "
                "use the scrape_url tool to read it. Do not invent URLs. "
                "Summarize the useful evidence and identify the source URL.\n\n"
                f"Search results:\n{state['search_results'][:6000]}"
            )
        ]
    })

    state["scraped_content"] = reader_result["messages"][-1].content
    print(state["scraped_content"])

    # Step 3: Write report
    print("\n" + "=" * 60)
    print("STEP 3 - REPORT WRITER")
    print("=" * 60)

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
    })

    print(state["report"])

    # Step 4: Critique report
    print("\n" + "=" * 60)
    print("STEP 4 - REPORT CRITIC")
    print("=" * 60)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"],
    })

    print(state["feedback"])

    return state


if __name__ == "__main__":
    research_topic = input("\nEnter a research topic: ")

    try:
        result = run_research_pipeline(research_topic)

        print("\nResearch pipeline completed successfully.")

    except Exception as exc:
        print(f"\nResearch pipeline failed: {exc}")
        raise
