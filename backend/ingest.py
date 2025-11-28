import os
import boto3
import time
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter

s3 = boto3.client('s3')
BUCKET_NAME = os.environ.get("BUCKET_NAME")

#This function is required as lambda function searches for this function to execute
def lambda_handler(event, context):
    print(f"Starting Ingestion for bucket: {BUCKET_NAME}")

    download_path = "/tmp/raw_data.txt"
    index_path = "/tmp/faiss_index"

    try:
        print("Downloading raw data from S3")
        s3.download_file(BUCKET_NAME, "raw/dataset.txt", download_path)
    except Exception as e:
        return {"statusCode": 500, "body": f"Error downloading raw data: {str(e)}"}
    
    print("Processing text...")
    loader = TextLoader(download_path, encoding='utf-8')
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    print(f"💎 Generating embeddings for {len(docs)} chunks...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

    # Rate Limit 
    db = FAISS.from_documents([docs[0]], embeddings)
    for i, doc in enumerate(docs[1:]):
        print(f"Processing chunk {i+2}/{len(docs)}")
        time.sleep(1)
        db.add_documents([doc])

    print("Saving index to /tmp")
    db.save_local(index_path)

    print("Uploading vectors back to S3")
    s3.upload_file(f"{index_path}/index.faiss", BUCKET_NAME, "vectors/index.faiss")
    s3.upload_file(f"{index_path}/index.pkl", BUCKET_NAME, "vectors/index.pkl")

    print("Ingestion Completed")
    return {"statusCode": 200, "body": "Knowledge base has been updated."}