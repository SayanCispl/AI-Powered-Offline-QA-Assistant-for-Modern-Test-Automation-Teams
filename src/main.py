import os
import time
import logging

from logging.handlers import RotatingFileHandler

from pythonjsonlogger import jsonlogger
from dotenv import load_dotenv

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from rich.text import Text

from src.qa_agent import QAAIAgent


# =====================================================
# LOAD ENV VARIABLES
# =====================================================
load_dotenv()

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
).upper()

DEBUG_MODE = (
    os.getenv("DEBUG", "false")
    .lower() == "true"
)

# =====================================================
# RICH CONSOLE
# =====================================================
console = Console()

# =====================================================
# ENSURE LOG DIRECTORY EXISTS
# =====================================================
os.makedirs("logs", exist_ok=True)

# =====================================================
# LOGGER CONFIGURATION
# =====================================================
logger = logging.getLogger("qa_ai_agent")

logger.setLevel(LOG_LEVEL)

# Prevent duplicate logs
logger.handlers.clear()

# JSON FORMATTER
json_formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s"
)

# FILE HANDLER
file_handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=5 * 1024 * 1024,
    backupCount=3
)

file_handler.setFormatter(
    json_formatter
)

# CONSOLE HANDLER
console_handler = logging.StreamHandler()

console_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# =====================================================
# SAFE EXECUTION WRAPPER
# =====================================================
def safe_execute(func):

    try:
        return func()

    except Exception:

        logger.exception(
            "Unhandled exception occurred"
        )

        console.print(
            "\n[bold red]"
            "An unexpected error occurred."
            "\nCheck logs/app.log"
            "[/bold red]"
        )

# =====================================================
# BEAUTIFUL HEADER
# =====================================================
def show_banner():

    console.print("\n")

    subtitle = (
        "[bold white]"
        "Offline AI-Powered QA Assistant "
        "with RAG + Ollama + ChromaDB"
        "[/bold white]"
    )

    console.print(
        Panel.fit(
            subtitle,
            title="🧠 QA Intelligence Platform",
            border_style="cyan",
            padding=(1, 4)
        )
    )

# =====================================================
# MENU TABLE
# =====================================================
def show_menu():

    table = Table(
        title="📋 Available Actions",
        show_header=True,
        header_style="bold cyan"
    )

    table.add_column(
        "Option",
        style="bold green",
        width=10
    )

    table.add_column(
        "Description",
        style="white"
    )

    table.add_row(
        "1",
        "Generate Test Cases"
    )

    table.add_row(
        "2",
        "Review Existing Test Cases"
    )

    table.add_row(
        "3",
        "Analyze Bug Report"
    )

    table.add_row(
        "4",
        "Analyze Logs / Errors"
    )

    table.add_row(
        "5",
        "Create QA Checklist"
    )

    table.add_row(
        "6",
        "Ask QA Question (RAG)"
    )

    table.add_row(
        "7",
        "Search QA Memory"
    )

    table.add_row(
        "8",
        "Analyze Flaky Automation Failure"
    )

    table.add_row(
        "9",
        "Exit"
    )

    console.print(table)

# =====================================================
# FORMAT AI RESPONSE
# =====================================================
def render_ai_response(
    title,
    content,
    border_style="green"
):

    console.print("\n")

    console.print(
        Panel(
            content,
            title=title,
            border_style=border_style,
            padding=(1, 2)
        )
    )

# =====================================================
# BUILD CONFIDENCE OUTPUT
# =====================================================
def build_confidence_output(
    answer,
    confidence,
    retrieval_time
):

    # =========================================
    # DYNAMIC CONFIDENCE COLOR
    # =========================================
    if confidence >= 80:

        confidence_color = "green"
        confidence_label = "Excellent Match"

    elif confidence >= 60:

        confidence_color = "yellow"
        confidence_label = "Moderate Match"

    else:

        confidence_color = "red"
        confidence_label = "Low Match"

    # =========================================
    # VISUAL CONFIDENCE BAR
    # =========================================
    filled_blocks = int(confidence / 10)

    confidence_bar = (
        "["
        + "█" * filled_blocks
        + "░" * (10 - filled_blocks)
        + "]"
    )

    # =========================================
    # FINAL OUTPUT
    # =========================================
    return (
        f"{answer}\n\n"

        f"[bold {confidence_color}]"
        f"📊 Confidence Score : "
        f"{confidence}%"
        f"[/bold {confidence_color}]\n"

        f"[bold cyan]"
        f"📈 Match Strength   : "
        f"{confidence_bar}"
        f"[/bold cyan]\n"

        f"[bold white]"
        f"🏷️ Confidence Type : "
        f"{confidence_label}"
        f"[/bold white]\n"

        f"[bold magenta]"
        f"⚡ Retrieval Time   : "
        f"{retrieval_time} sec"
        f"[/bold magenta]"
    )

