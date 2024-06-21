import os
import uuid
from tempfile import NamedTemporaryFile
from tkinter.tix import Form

import oss2
from fastapi import APIRouter, UploadFile, File, Depends
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader, PyPDFLoader, UnstructuredFileLoader

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from common.utils.ResponseRes import R
from models.knowledge import KnowledgeBase
from models.user import User
from router.user import get_login_user

knowledge_router = APIRouter(prefix="/api/knowledge", tags=["知识库管理"])



@knowledge_router .post("/upload", summary="新增数据库")
async def handle_file_upload(
    file: UploadFile = File(...),
    name: str = Form(),
    creator: str = Form(),
    description: str = Form(),
   # user: User = Depends(get_login_user)
):
    # 生成唯一文件名
    with NamedTemporaryFile(delete=False) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_filename = tmp.name
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension == ".txt":
        loader = TextLoader(tmp_filename)
    elif file_extension == ".pdf":
        loader =  PyPDFLoader(tmp_filename)

    else:
        # 如果是其他类型的文件,可以使用通用的 UnstructuredFileLoader
        loader = UnstructuredFileLoader(tmp_filename)

    # 使用选择的加载器加载文件
    documents = loader.load()
    # 使用 RecursiveCharacterTextSplitter 对文档进行分割
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    # 将文档及其嵌入存储到 ChromaDB
    persist_directory = "chroma_data"
    chroma_db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    chroma_db.add_documents(split_docs)

    # 存储文件元数据
    metadata = {
        "name": name,
        "creator": creator,
        "description": description,
       # "user": user.id
    }
    chroma_db.add_texts([doc.page_content for doc in split_docs], metadatas=[metadata] * len(split_docs))
    auth = oss2.Auth(aliyun_config["access-key-id"], aliyun_config["access-key-secret"])
    bucket = oss2.Bucket(auth, aliyun_config["end-point"], aliyun_config["bucket-name"])
    oss_file_name = os.path.basename(file.filename)
    bucket.put_object_from_file(oss_file_name, tmp_filename)
    oss_file_url = f"https://{aliyun_config['bucket-name']}.{aliyun_config['end-point']}/{oss_file_name}"

    os.remove(tmp_filename)
    unique_filename = f"{uuid.uuid4().hex}-{file.filename}"
    file_location = f"uploads/{unique_filename}"
    await KnowledgeBase.create(title = "name",description= description,OSSlink = oss_file_url,userID = 123)
    return R.ok("文件上传成功")
