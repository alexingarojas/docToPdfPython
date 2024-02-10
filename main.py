from fastapi import FastAPI, UploadFile, File, Response, status
from fastapi.responses import FileResponse
from docx2pdf import convert
import os
import pypandoc

app = FastAPI()

# http://127.0.0.1:8000/

@app.get("/")
def index():
    return {"message" : "hola mundoss"}  

@app.get("/ipId/{text}")
def convertToPdf(text: int):
    return {"id" : text}

@app.post("/convertToPdf")
async def create_upload_file(file: UploadFile = File(...))-> FileResponse:
    path_main = "./documentos"
    contents = await file.read()
    file_path = os.path.join(path_main, file.filename)
    with open(file_path, 'wb') as f:
        f.write(contents)
    doc_path = os.path.join(path_main, file.filename)
    pdf_path = os.path.join(path_main, file.filename.replace(".docx", ".pdf"))
    try:
        convert(doc_path, pdf_path)
    except AttributeError:
        pass  
    response = FileResponse(pdf_path)
    response.headers["Content-Disposition"] = f"attachment; filename={os.path.basename(pdf_path)}"
    return response

@app.post("/convertToPdf/v2")
async def create_upload_file_new(file: UploadFile = File(...))-> FileResponse:
    path_main = "./documentos"
    contents = await file.read()
    file_path = os.path.join(path_main, file.filename)
    with open(file_path, 'wb') as f:
        f.write(contents)
    doc_path = os.path.join(path_main, file.filename)
    pdf_path = os.path.join(path_main, file.filename.replace(".docx", ".pdf"))
    
    output = pypandoc.convert_file(doc_path, 'pdf', outputfile=pdf_path)
    assert output == "" 
    
    response = FileResponse(pdf_path)
    response.headers["Content-Disposition"] = f"attachment; filename={os.path.basename(pdf_path)}"
    return response

