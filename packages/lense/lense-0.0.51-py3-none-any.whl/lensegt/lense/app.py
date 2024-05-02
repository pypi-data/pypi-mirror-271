#from loader import load_document
from lensegt.my_backend.qna_engine import *
from lensegt.my_backend.SQL_engine import *
from lensegt.my_backend.csv_engine import *
from fastapi import FastAPI, File, UploadFile, Form
from enum import Enum
from lensegt.my_backend.qna_engine import embed_and_run_openai, embed_and_run_azureopenai, embed_and_run_mistral, embed_and_run_model
import shutil
import os
from lensegt.my_backend.loader import load_document, load_directory
from fastapi import FastAPI, Request ,APIRouter
from fastapi.staticfiles import StaticFiles 
from fastapi.templating import Jinja2Templates
import uvicorn
import warnings
from typing import List
warnings.filterwarnings('ignore')
from lensegt import lense

app = FastAPI()

# Define an Enum for engine selection
class EngineType(str, Enum):
    OPENAI = "OpenAI"
    AZURE_OPENAI = "Azure OpenAI"
    HuggingFace = "HuggingFace"

class MistralModel(str, Enum):
    MIXTRAL = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    MISTRAL = "mistralai/Mistral-7B-Instruct-v0.2"
    GEMMA = "google/gemma-7b"
    PHI = "microsoft/Phi-3-mini-4k-instruct"
    TINYLLAMA = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    STABLELM = "stabilityai/stablelm-2-zephyr-1_6b"
    H2O = "h2oai/h2o-danube2-1.8b-chat"
class EngineType1(str, Enum):
    OPENAI = "OpenAI"
    AZURE_OPENAI = "Azure OpenAI"

# List to store engines
engines = []

# Temporary directory to store uploaded files
temporary_folder = "temp_uploaded_files"

# Ensure the temporary folder exists
os.makedirs(temporary_folder, exist_ok=True)


@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    try:
        # Iterate over each uploaded file
        for file in files:
            # Save the uploaded file to the temporary directory
            save_path = os.path.join(temporary_folder, file.filename)
            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        
        return {"result": "Files uploaded to temporary folder successfully", "folder_path": temporary_folder}
    
    except Exception as e:
        return {"error": str(e)}

