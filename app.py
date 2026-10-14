import html
import time

import streamlit as st
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ── Updated visual design ────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --bg: #0b1020;
        --panel: #111a2d;
        --panel-soft: rgba(17, 26, 45, .76);
        --text: #edf3ff;
        --muted: #9aa9c2;
        --accent: #69e2d0;
        --accent-2: #8b9cff;
        --line: rgba(155, 178, 220, .16);
        --success: #76e2a7;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--text);
    }
    .stApp {
        background: var(--bg);
        background-image:
            radial-gradient(ellipse 70% 42% at 8% 0%, rgba(105,226,208,.12), transparent 65%),
            radial-gradient(ellipse 55% 40% at 95% 15%, rgba(139,156,255,.12), transparent 65%);
    }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { max-width: 1240px; padding: 1.7rem 2.2rem 3rem; }

    .topline {
        display: flex; align-items: center; justify-content: space-between;
        gap: 1rem; padding: .65rem 0 1.2rem; border-bottom: 1px solid var(--line);
        margin-bottom: 1.7rem;
    }
    .brand { display: flex; align-items: center; gap: .7rem; font-weight: 700; letter-spacing: -.02em; }
    .brand-mark {
        display: grid; place-items: center; width: 2.3rem; height: 2.3rem;
        border-radius: .75rem; color: #07131d; font-size: 1.1rem;
        background: linear-gradient(135deg, var(--accent), #8b9cff);
        box-shadow: 0 0 24px rgba(105,226,208,.18);
    }
    .top-tag {
        font: 500 .68rem 'DM Mono', monospace; letter-spacing: .12em; text-transform: uppercase;
        color: var(--accent); border: 1px solid rgba(105,226,208,.28);
        background: rgba(105,226,208,.06); border-radius: 999px; padding: .42rem .75rem;
    }
    .hero { padding: 1.2rem 0 1.6rem; }
    .eyebrow { color: var(--accent); text-transform: uppercase; letter-spacing: .2em;
        font: 500 .7rem 'DM Mono', monospace; margin-bottom: .8rem; }
    .hero h1 { font: 700 clamp(2.5rem, 5vw, 4.3rem)/1.04 'Space Grotesk', sans-serif;
        letter-spacing: -.055em; margin: 0 0 .85rem; color: var(--text); }
    .hero h1 span { color: var(--accent); }
    .hero p { color: var(--muted); max-width: 670px; font-size: 1.02rem; line-height: 1.75; margin: 0; }
    .hero-rule { height: 1px; margin: 1.5rem 0 1.8rem;
        background: linear-gradient(90deg, var(--accent), rgba(139,156,255,.35), transparent); }

    .section-title { font: 600 1.15rem 'Space Grotesk', sans-serif; margin: .2rem 0 1rem; }
    .section-kicker { color: var(--muted); font: .68rem 'DM Mono', monospace;
        text-transform: uppercase; letter-spacing: .15em; margin-bottom: .5rem; }
    .input-card {
        background: var(--panel-soft); border: 1px solid var(--line); border-radius: 18px;
        padding: 1.35rem 1.4rem 1.25rem; box-shadow: 0 16px 44px rgba(0,0,0,.12);
    }
    .stTextInput label { color: #c9d5eb !important; font-size: .82rem !important; font-weight: 600 !important; }
    .stTextInput input {
        background: #0b1325 !important; color: var(--text) !important;
        border: 1px solid rgba(155,178,220,.25) !important; border-radius: 11px !important;
        min-height: 3rem !important;
    }
    .stTextInput input:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 2px rgba(105,226,208,.12) !important; }
    .stTextInput input::placeholder { color: #71819c !important; }
    .stButton > button, .stDownloadButton > button {
        border: 1px solid transparent !important; border-radius: 11px !important;
        background: linear-gradient(110deg, var(--accent), #a5b2ff) !important;
        color: #07131d !important; font-weight: 700 !important;
        min-height: 2.85rem; transition: transform .15s ease, filter .15s ease;
    }
    .stButton > button:hover, .stDownloadButton > button:hover { transform: translateY(-1px); filter: brightness(1.05); }
    .stButton > button:focus, .stDownloadButton > button:focus { box-shadow: 0 0 0 3px rgba(105,226,208,.18) !important; }

    .example-label { color: var(--muted); font: .68rem 'DM Mono', monospace; letter-spacing: .12em; margin: .95rem 0 .55rem; }
    .example-chip { display: inline-block; border: 1px solid var(--line); background: rgba(255,255,255,.025);
        color: #c2cde0; border-radius: 8px; padding: .4rem .6rem; margin: 0 .35rem .35rem 0; font-size: .75rem; }
    .pipeline-card {
        display: flex; gap: .85rem; align-items: flex-start; padding: 1rem;
        margin-bottom: .65rem; border-radius: 13px; border: 1px solid var(--line);
        background: rgba(17,26,45,.72);
    }
    .pipeline-num { flex: 0 0 2rem; width: 2rem; height: 2rem; display: grid; place-items: center;
        border: 1px solid rgba(105,226,208,.24); border-radius: 9px; color: var(--accent);
        background: rgba(105,226,208,.07); font: .72rem 'DM Mono', monospace; }
    .pipeline-copy { flex: 1; min-width: 0; }
    .pipeline-title { font-weight: 700; font-size: .9rem; margin: .05rem 0 .25rem; color: var(--text); }
    .pipeline-desc { font-size: .78rem; line-height: 1.5; color: var(--muted); }
    .pipeline-status { font: .62rem 'DM Mono', monospace; letter-spacing: .07em; white-space: nowrap; padding-top: .2rem; color: #71819c; }
    .pipeline-card.active { border-color: rgba(105,226,208,.48); background: rgba(105,226,208,.055); }
    .pipeline-card.active .pipeline-status { color: var(--accent); }
    .pipeline-card.done { border-color: rgba(118,226,167,.32); }
    .pipeline-card.done .pipeline-num { color: var(--success); border-color: rgba(118,226,167,.3); background: rgba(118,226,167,.07); }
    .pipeline-card.done .pipeline-status { color: var(--success); }

    .result-heading { font: 600 1.35rem 'Space Grotesk', sans-serif; margin: .5rem 0 1rem; }
    .result-box { border: 1px solid var(--line); border-radius: 15px; padding: 1.25rem 1.35rem;
        background: rgba(17,26,45,.62); margin: .7rem 0 1rem; }
    .result-label { color: var(--accent); font: 500 .68rem 'DM Mono', monospace;
        letter-spacing: .15em; text-transform: uppercase; border-bottom: 1px solid var(--line);
        padding-bottom: .7rem; margin-bottom: .9rem; }
    .report-box { border: 1px solid rgba(105,226,208,.24); border-radius: 16px;
        padding: 1.3rem 1.4rem; background: rgba(17,26,45,.78); }
    .feedback-box { border: 1px solid rgba(118,226,167,.22); border-radius: 16px;
        padding: 1.3rem 1.4rem; background: rgba(17,26,45,.65); margin-top: 1rem; }
    .footer-note { text-align: center; color: #667792; font: .67rem 'DM Mono', monospace;
        letter-spacing: .07em; padding: 2.5rem 0 .5rem; }
    .stSpinner > div { border-top-color: var(--accent) !important; }
    details summary { color: #c2cde0 !important; font-size: .84rem !important; }
    [data-testid="stAlert"] { border-radius: 12px; }

    @media (max-width: 760px) {
        .block-container { padding: 1rem 1rem 2rem; }
        .topline { align-items: flex-start; }
        .top-tag { font-size: .57rem; }
        .hero { padding-top: .6rem; }
        .input-card { padding: 1rem; }
        .pipeline-status { font-size: .56rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Helpers ───────────────────────────────────────────────────────────────────
def render_pipeline_step(num: str, title: str, desc: str, state: str) -> None:
    status = {"waiting": "WAITING", "running": "● RUNNING", "done": "✓ DONE"}.get(state, "WAITING")
    card_class = "active" if state == "running" else ("done" if state == "done" else "")
    st.markdown(
        f"""
        <div class="pipeline-card {card_class}">
            <div class="pipeline-num">{html.escape(num)}</div>
            <div class="pipeline-copy">
                <div class="pipeline-title">{html.escape(title)}</div>
                <div class="pipeline-desc">{html.escape(desc)}</div>
            </div>
            <div class="pipeline-status">{status}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status(step: str, results: dict, is_running: bool) -> str:
    steps = ["search", "reader", "writer", "critic"]
    if step in results:
        return "done"
    if is_running:
        for item in steps:
            if item not in results:
                return "running" if item == step else "waiting"
    return "waiting"


# ── Session state ─────────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = {}
if "running" not in st.session_state:
    st.session_state.running = False
if "done" not in st.session_state:
    st.session_state.done = False


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="topline">
        <div class="brand"><div class="brand-mark">✳</div><span>ResearchMind</span></div>
        <div class="top-tag">Multi-agent research system</div>
    </div>
    <div class="hero">
        <div class="eyebrow">Research, synthesized by AI</div>
        <h1>Turn a question into<br><span>clear insight.</span></h1>
        <p>Four specialized stages work together to search the web, read relevant sources, draft a research report, and review the final result.</p>
    </div>
    <div class="hero-rule"></div>
    """,
    unsafe_allow_html=True,
)


# ── Main layout ───────────────────────────────────────────────────────────────
col_input, col_pipeline = st.columns([1.08, 0.92], gap="large")

with col_input:
    st.markdown('<div class="section-kicker">01 / Start your research</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">What do you want to explore?</div>', unsafe_allow_html=True)
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Recent progress in small language models",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("✦  Run research pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="example-label">QUICK IDEAS</div>', unsafe_allow_html=True)
    examples = ["AI agents and workflows", "CRISPR gene editing", "Fusion energy progress"]
    st.markdown(
        "".join(f'<span class="example-chip">{html.escape(example)}</span>' for example in examples),
        unsafe_allow_html=True,
    )
    st.caption("Tip: a focused topic usually produces a more useful report.")

with col_pipeline:
    st.markdown('<div class="section-kicker">02 / Behind the scenes</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Research pipeline</div>', unsafe_allow_html=True)
    current_results = st.session_state.results
    render_pipeline_step("01", "Search agent", "Finds relevant web information", render_status("search", current_results, st.session_state.running))
    render_pipeline_step("02", "Reader agent", "Selects a source and extracts details", render_status("reader", current_results, st.session_state.running))
    render_pipeline_step("03", "Writer chain", "Turns findings into a structured report", render_status("writer", current_results, st.session_state.running))
    render_pipeline_step("04", "Critic chain", "Reviews the report for quality and gaps", render_status("critic", current_results, st.session_state.running))


# ── Trigger pipeline ──────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()


# ── Execute pipeline ──────────────────────────────────────────────────────────
if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input.strip()
    try:
        with st.spinner("🔎 Search agent is gathering relevant information…"):
            search_agent = build_search_agent()
            search_response = search_agent.invoke(
                {"messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]}
            )
            results["search"] = search_response["messages"][-1].content
            st.session_state.results = dict(results)

        with st.spinner("📚 Reader agent is exploring a relevant source…"):
            reader_agent = build_reader_agent()
            reader_response = reader_agent.invoke(
                {
                    "messages": [
                        (
                            "user",
                            f"Based on the following search results about '{topic_val}', pick the most relevant URL and scrape it for deeper content.\n\nSearch Results:\n{results['search'][:800]}",
                        )
                    ]
                }
            )
            results["reader"] = reader_response["messages"][-1].content
            st.session_state.results = dict(results)

        with st.spinner("✍️ Writer is drafting the research report…"):
            research_combined = (
                f"SEARCH RESULTS:\n{results['search']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
            )
            results["writer"] = writer_chain.invoke(
                {"topic": topic_val, "research": research_combined}
            )
            st.session_state.results = dict(results)

        with st.spinner("🧭 Critic is reviewing the report…"):
            results["critic"] = critic_chain.invoke({"report": results["writer"]})
            st.session_state.results = dict(results)

        st.session_state.running = False
        st.session_state.done = True
        st.rerun()

    except Exception as exc:
        st.session_state.running = False
        st.error(f"The research pipeline stopped: {type(exc).__name__}: {exc}")
        st.info("Check your model API key, provider quota, and the terminal or Streamlit logs for details.")


# ── Results ───────────────────────────────────────────────────────────────────
r = st.session_state.results
if r:
    st.markdown('<div class="hero-rule"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">03 / Output</div>', unsafe_allow_html=True)
    st.markdown('<div class="result-heading">Your research results</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("🔎 Search agent output", expanded=False):
            st.markdown('<div class="result-label">Search results · raw output</div>', unsafe_allow_html=True)
            st.text(r["search"])

    if "reader" in r:
        with st.expander("📚 Reader agent output", expanded=False):
            st.markdown('<div class="result-label">Source extraction · raw output</div>', unsafe_allow_html=True)
            st.text(r["reader"])

    if "writer" in r:
        st.markdown('<div class="report-box"><div class="result-label">✦ Final research report</div>', unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown('</div>', unsafe_allow_html=True)
        st.download_button(
            label="↓  Download report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    if "critic" in r:
        st.markdown('<div class="feedback-box"><div class="result-label">✓ Critic feedback</div>', unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown('</div>', unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer-note">RESEARCHMIND · LANGCHAIN MULTI-AGENT PIPELINE · BUILT WITH STREAMLIT</div>',
    unsafe_allow_html=True,
)
