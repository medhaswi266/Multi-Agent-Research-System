import re
import time

import streamlit as st

from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Instrument+Sans:wght@400;500;600&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&display=swap');

:root {
    --ink:      #0f1522;
    --surface:  #172033;
    --surface2: #1d2840;
    --line:     #2a3652;
    --text:     #e6eaf2;
    --muted:    #8b97ad;
    --accent:   #7c8cff;
    --accent-2: #5b6cf0;
    --done:     #3ddc97;
    --paper:    #f7f8fb;
    --paper-ink:#1b2233;
}

/* ── Base ── */
html, body, .stApp {
    font-family: 'Instrument Sans', sans-serif;
    color-scheme: dark;
}
.stApp {
    background: var(--ink);
    background-image:
        radial-gradient(ellipse 70% 45% at 10% -10%, rgba(124,140,255,0.16) 0%, transparent 60%),
        radial-gradient(ellipse 50% 35% at 100% 0%, rgba(61,220,151,0.06) 0%, transparent 60%);
}
.stApp, .stApp label,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4 {
    color: var(--text);
}

/* ── Hide default chrome ── */
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding: 2.2rem 3rem 4rem; max-width: 1100px; }

/* ── Brand bar ── */
.brandbar {
    display: flex; align-items: center; gap: 0.6rem;
    font-family: 'Bricolage Grotesque', sans-serif;
    font-weight: 700; font-size: 1.05rem; color: var(--text);
}
.brandmark {
    width: 28px; height: 28px; border-radius: 8px;
    background: linear-gradient(135deg, var(--accent), var(--accent-2));
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 0.95rem;
}
.brandbar .tag { margin-left: auto; font-weight: 500; font-size: 0.85rem; color: var(--muted); }

/* ── Hero ── */
.hero { padding: 3.2rem 0 1.6rem; }
.hero h1 {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: clamp(2.4rem, 5.2vw, 4.2rem);
    font-weight: 800; line-height: 1.04; letter-spacing: -0.03em;
    color: var(--text); margin: 0 0 1rem; padding: 0; max-width: 17ch;
}
.hero p {
    font-size: 1.08rem; line-height: 1.65; color: var(--muted);
    max-width: 56ch; margin: 0;
}

/* ── Search bar card (st.container key="search_card") ── */
.st-key-search_card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 1.1rem 1.2rem 0.9rem;
    box-shadow: 0 20px 50px rgba(0,0,0,0.35);
}

/* ── Text input: fixes white box / white text ── */
[data-baseweb="input"], [data-baseweb="base-input"] {
    background-color: var(--ink) !important;
    border-radius: 12px !important;
}
[data-baseweb="input"] {
    border: 1px solid var(--line) !important;
    transition: border-color .2s, box-shadow .2s;
}
[data-baseweb="input"]:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(124,140,255,0.22) !important;
}
.stTextInput input {
    background: transparent !important;
    color: #0f1522 !important;
    -webkit-text-fill-color: #0f1522 !important;
    caret-color: #0f1522 !important;
    font-family: 'Instrument Sans', sans-serif !important;
    font-size: 1.02rem !important;
    padding: 0.8rem 1rem !important;
}
.stTextInput input::placeholder {
    color: #6c7891 !important;
    -webkit-text-fill-color: #6c7891 !important;
    opacity: 1 !important;
}

