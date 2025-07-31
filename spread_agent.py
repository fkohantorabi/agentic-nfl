from agno.agent import Agent
from agno.document.base import Document
from agno.embedder.google import GeminiEmbedder
from agno.knowledge.document import DocumentKnowledgeBase
from gemini import Gemini
from agno.storage.sqlite import SqliteStorage
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.reasoning import ReasoningTools
from website import WebsiteTools
from agno.vectordb.lancedb import LanceDb, SearchType


def read_file(file_path="instructions.txt"):
    try:
        with open(file_path, 'r') as file:
            # Read the entire file content as a single string with new line characters
            content = file.read()
            return content
    except Exception as e:
        print(f"Error reading instructions file: {e}")
        return ""


knowledge = DocumentKnowledgeBase(
    documents=[Document(content=read_file("player_roles.txt"))],
    vector_db=LanceDb(
        uri="db/lancedb",
        table_name="agno_docs",
        search_type=SearchType.hybrid,
        # Use OpenAI for embeddings
        embedder=GeminiEmbedder(dimensions=1536),
    ),
)

# Store agent sessions in a SQLite database
# storage = SqliteStorage(table_name="agent_sessions", db_file="db/agent.db")


# Initialize instructions from file
instructions = read_file("instructions.txt")

agent = Agent(
    name="Agno Assist",
    model=Gemini(id="gemini-2.0-flash-exp", rate_limit=10),
    instructions=instructions,
    tools=[ReasoningTools(add_instructions=True), WebsiteTools(), GoogleSearchTools()],
    knowledge=knowledge,
#    storage=storage,
    add_datetime_to_instructions=True,
    # Add the chat history to the messages
    add_history_to_messages=True,
    # Number of history runs
    num_history_runs=3,
    markdown=True,
)

if __name__ == "__main__":
    # Load the knowledge base, comment out after first run
    # Set recreate to True to recreate the knowledge base if needed
    agent.knowledge.load(recreate=False)
    agent.print_response("Dallas Cowboys +6.5 Philadelphia Eagles", stream=True,
                         show_full_reasoning=True,
                         stream_intermediate_steps=True)