# =====================================================
# MAIN APPLICATION
# =====================================================
def run():

    logger.info(
        "QA AI Agent started",
        extra={
            "debug_mode": DEBUG_MODE
        }
    )

    agent = QAAIAgent()

    show_banner()

    while True:

        show_menu()

        choice = input(
            "\nSelect option: "
        ).strip()

        # =================================================
        # GENERATE TEST CASES
        # =================================================
        if choice == "1":

            def handle_test_cases():

                requirement = input(
                    "\nEnter requirement:\n"
                )

                result = (
                    agent.generate_test_cases(
                        requirement
                    )
                )

                render_ai_response(
                    "🧪 Generated Test Cases",
                    result,
                    "green"
                )

            safe_execute(
                handle_test_cases
            )

        # =================================================
        # REVIEW TEST CASES
        # =================================================
        elif choice == "2":

            def handle_review():

                test_cases = input(
                    "\nPaste test cases:\n"
                )

                result = (
                    agent.review_test_cases(
                        test_cases
                    )
                )

                render_ai_response(
                    "📋 Test Case Review",
                    result,
                    "yellow"
                )

            safe_execute(
                handle_review
            )

        # =================================================
        # BUG ANALYSIS
        # =================================================
        elif choice == "3":

            def handle_bug():

                bug = input(
                    "\nPaste bug report:\n"
                )

                result = (
                    agent.analyze_bug(
                        bug
                    )
                )

                render_ai_response(
                    "🐞 Bug Analysis",
                    result,
                    "red"
                )

            safe_execute(
                handle_bug
            )

        # =================================================
        # LOG ANALYSIS
        # =================================================
        elif choice == "4":

            def handle_logs():

                logs = input(
                    "\nPaste logs/errors:\n"
                )

                result = (
                    agent.analyze_logs(
                        logs
                    )
                )

                render_ai_response(
                    "📄 Log Analysis",
                    result,
                    "magenta"
                )

            safe_execute(
                handle_logs
            )

        # =================================================
        # QA CHECKLIST
        # =================================================
        elif choice == "5":

            def handle_checklist():

                feature = input(
                    "\nEnter feature name:\n"
                )

                result = (
                    agent.create_checklist(
                        feature
                    )
                )

                render_ai_response(
                    "✅ QA Checklist",
                    result,
                    "cyan"
                )

            safe_execute(
                handle_checklist
            )

        # =================================================
        # RAG QUESTION ANSWERING
        # =================================================
        elif choice == "6":

            def handle_rag():

                question = input(
                    "\nAsk your QA question:\n"
                )

                logger.info(
                    "RAG query received",
                    extra={
                        "query": question,
                        "debug_mode": DEBUG_MODE
                    }
                )

                start_time = time.time()

                response = (
                    agent.ask_with_rag(
                        question
                    )
                )

                end_time = time.time()

                retrieval_time = round(
                    end_time - start_time,
                    2
                )

                answer = response.get(
                    "answer",
                    "No answer generated."
                )

                confidence = response.get(
                    "confidence_score",
                    0
                )

                formatted_answer = (
                    build_confidence_output(
                        answer,
                        confidence,
                        retrieval_time
                    )
                )

                render_ai_response(
                    "🧠 QA AI RAG Answer",
                    formatted_answer,
                    "green"
                )

            safe_execute(
                handle_rag
            )

        # =================================================
        # MEMORY SEARCH
        # =================================================
        elif choice == "7":

            def handle_memory():

                query = input(
                    "\nSearch QA memory:\n"
                )

                logger.info(
                    "Memory search",
                    extra={
                        "query": query,
                        "debug_mode": DEBUG_MODE
                    }
                )

                results = (
                    agent.search_memory(
                        query
                    )
                )

                docs = results.get(
                    "documents",
                    []
                )

                distances = results.get(
                    "distances",
                    []
                )

                if not docs:

                    render_ai_response(
                        "🔍 QA Memory Search",
                        "No matching documents found.",
                        "yellow"
                    )

                    return

                output = ""

                for i, doc in enumerate(docs[0]):

                    distance = (
                        distances[0][i]
                    )

                    confidence = round(
                        max(
                            0,
                            min(
                                100,
                                (1 - distance) * 100
                            )
                        ),
                        2
                    )

                    preview = (
                        doc[:350]
                        .replace("\n", " ")
                    )

                    output += (
                        f"\n[Result {i + 1}]\n"
                        f"Confidence: {confidence}%\n"
                        f"{preview}\n\n"
                    )

                render_ai_response(
                    "🔍 QA Memory Results",
                    output,
                    "blue"
                )

            safe_execute(
                handle_memory
            )

        # =================================================
        # ANALYZE FLAKY AUTOMATION FAILURE
        # =================================================
        elif choice == "8":

            def handle_flaky_test():

                failure_log = input(
                    "\nPaste automation failure/log:\n"
                )

                logger.info(
                    "Flaky test RCA analysis",
                    extra={
                        "failure_log": failure_log,
                        "debug_mode": DEBUG_MODE
                    }
                )

                start_time = time.time()

                response = (
                    agent.analyze_flaky_test(
                        failure_log
                    )
                )

                end_time = time.time()

                retrieval_time = round(
                    end_time - start_time,
                    2
                )

                answer = response.get(
                    "answer",
                    "No RCA generated."
                )

                confidence = response.get(
                    "confidence_score",
                    0
                )

                formatted_answer = (
                    build_confidence_output(
                        answer,
                        confidence,
                        retrieval_time
                    )
                )

                render_ai_response(
                    "🧪 AI Flaky Test RCA",
                    formatted_answer,
                    "cyan"
                )

            safe_execute(
                handle_flaky_test
            )

        # =================================================
        # EXIT
        # =================================================
        elif choice == "9":

            logger.info(
                "QA AI Agent stopped"
            )

            console.print(
                "\n[bold red]"
                "Exiting QA AI Agent..."
                "[/bold red]"
            )

            break

        # =================================================
        # INVALID OPTION
        # =================================================
        else:

            console.print(
                "\n[bold red]"
                "Invalid option. "
                "Please try again."
                "[/bold red]"
            )

        console.print(
            Rule(style="dim")
        )