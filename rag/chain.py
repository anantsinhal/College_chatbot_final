from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI

from config import GOOGLE_API_KEY, LLM_MODEL, LLM_TEMPERATURE
from rag.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT
from rag.retriever import retriever

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY is not set. Add it to a .env file in the project root."
    )

llm = ChatGoogleGenerativeAI(
    model=LLM_MODEL,
    google_api_key=GOOGLE_API_KEY,
    temperature=LLM_TEMPERATURE,
)

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
    condense_question_prompt=CONDENSE_QUESTION_PROMPT,
    combine_docs_chain_kwargs={"prompt": QA_PROMPT},
)
