from fastapi import FastAPI, File, UploadFile, HTTPException, Form, requests
import os
from tempfile import NamedTemporaryFile
from typing import List
from pydantic import BaseModel
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter


from fastapi import APIRouter
file_router = APIRouter(prefix="/api/file", tags=["文件上传"])
from common.config import BusinessException

class FileUrl(BaseModel):
    file_url: str

@file_router.post("/uploadfile/", summary="上传文件")
async def create_upload_file(file_url: str = Form(...)):
    try:
        # 从URL下载文件
        response = requests.get(file_url)
        if response.status_code == 200:
            file_suffix = os.path.splitext(file_url)[-1]
            with NamedTemporaryFile(delete=False, suffix=file_suffix) as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name

            # 后续处理逻辑
            loader = TextLoader(temp_file_path)
            raw_document = loader.load()
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
            documents = text_splitter.split_documents(raw_document)
            db = Chroma.from_documents(documents, OpenAIEmbeddings())
            query = "古元是谁"
            docs = db.similarity_search(query)
            print(docs[0].page_content)
        else:
            raise HTTPException(status_code=400, detail="Failed to download file from URL")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    return {"status": "success"}

    # Use LangChain to process the documents and store in vector database
   

    # Store the vector store (you might want to save this to disk or a database)
    # For this example, we'll just return the number of documents processed
   

def process_with_langchain(documents: list) -> list:
    # Placeholder for LangChain processing
    # Replace this with actual LangChain processing logic
    return documents