from openai import OpenAI
import os, json
import markdown2
import pymupdf
from PIL import Image
from itertools import repeat
from concurrent.futures import ProcessPoolExecutor

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent 

from django.conf import settings

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_GEN_API_KEY"))

client = OpenAI(api_key=os.getenv('openai'))


def gpt_response(messages, json=False, temperature=1):
    # print(messages)
    response = client.chat.completions.create(
    response_format={ "type": "json_object" } if json else {"type": "text"}, #"json_schema", "json_schema": {'choice': 'the best option from the given choices' } } if json else {},
    temperature = temperature,
    model="gpt-4o-mini",
    messages=messages
    )

    return response.choices[0].message.content
    

def summarize(article, messages):
    
    messages.append({'role': 'user', 'content': f'''Please summarize the following document:
{article}

Instruction:
- Please convey maximum information from the content above  effectively.
- Do not include chat text in your response.'''})

    return(gpt_response(messages, False))

def keytakeaways(article, messages):
    messages.append({'role': 'user', 'content': f'''Please extract the key takeaways from the given document:
{article}

Instruction:
- Please convey maximum information from the content above  effectively.
- Do not include chat text in your response.'''})
    
    return gpt_response(messages, False)

def fluidate(content, messages, choice):

    content = "\n\n\n".join(content)
    if choice == 0:
        messages.append({'role': 'user', 'content': f'''Please cohere these summaries generated from each pages of single document:
{content}

Instruction:
- Please convey maximum information effectively.
- Please do not generalize what is said in the given summaries, rather try to convey the exact content in each summaries.
- Make the final output easily readable by using markdown formating (If headings are used, only use Headings other than h1 (# elements) in the markdown response).
- Never give an introductory title like "Summary"(in fact a General Title for the whole content is unnecessary, but use headings to emphasize subjects if possible).
- Do not include chat text in your response.'''})
    else:
        messages.append({'role': 'user', 'content': f'''Please cohere these key points generated from each pages of single document:
{content}

Instruction:
- Please convey maximum information effectively.
- Please do not generalize what is said in the given key points, rather try to convey the exact content in each key points.
- Make the final output easily readable by using markdown formating (If headings are used, only use Headings other than h1 (# elements) in the markdown response).
- Never give an introductory title like "Key Points"(in fact a General Title for the whole content is unnecessary, but use headings to emphasize subjects if possible).
- Do not include chat text in your response.'''})

    return gpt_response(messages, False)



def sk_wrapper(choice, fc):

    messages = [
        {'role': 'system', 'content': '''You are a Big law Lawyer practicing in India. You are very intelligent.'''}]

    if choice == 0:
        with ProcessPoolExecutor() as executor:
            output = list(executor.map(summarize, fc, repeat(messages)))
    else:
        with ProcessPoolExecutor() as executor:
            output = list(executor.map(keytakeaways, fc, repeat(messages)))

    if output:
        content = fluidate(output, messages, choice)
    
    return content


def convert_markdown_to_html(markdown_text):
    html = markdown2.markdown(markdown_text)
    return html


def extract_text_from_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)
    zoom_x = 2.0
    zoom_y = 2.0
    mat = pymupdf.Matrix(zoom_x, zoom_y)
    doc_pics = []
    pdf_path = pdf_path.replace('\\', '/')
    print(pdf_path)
    bfp = os.path.join(settings.MEDIA_ROOT, f'file_images/{pdf_path.split("/")[-1].replace(".pdf", "")}').replace("\\", "/")
    print(bfp)
    if not os.path.isdir(bfp):
        os.mkdir(bfp)
    for page in doc:
        pix = page.get_pixmap(matrix=mat)
        fp = os.path.join(bfp, f"page-{page.number}.png")
        pix.save(fp)
        doc_pics.append(fp)
    # for path in doc_pics:
    #     ocr_text = ocr_gen_ai(Image.open(path))
    with ProcessPoolExecutor() as executor:
        doc_texts = list(executor.map(ocr_gen_ai, doc_pics))

    ocr_content = "\n".join(doc_texts)

    with open(f'{BASE_DIR}/skapp/ocr_text/{pdf_path.split("/")[-1].replace(".pdf", "")}.txt', "w", encoding="UTF-8") as oc:
        oc.write(ocr_content)

    return doc_texts

def ocr_gen_ai(path):
    # Choose a Gemini model.
    img = Image.open(path)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    prompt = """Extract text from the following image. Retain things in the image as their equivalent markdown in your response. Do not add any additional content to the content in the image (especially chatty texts)"""

    response = model.generate_content([prompt, "\n\n", img])

    return response.text
