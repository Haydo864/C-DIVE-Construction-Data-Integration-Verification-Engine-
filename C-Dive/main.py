from fastapi import UploadFile, File
import PyPDF2
import io
import os
import instructor
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models import ConstructionInvoice


app = FastAPI(title="C-DIVE API (Gemini Edition)")

# BULLETPROOF CORS SETUP
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. CONFIGURE GEMINI
REAL_API_KEY = "API KEY HERE"
genai.configure(api_key=REAL_API_KEY)

# 2. PATCH GEMINI WITH INSTRUCTOR
# We use gemini-1.5-pro because it is exceptional at complex data extraction
client = instructor.from_gemini(
    client=genai.GenerativeModel(model_name="gemini-2.5-flash"),
    mode=instructor.Mode.GEMINI_JSON,
)



class InvoiceTextRequest(BaseModel):
    raw_text: str

@app.post("/api/upload-invoice")
async def upload_invoice(file: UploadFile = File(...)):
    try:
        # 1. Read the uploaded PDF file into memory
        file_content = await file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        
        # 2. Extract all the text from the PDF pages
        extracted_text = ""
        for page in pdf_reader.pages:
            extracted_text += page.extract_text() + "\n"
            
        # 3. Pass the extracted text directly to your existing Gemini AI logic
        extracted_invoice = client.chat.completions.create(
            response_model=ConstructionInvoice,
            messages=[
                {"role": "user", "content": f"You are a precise multifamily real estate data extractor. Extract data from this raw invoice text:\n\n{extracted_text}"}
            ]
        )

        # 4. Run your exact same Fail-Safe math check
        calculated_total = sum(item.amount for item in extracted_invoice.line_items)
        math_variance = round(abs(extracted_invoice.total_amount - calculated_total), 2)
        
        status = "Green"
        flags = []
        
        if math_variance > 0:
            status = "Red"
            flags.append(f"Math Error: Line items sum to ${calculated_total}, but total is ${extracted_invoice.total_amount}.")

        return {
            "status": status,
            "flags": flags,
            "data": extracted_invoice.model_dump(),
            "extracted_text_preview": extracted_text[:200] # Send a preview back to the frontend
        }

    except Exception as e:
        print(f"\n❌ FILE UPLOAD ERROR: {str(e)}\n")
        raise HTTPException(status_code=500, detail=str(e))


    except Exception as e:
        print(f"\n❌ EXTREMELY HELPFUL ERROR MESSAGE: {str(e)}\n")
        raise HTTPException(status_code=500, detail=str(e))