/* ── Buttons ── */
.stButton > button, .stDownloadButton > button {
    font-family: 'Instrument Sans', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    transition: transform .15s, box-shadow .15s, background .15s, border-color .15s !important;
}
/* primary */
.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%) !important;
    color: #ffffff !important;
    border: none !important;
    padding: 0.8rem 1.4rem !important;
    font-size: 0.98rem !important;
    box-shadow: 0 8px 22px rgba(91,108,240,0.38) !important;
}
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 12px 28px rgba(91,108,240,0.5) !important;
}
.stButton > button[kind="primary"] p,
.stButton > button[data-testid="stBaseButton-primary"] p { color: #ffffff !important; }
.st-key-run_btn button { width: 100%; }

/* secondary (example chips + download) */
.stButton > button[kind="secondary"],
.stButton > button[data-testid="stBaseButton-secondary"],
.stDownloadButton > button {
    background: transparent !important;
    color: var(--muted) !important;
    border: 1px solid var(--line) !important;
}
.stButton > button[kind="secondary"]:hover,
.stButton > button[data-testid="stBaseButton-secondary"]:hover,
.stDownloadButton > button:hover {
    color: var(--text) !important;
    border-color: var(--accent) !important;
    background: rgba(124,140,255,0.08) !important;
}
.stButton > button[kind="secondary"] p,
.stButton > button[data-testid="stBaseButton-secondary"] p,
.stDownloadButton > button p { color: inherit !important; }
.st-key-chips button {
    width: 100%; font-size: 0.82rem !important; font-weight: 500 !important;
    padding: 0.3rem 0.6rem !important; border-radius: 999px !important; min-height: 0 !important;
}
.chips-label { font-size: 0.85rem; color: var(--muted); margin: 0.2rem 0 0.4rem; }

/* ── Pipeline ── */
.pipe-title {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 1.15rem; font-weight: 700; color: var(--text); margin: 2.4rem 0 0.9rem;
}
.pipeline {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 0.9rem;
}
.pstep {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 1.1rem 1.2rem 1.15rem;
    position: relative;
    transition: border-color .3s, background .3s;
}
.pstep::after {
    content: ''; position: absolute; left: 0; right: 0; bottom: 0; height: 3px;
    border-radius: 0 0 14px 14px; background: var(--line); transition: background .3s;
}
.pstep.running { border-color: rgba(124,140,255,0.6); background: var(--surface2); }
.pstep.running::after { background: var(--accent); }
.pstep.done { border-color: rgba(61,220,151,0.35); }
.pstep.done::after { background: var(--done); }
.pstep-top { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.55rem; }
.pstep-num {
    width: 24px; height: 24px; border-radius: 50%;
    background: var(--ink); border: 1px solid var(--line);
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 0.74rem; font-weight: 600; color: var(--muted);
}
.pstep.running .pstep-num { border-color: var(--accent); color: var(--accent); }
.pstep.done .pstep-num { background: var(--done); border-color: var(--done); color: #08261a; }
.pstep-status { margin-left: auto; font-size: 0.78rem; color: var(--muted); display: flex; align-items: center; gap: 0.35rem; }
.pstep.running .pstep-status { color: var(--accent); }
.pstep.done .pstep-status { color: var(--done); }
.dot { width: 7px; height: 7px; border-radius: 50%; background: currentColor; }
.pstep.running .dot { animation: pulse 1.1s ease-in-out infinite; }
@keyframes pulse { 0%,100% { opacity: .25; } 50% { opacity: 1; } }
@media (prefers-reduced-motion: reduce) { .pstep.running .dot { animation: none; } }
.pstep-name {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 1rem; font-weight: 700; color: var(--text);
}
.pstep-desc { font-size: 0.85rem; color: var(--muted); margin-top: 0.2rem; line-height: 1.45; }

/* ── Progress bar ── */
[data-testid="stProgress"] > div > div { background-color: var(--line) !important; }
[data-testid="stProgress"] [role="progressbar"] > div { background: var(--accent) !important; }
[data-testid="stProgress"] p { color: var(--muted) !important; font-size: 0.85rem; }

/* ── Results heading ── */
.results-title {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 1.6rem; font-weight: 800; letter-spacing: -0.02em;
    color: var(--text); margin: 2.8rem 0 0.4rem;
}
.results-sub { color: var(--muted); font-size: 0.95rem; margin-bottom: 0.6rem; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { gap: 0.4rem; border-bottom: 1px solid var(--line); }
.stTabs [data-baseweb="tab"] {
    background: transparent; color: var(--muted);
    font-family: 'Instrument Sans', sans-serif; font-weight: 600; font-size: 0.95rem;
    padding: 0.6rem 1rem;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--text); }
.stTabs [aria-selected="true"] { color: var(--text) !important; }
.stTabs [data-baseweb="tab-highlight"] { background-color: var(--accent) !important; }
.stTabs [data-baseweb="tab-border"] { display: none; }

/* ── Report "paper" (st.container key="report_paper") ── */
.st-key-report_paper {
    background: var(--paper);
    border-radius: 16px;
    padding: 2.4rem 3rem;
    margin-top: 1rem;
    box-shadow: 0 24px 60px rgba(0,0,0,0.4);
}
.stApp .st-key-report_paper,
.stApp .st-key-report_paper * { color: var(--paper-ink); }
.stApp .st-key-report_paper p,
.stApp .st-key-report_paper li {
    font-family: 'Newsreader', Georgia, serif;
    font-size: 1.1rem; line-height: 1.75;
}
.stApp .st-key-report_paper h1,
.stApp .st-key-report_paper h2,
.stApp .st-key-report_paper h3 {
    font-family: 'Bricolage Grotesque', sans-serif;
    letter-spacing: -0.02em; font-weight: 800;
}
.stApp .st-key-report_paper h2 { font-size: 1.45rem; margin-top: 1.6rem; }
.stApp .st-key-report_paper a { color: #3b4bd6; text-decoration: underline; }

/* ── Critic card (st.container key="critic_card") ── */
.st-key-critic_card {
    background: var(--surface);
    border: 1px solid rgba(61,220,151,0.3);
    border-radius: 16px;
    padding: 1.8rem 2.2rem;
    margin-top: 1rem;
}
.score-badge {
    display: inline-flex; align-items: baseline; gap: 0.25rem;
    background: rgba(61,220,151,0.12); border: 1px solid rgba(61,220,151,0.4);
    border-radius: 12px; padding: 0.5rem 1rem; margin-bottom: 1rem;
    font-family: 'Bricolage Grotesque', sans-serif;
}
.score-badge .big { font-size: 2rem; font-weight: 800; color: var(--done); line-height: 1; }
.score-badge .of { font-size: 0.95rem; color: var(--muted); }

/* ── Expanders ── */
[data-testid="stExpander"] {
    background: var(--surface); border: 1px solid var(--line) !important; border-radius: 12px;
}
[data-testid="stExpander"] summary p { color: var(--text) !important; font-weight: 600; }

/* ── Alerts ── */
[data-testid="stAlert"] { border-radius: 12px; }

/* ── Footer ── */
.footer { text-align: center; color: #5f6b84; font-size: 0.82rem; margin-top: 4rem; }

@media (max-width: 640px) {
    .block-container { padding: 1.4rem 1.1rem 3rem; }
    .st-key-report_paper { padding: 1.4rem 1.2rem; }
}
</style>
""",
    unsafe_allow_html=True,
)


# ── Helpers ──────────────────────────────────────────────────────────────────
STEPS = [
    ("search", "Search agent", "Finds recent sources on your topic"),
    ("reader", "Reader agent", "Opens the best source and extracts detail"),
    ("writer", "Writer", "Drafts a structured report"),
    ("critic", "Critic", "Scores the report and flags gaps"),
]


def render_pipeline(placeholder, results: dict, running: bool):
    """Draw the four pipeline steps with their current state."""
    cards = []
    running_assigned = False
    for i, (key, name, desc) in enumerate(STEPS, start=1):
        if key in results:
            state, label, num = "done", "Done", "✓"
        elif running and not running_assigned:
            state, label, num = "running", "Working", str(i)
            running_assigned = True
        else:
            state, label, num = "waiting", "Waiting", str(i)
        cards.append(
            f'<div class="pstep {state}">'
            f'<div class="pstep-top"><span class="pstep-num">{num}</span>'
            f'<span class="pstep-status"><span class="dot"></span>{label}</span></div>'
            f'<div class="pstep-name">{name}</div>'
            f'<div class="pstep-desc">{desc}</div>'
            f"</div>"
        )
    placeholder.markdown(
        '<div class="pipeline">' + "".join(cards) + "</div>", unsafe_allow_html=True
    )


def set_topic(value: str):
    st.session_state.topic_input = value


def extract_score(text: str):
    m = re.search(r"Score:\s*(\d+(?:\.\d+)?)\s*/\s*10", text)
    return m.group(1) if m else None


# ── Session state ────────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = {}
if "report_topic" not in st.session_state:
    st.session_state.report_topic = ""


# ── Brand bar + hero ─────────────────────────────────────────────────────────
st.markdown(
    """
<div class="brandbar"><span class="brandmark">🔬</span>ResearchMind<span class="tag">Multi-agent research assistant</span></div>
<div class="hero">
<h1>Ask a question. Four agents write the report.</h1>
<p>ResearchMind searches the web, reads the best source, drafts a structured report and then critiques it, so you get a result you can trust and check.</p>
</div>
""",
    unsafe_allow_html=True,
)

# ── Search card ──────────────────────────────────────────────────────────────
with st.container(key="search_card"):
    c_in, c_btn = st.columns([5, 1.6], vertical_alignment="center")
    with c_in:
        topic = st.text_input(
            "Research topic",
            placeholder="e.g. Quantum computing breakthroughs in 2025",
            key="topic_input",
            label_visibility="collapsed",
        )
    with c_btn:
        with st.container(key="run_btn"):
            run_btn = st.button("Run research", type="primary")

    st.markdown('<div class="chips-label">Or try one of these:</div>', unsafe_allow_html=True)
    examples = ["LLM agents in 2025", "CRISPR gene editing", "Fusion energy progress", "Edge AI chips"]
    with st.container(key="chips"):
        chip_cols = st.columns(len(examples))
        for i, ex in enumerate(examples):
            with chip_cols[i]:
                st.button(ex, key=f"chip_{i}", on_click=set_topic, args=(ex,))

# ── Pipeline (updates live while running) ───────────────────────────────────
st.markdown('<div class="pipe-title">How it works</div>', unsafe_allow_html=True)
pipeline_ph = st.empty()
progress_ph = st.empty()
render_pipeline(pipeline_ph, st.session_state.results, False)

# ── Run ──────────────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Enter a research topic to get started.")
    else:
        results = {}
        st.session_state.results = {}
        current = "search"
        try:
            render_pipeline(pipeline_ph, results, True)
            progress_ph.progress(0.05, text="Search agent is finding sources…")
            search_agent = build_search_agent()
            sr = search_agent.invoke(
                {"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]}
            )
            results["search"] = sr["messages"][-1].content

            current = "reader"
            render_pipeline(pipeline_ph, results, True)
            progress_ph.progress(0.30, text="Reader agent is scraping the best source…")
            reader_agent = build_reader_agent()
            rr = reader_agent.invoke(
                {
                    "messages": [
                        (
                            "user",
                            f"Based on the following search results about '{topic}', "
                            f"pick the most relevant URL and scrape it for deeper content.\n\n"
                            f"Search Results:\n{results['search'][:800]}",
                        )
                    ]
                }
            )
            results["reader"] = rr["messages"][-1].content

            current = "writer"
            render_pipeline(pipeline_ph, results, True)
            progress_ph.progress(0.55, text="Writer is drafting the report…")
            research_combined = (
                f"SEARCH RESULTS:\n{results['search']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
            )
            results["writer"] = writer_chain.invoke({"topic": topic, "research": research_combined})

            current = "critic"
            render_pipeline(pipeline_ph, results, True)
            progress_ph.progress(0.85, text="Critic is reviewing the report…")
            results["critic"] = critic_chain.invoke({"report": results["writer"]})

            progress_ph.progress(1.0, text="Done")
            render_pipeline(pipeline_ph, results, False)
            st.session_state.results = results
            st.session_state.report_topic = topic.strip()
            time.sleep(0.6)
            progress_ph.empty()
        except Exception as e:
            progress_ph.empty()
            render_pipeline(pipeline_ph, results, False)
            st.session_state.results = results
            st.error(
                f"The {current} step failed. Check that GROQ_API_KEY and TAVILY_API_KEY "
                f"are set, then run it again."
            )
            with st.expander("Error details"):
                st.code(str(e))


# ── Results ──────────────────────────────────────────────────────────────────
r = st.session_state.results

if "writer" in r:
    st.markdown(
        f'<div class="results-title">Your report</div>'
        f'<div class="results-sub">Topic: {st.session_state.report_topic.replace("<", "&lt;")}</div>',
        unsafe_allow_html=True,
    )

    tab_report, tab_critic, tab_sources = st.tabs(["Report", "Critic review", "Sources & raw data"])

    with tab_report:
        with st.container(key="report_paper"):
            st.markdown(r["writer"])
        st.write("")
        st.download_button(
            label="Download report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    with tab_critic:
        if "critic" in r:
            with st.container(key="critic_card"):
                score = extract_score(r["critic"])
                if score:
                    st.markdown(
                        f'<div class="score-badge"><span class="big">{score}</span>'
                        f'<span class="of">/ 10</span></div>',
                        unsafe_allow_html=True,
                    )
                st.markdown(r["critic"])
        else:
            st.info("The critic review didn't finish. Run the pipeline again.")

    with tab_sources:
        with st.expander("Search agent output", expanded=False):
            st.markdown(r.get("search", "No search output."))
        with st.expander("Reader agent output (scraped content)", expanded=False):
            st.markdown(r.get("reader", "No scraped content."))


# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer">ResearchMind · Built with LangChain and Streamlit</div>',
    unsafe_allow_html=True,
)
