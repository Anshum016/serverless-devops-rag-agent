import os
import boto3
from typing import TypedDict
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langgraph.graph import StateGraph, END

load_dotenv()

#This function will load the vectors from s3
def load_vector_store():
    s3_bucket = os.environ.get("BUCKET_NAME")
    if not s3_bucket:
        raise ValueError("environment variable is missing. Cannot load from S3.")    
    local_path = "/tmp/faiss_index"
    # Initialize Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    # AWS Lambda Logic
    if not os.path.exists(f"{local_path}/index.faiss"):
        print(f"Downloading Vector DB from S3: {s3_bucket}")
        s3 = boto3.client('s3')
        try:
            os.makedirs(local_path, exist_ok=True)
            s3.download_file(s3_bucket, "vectors/index.faiss", f"{local_path}/index.faiss")
            s3.download_file(s3_bucket, "vectors/index.pkl", f"{local_path}/index.pkl")
            print("Download complete")
        except Exception as e:
            print(f"Error downloading from S3: {e}")
            raise e
    else:
        print("Vector DB found in Lambda cache.")

    return FAISS.load_local(local_path, embeddings, allow_dangerous_deserialization=True)

#Langgraph flow
class AgentState(TypedDict):
    question: str
    context: str
    answer: str
    grading: str

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# Initialize Vector Store 
vector_store = load_vector_store()

#Defining nodes
def retrieval_node(state: AgentState):
    print(f"Searching for: {state['question']}")
    docs = vector_store.similarity_search(state["question"], k=3)
    context_text = "\n\n".join([d.page_content for d in docs])
    print(f"Found {len(docs)} documents.")
    return {"context": context_text}

def grading_node(state: AgentState):
    print("Grading relevance")
    
    prompt = f"""
    You are a strict grader.
    Question: {state['question']}
    <context>{state['context']}</context>
    
    Does the text inside <context> tags contain info relevant to the question?
    Reply ONLY with 'yes' or 'no'.
    """
    
    response = llm.invoke(prompt).content.strip().lower()
    print(f"Grader: '{response}'")
    
    return {"grading": "relevant" if "yes" in response else "not_relevant"}

def generation_node(state: AgentState):
    print("Generating answer")
    
    prompt = f"""
    You are a DevOps Engineer. Answer ONLY using the context below.
    
    <context>{state['context']}</context>
    
    Question: {state['question']}
    """
    
    response = llm.invoke(prompt)
    return {"answer": response.content}

#Adding nodes
workflow = StateGraph(AgentState)

workflow.add_node("retrieve", retrieval_node)
workflow.add_node("grade", grading_node)
workflow.add_node("generate", generation_node)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "grade")

#This is a special function which will handle the conditional logic and will only pass flow if docs generate are relevant to the query
def decide_next_step(state: AgentState):
    if state["grading"] == "relevant":
        return "generate"
    print("Irrelevant docs. Ending.")
    return END

workflow.add_conditional_edges(
    "grade", 
    decide_next_step, 
    {"generate": "generate", END: END}
)

workflow.add_edge("generate", END)
app = workflow.compile()