from fastapi import FastAPI, UploadFile, File
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


UPLOAD_DIR = Path("backend/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Tax AI Backend is running"
    }


# =========================================================
# DOCUMENT UPLOAD
# =========================================================

@app.post("/upload")
async def upload_documents(

    pan: UploadFile | None = File(None),

    aadhaar: list[UploadFile] = File(default=[]),

    salary: list[UploadFile] = File(default=[]),

    bank: list[UploadFile] = File(default=[]),

    form16: list[UploadFile] = File(default=[]),
):

    uploaded_files = {}


    files = {

        "pan": [pan] if pan else [],

        "aadhaar": aadhaar,

        "salary": salary,

        "bank": bank,

        "form16": form16,
    }


    # =====================================================
    # SAVE FILES
    # =====================================================

    for document_type, document_files in files.items():

        uploaded_files[document_type] = []


        for file in document_files:

            if file is None:
                continue


            file_path = UPLOAD_DIR / file.filename


            content = await file.read()


            with open(file_path, "wb") as output_file:

                output_file.write(content)


            uploaded_files[document_type].append({

                "filename": file.filename,

                "path": str(file_path),

            })


    return {

        "message": "Documents uploaded successfully",

        "files": uploaded_files,

    }