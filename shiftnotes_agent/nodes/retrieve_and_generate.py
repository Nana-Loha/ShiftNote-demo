import pathlib
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import chromadb
from sentence_transformers import SentenceTransformer

from shiftnotes_agent.state import ShiftNotesState
from shiftnotes_agent.logger import get_logger, log_node_entry, log_node_exit, log_error

load_dotenv()
logger = get_logger("retrieve_and_generate")

# Lazy-initialized so the module can be imported without API keys set
_llm = None
_embed_model = None

# Must match the collection name and model used in prototype/rag/embed.py
CHROMA_COLLECTION = "shift_reports"
_CHROMA_DIR = str(pathlib.Path(__file__).parent.parent.parent / "chroma_db")
_EMBED_MODEL_NAME = "all-MiniLM-L6-v2"


def _get_llm():
    global _llm
    if _llm is None:
        _llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    return _llm


def _get_embed_model():
    global _embed_model
    if _embed_model is None:
        _embed_model = SentenceTransformer(_EMBED_MODEL_NAME)
    return _embed_model


def retrieve_and_generate(state: ShiftNotesState) -> ShiftNotesState:
    run_id = state.get("run_id", "unknown")
    log_node_entry(logger, "retrieve_and_generate", run_id)

    try:
        if state.get("error"):
            return state

        detected_signals = state.get("detected_signals", [])

        if not detected_signals:
            log_node_exit(logger, "retrieve_and_generate", run_id, "no signals — skipping RAG")
            return {
                **state,
                "retrieved_context": "",
                "generated_briefing": "No operational signals detected this period."
            }

        raw_reports = state.get("raw_reports", [])

        # --- Step 1: Retrieve historical context from ChromaDB ---
        retrieved_context = _retrieve_context(detected_signals)

        # --- Step 2: Generate briefing with OpenAI ---
        generated_briefing = _generate_briefing(detected_signals, raw_reports, retrieved_context)

        log_node_exit(logger, "retrieve_and_generate", run_id, "briefing generated")

        return {
            **state,
            "retrieved_context": retrieved_context,
            "generated_briefing": generated_briefing
        }

    except Exception as e:
        log_error(logger, "retrieve_and_generate", run_id, str(e))
        return {
            **state,
            "error": f"retrieve_and_generate failed: {str(e)}"
        }


def _retrieve_context(detected_signals: list[dict]) -> str:
    """
    Searches ChromaDB for historical reports similar to the detected signals.
    Uses the same collection and embedding model as prototype/rag/embed.py.
    """
    try:
        client = chromadb.PersistentClient(path=_CHROMA_DIR)
        collection = client.get_collection(CHROMA_COLLECTION)

        signal_names = []
        for report in detected_signals:
            for signal in report.get("signals_found", []):
                signal_names.append(signal["name"])

        query = f"operational issues: {', '.join(set(signal_names))}"
        query_embedding = _get_embed_model().encode([query]).tolist()

        results = collection.query(query_embeddings=query_embedding, n_results=3)

        docs = results.get("documents", [[]])[0]
        if docs:
            return "\n".join(docs)
        return "No historical context available yet."

    except Exception:
        # ChromaDB might be empty on first run — that's fine
        return "No historical context available yet."


def _generate_briefing(detected_signals: list[dict], raw_reports: list[dict], context: str) -> str:
    """
    Uses OpenAI to generate a week-by-week operational briefing
    matching the structure of the prototype notebook (Step 8).
    """
    weekly_summary = _build_weekly_summary(detected_signals, raw_reports)

    system_prompt = """You are an operational intelligence assistant for a hospitality company.
Your job is to write clear, concise weekly briefings for Ted, the General Manager.
Write in plain English. Be direct. Focus on what requires attention.
Format: one clearly labelled section per week (Week 1:, Week 2:, etc.), under 300 words total."""

    user_prompt = f"""Write a week-by-week operational briefing based on the data below.
Include one section per week. For each week state the key signals, highest waste kiosk,
and one recommended action.

Weekly data:
{weekly_summary}

Historical context from past reports:
{context}

Write the briefing now."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    response = _get_llm().invoke(messages)
    return response.content


def _build_weekly_summary(detected_signals: list[dict], raw_reports: list[dict]) -> str:
    """
    Groups data by week, matching the prototype notebook Step 6/8 structure.
    Uses raw_reports for total report count and unclaimed lunches (all reports),
    and detected_signals for per-signal counts (only flagged reports).
    """
    from collections import defaultdict, Counter

    # Total counts per week from ALL reports
    weekly_totals: dict = defaultdict(lambda: {
        "total_reports": 0,
        "unclaimed": 0,
        "kiosk_waste": Counter(),
    })
    for r in raw_reports:
        week = r.get("week", "Unknown")
        weekly_totals[week]["total_reports"] += 1
        weekly_totals[week]["unclaimed"] += int(r.get("number_of_unclaimed_lunches") or 0)
        weekly_totals[week]["kiosk_waste"][r.get("kiosk", "Unknown")] += int(
            r.get("number_of_unclaimed_lunches") or 0
        )

    # Signal counts per week from flagged reports only
    weekly_signals: dict = defaultdict(lambda: {
        "chicken_shortage": 0,
        "poke_request": 0,
        "ops_issue": 0,
        "team_recognition": 0,
    })
    for report in detected_signals:
        week = report.get("week", "Unknown")
        for signal in report.get("signals_found", []):
            name = signal["name"]
            if name in weekly_signals[week]:
                weekly_signals[week][name] += 1

    all_weeks = sorted(
        set(list(weekly_totals.keys()) + list(weekly_signals.keys())),
        key=lambda w: (w == "Unknown", w)
    )

    lines = []
    for week in all_weeks:
        totals = weekly_totals[week]
        signals = weekly_signals[week]
        top_kiosk = (
            totals["kiosk_waste"].most_common(1)[0][0]
            if totals["kiosk_waste"] else "N/A"
        )
        lines.append(f"Week {week}:")
        lines.append(f"  - Reports analyzed: {totals['total_reports']}")
        lines.append(f"  - Poke requests: {signals['poke_request']}")
        lines.append(f"  - Chicken shortages: {signals['chicken_shortage']}")
        lines.append(f"  - Operational issues: {signals['ops_issue']}")
        lines.append(f"  - Team recognition: {signals['team_recognition']}")
        lines.append(f"  - Unclaimed lunches: {totals['unclaimed']}")
        lines.append(f"  - Highest waste kiosk: {top_kiosk}")
        lines.append("")

    return "\n".join(lines)