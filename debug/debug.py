"""
Quick manual retrieval/answer testing tool. Run from the project root:

    python debug/debug.py ask "What B.Tech programs does SMIT offer?"
    python debug/debug.py raw "How do I get admission into SMIT"
    python debug/debug.py webonly "How do I get admission into SMIT"
    python debug/debug.py page "https://smu.edu.in/smit/eligibility-criteria.php"

Modes:
  ask     - runs the real qa_chain (empty chat history) and prints the
            answer + actual source documents used.
  raw     - shows the top 10 raw similarity matches across ALL chunks
            (webpages + PDFs mixed), bypassing the two-stage retriever.
  webonly - same as raw, but filtered to webpage chunks only.
  page    - dumps every stored chunk for one exact source URL/path.
"""

import os
import sys

# Allow running this script directly from inside debug/ while still
# importing project-root modules (config, rag, etc).
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.retriever import vectorstore
from rag.chain import qa_chain

mode = sys.argv[1] if len(sys.argv) > 1 else "ask"

if mode == "ask":
    question = sys.argv[2]
    result = qa_chain.invoke({"question": question, "chat_history": []})
    print(result["answer"])
    print("\nSources:")
    for doc in result["source_documents"]:
        print(" -", doc.metadata.get("source"))

elif mode == "raw":
    question = sys.argv[2]
    results = vectorstore.similarity_search_with_score(question, k=10)
    for doc, score in results:
        print(f"{score:.4f} | {doc.metadata.get('source')}")
        print("   ", doc.page_content[:150])
        print()

elif mode == "page":
    source_url = sys.argv[2]
    results = vectorstore.get(where={"source": source_url})
    for doc in results["documents"]:
        print(doc[:300])
        print("---")

elif mode == "webonly":
    question = sys.argv[2]
    results = vectorstore.similarity_search_with_score(question, k=10, filter={"type": "webpage"})
    for doc, score in results:
        print(f"{score:.4f} | {doc.metadata.get('source')}")
        print("   ", doc.page_content[:150])
        print()

else:
    print(f"Unknown mode: {mode}")
    print("Use one of: ask, raw, webonly, page")