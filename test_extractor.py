from backend.document_reader import read_document
from backend.llm_extractor import extract_salary_data


file_path = "backend/uploads/salary.png"


print("\n========== STEP 1: OCR ==========\n")

ocr_text = read_document(file_path)

print(ocr_text)


print("\n========== STEP 2: LLM EXTRACTION ==========\n")

result = extract_salary_data(ocr_text)

print(result)


print("\n=============================================\n")