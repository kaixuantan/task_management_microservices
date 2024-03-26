from pypdf import PdfReader
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY=os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
print(GOOGLE_API_KEY)

reader = PdfReader("/Users/tankaixuan/Library/Mobile Documents/com~apple~CloudDocs/Y2S2/ESD/Project/esd-github/WrapperMicroservices/GeminiWrapper/Project Requirements (Final).pdf")
number_of_pages = len(reader.pages)
text = ''.join([page.extract_text() for page in reader.pages])
print(text[:2155])

model = genai.GenerativeModel('gemini-pro')

prompt = f"""Here is an project requirement document: <paper>{text}</paper>

Please do the following:
1. Summarize the document and give the key requirements.
2. Generate a few ideas that fulfill the requirements for the project.
"""

start_time = time.time()
response = model.generate_content(prompt)
end_time = time.time()
elapsed_time = end_time - start_time

# Open a file in write mode ('w') and write the response text to it
with open('gemini_response.md', 'w') as file:
    file.write(f"{response.text}")

print(f"Time taken: {elapsed_time} seconds")