@app.post("/process_documents/")
async def process_documents(
    engine_type: EngineType,
    selected_model: MistralModel = None,
    api_key: str = Form(None),
    api_version: str = Form(None),
    azure_endpoint: str = Form(None),
    hf_token: str = Form(None)
):
    global temporary_folder
    try:
        # Check if any file has been uploaded
        if not temporary_folder:
            return {"error": "No files uploaded"}

        # Load documents from the uploaded files
        documents = []
        documents.extend(load_directory(temporary_folder))
        
        # Select and run the appropriate engine based on user input
        if engine_type == EngineType.OPENAI:
            if api_key is None:
                return {"error": "api_key is required for OpenAI"}
            engine = embed_and_run_openai(
                documents=documents,
                api_key=api_key
            )
        elif engine_type == EngineType.AZURE_OPENAI:
            if any(arg is None for arg in [api_key, api_version, azure_endpoint]):
                return {"error": "api_key, api_version, and azure_endpoint are required for Azure OpenAI"}
            engine = embed_and_run_azureopenai(
                documents=documents,
                api_key=api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint
            )
        elif engine_type == EngineType.HuggingFace:
            if hf_token is None or selected_model is None:
                return {"error": "hf_token and selected_model are required for Mistral"}
            engine = embed_and_run_model(
                documents=documents,
                hf_token=hf_token,
                model=selected_model
            )
        else:
            return {"error": "Invalid engine type"}
        
        # Store the engine in the list
        engines.append(engine)
        
        # Clean up: Remove the temporary files
        # if os.path.exists('temp_uploaded_files'):
        #     shutil.rmtree('temp_uploaded_files')
        #     print("Temporary folder removed")

        if os.path.exists('temp_uploaded_files'):
            for filename in os.listdir('temp_uploaded_files'):
                file_path = os.path.join('temp_uploaded_files', filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")
            print("Temporary files removed")
        
        return {"result": "Engine created and stored successfully"}
    
    except Exception as e:
        return {"error": str(e)}



    
@app.post("/use-engine_document/")
async def use_engine(
    query: str = Form(...)
):
    try:
        # Check if any engine has been stored
        if not engines:
            return {"error": "No engine available"}
        
        # Use the latest stored engine to run the query
        engine = engines[-1]
        result = engine(query)
        response = str(result)
        pattern = r'Answer:\s*(.*)'
        matches = re.findall(pattern, response, re.DOTALL)
        answer = ""
        if matches:
            for match in matches:
                print(match)
                answer+=match
        else:
            answer += response

        return {"result": answer}
    
    except Exception as e:
        return {"error": str(e)}
    
# Endpoint to select the engine type and process the uploaded file
@app.post("/process_csv/")
async def process_document(
    engine_type: EngineType1,
    api_key: str = Form(None),
    api_version: str = Form(None),
    azure_endpoint: str = Form(None)
):
    global temporary_folder
    try:

        if os.path.isdir(temporary_folder):
            files = os.listdir(temporary_folder)

            # Check if there is exactly one file in the folder
            if len(files) == 1:
                file_path = os.path.join(temporary_folder, files[0])
                documents = load_document(file_path)
            else:
                return {"error": "Temporary folder should contain exactly one CSV file"}
        else:
            return {"error": "Temporary folder not found"}
        
        # Select and run the appropriate engine based on user input
        if engine_type == EngineType1.OPENAI:
            if api_key is None:
                return {"error": "api_key is required for OpenAI"}
            engine = csv_engine_openai(
                df=documents,
                api_key=api_key
            )
        elif engine_type == EngineType1.AZURE_OPENAI:
            if any(arg is None for arg in [api_key, api_version, azure_endpoint]):
                return {"error": "api_key, api_version, and azure_endpoint are required for Azure OpenAI"}
            engine = csv_engine_azure(
                df=documents,
                api_key=api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint
            )
        else:
            return {"error": "Invalid engine type"}
        
        # Store the engine in the list
        engines.append(engine)
        
        if os.path.exists('temp_uploaded_files'):
            for filename in os.listdir('temp_uploaded_files'):
                file_path = os.path.join('temp_uploaded_files', filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")
            print("Temporary files removed")
        
        return {"result": "Engine created and stored successfully"}
    
    except Exception as e:
        return {"error": str(e)}

    
@app.post("/use-engine_csv/")
def use_engine(
    query: str = Form(...)
):
    try:
        # Check if any engine has been stored
        if not engines:
            return {"error": "No engine available"}
        
        # Use the latest stored engine to run the query
        engine = engines[-1]
        result = engine(query_str=query)
        result = result.message.content

        return {"result": result}
    
    except Exception as e:
        return {"error": str(e)}
class EngineType2(str, Enum):
    OPENAI = "OpenAI"
    AZURE_OPENAI = "Azure OpenAI"
    GOOGLE_GENAI = "Google GenAI"


# Endpoint to create an engine based on the selected parameters
@app.post("/process_SQl_URL/")
async def process_document(
    db_url: str = Form(...),
    engine_type: EngineType2 = Form(...),
    api_key: str = Form(None),
    api_version: str = Form(None),
    azure_endpoint: str = Form(None),
    google_api_key: str = Form(None)
):
    try:

        # Select and run the appropriate engine based on user input
        if engine_type == EngineType1.OPENAI:
            if api_key is None:
                return {"error": "api_key is required for OpenAI"}
            engine = sql_engine_openai(db_url=db_url, api_key=api_key)
        elif engine_type == EngineType1.AZURE_OPENAI:
            if any(arg is None for arg in [api_key, api_version, azure_endpoint]):
                return {"error": "api_key, api_version, and azure_endpoint are required for Azure OpenAI"}
            engine = sql_engine_azure(db_url=db_url, api_key=api_key, api_version=api_version, azure_endpoint=azure_endpoint)
        elif engine_type == EngineType1.GOOGLE_GENAI:
            if google_api_key is None:
                return {"error": "google_api_key is required for Google GenAI"}
            engine = sql_engine_genai(db_url=db_url, api_key=google_api_key)
        else:
            return {"error": "Invalid engine type"}

        # Store the engine in the list
        engines.append(engine)
        
        return {"result": "Engine created and stored successfully"}
    
    except Exception as e:
        return {"error": str(e)}

# Another endpoint to use the stored engine
@app.post("/use-SQL-engine/")
async def use_engine(
    query: str = Form(...)
):
    try:
        # Check if any engine has been stored
        if not engines:
            return {"error": "No engine available"}
        
        # Use the latest stored engine to run the query
        engine = engines[-1]
        result = engine(query)
        return {"result": result}
    
    except Exception as e:
        return {"error": str(e)}
    

def start():
    print("-"*100)
    print("Inside the the start function")
    print("current path of directory",os.getcwd())
    file_path =  lense.__file__
    path = os.path.join(os.path.dirname(os.path.dirname(file_path)),"my_frontend")

    app.mount("/", StaticFiles(directory=path, html=True), name="my_frontend")

    # running in pip installer
    uvicorn.run("lense.app:app", reload=False, host="127.0.0.1", port=9017,workers=1)

    # running in local through demo.py
    # uvicorn.run("lensegt.lense.app:app", reload=False, host="127.0.0.1", port=9017,workers=1)