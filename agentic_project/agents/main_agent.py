from langchain_google_vertexai import ChatVertexAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage
import yaml
import os

class Agent:
    def __init__(self):
        self.llm = ChatVertexAI(model_name="gemini-2.0-flash-001", project="gen-ai-poc-onboarding", location="us-central1")
        self.tools_map = {t.name: t for t in self._get_tools()}
        self.llm_with_tools = self.llm.bind_tools(list(self.tools_map.values()))

        # Load system prompt from config
        config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        self.system_prompt = config.get("system_prompt", "You are a helpful AI agent.")

    def _get_tools(self):
        from tools.tool_manager import get_tools
        return get_tools()

    def run(self, message: str) -> str:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=message),
        ]
        # Agentic loop: keep calling LLM until no more tool calls
        for _ in range(10):  # max iterations to prevent infinite loops
            response = self.llm_with_tools.invoke(messages)
            messages.append(response)
            if not response.tool_calls:
                break
            # Execute each tool call and feed results back
            for tc in response.tool_calls:
                fn = self.tools_map.get(tc["name"])
                tool_name = tc["name"]
                user_query = message  # Capture the original user query
                tool_result = fn.invoke(tc["args"]) if fn else f"Unknown tool: {tc['name']}"
                messages.append(ToolMessage(content=str(tool_result), tool_call_id=tc["id"]))

                # Ingest MCP data to RAG
                self._ingest_to_rag(user_query, str(tool_result), tool_name)

        return response.content if hasattr(response, "content") else str(response)

    def _ingest_to_rag(self, query: str, mcp_result: str, tool_name: str = "mcp_tool") -> None:
        """Ingest MCP-fetched data into ChromaDB for future RAG retrieval."""
        try:
            import chromadb, hashlib, os
            from datetime import datetime
            chroma_path = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
            client = chromadb.PersistentClient(path=os.path.abspath(chroma_path))
            collection = client.get_or_create_collection("knowledge_base", metadata={"hnsw:space": "cosine"})
            doc_id = "mcp_" + hashlib.md5(f"{tool_name}:{query}".encode()).hexdigest()[:16]
            chunk_id = f"{doc_id}_chunk_0"
            collection.upsert(
                ids=[chunk_id],
                documents=[f"Tool: {tool_name}\nQuery: {query}\nResult: {mcp_result}"],
                metadatas=[{"doc_id": doc_id, "title": f"MCP: {tool_name}", "source": "mcp_tool",
                             "chunk_index": 0, "ingested_at": datetime.utcnow().isoformat()}],
            )
        except Exception as e:
            pass  # RAG ingestion is best-effort, never block the response