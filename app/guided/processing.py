import json
import xml.etree.ElementTree as ET
from langchain.docstore.document import Document
from typing import List, Union
from PIL import Image
import pytesseract

def process_jsonl(file_path: str) -> List[Document]:
    """Process JSONL files into LangChain Documents"""
    documents = []
    with open(file_path, "r") as f:
        for line in f:
            data = json.loads(line)
            content = (
                f"Service Name: {data.get('func_name', 'N/A')}\n"
                f"Description: {data.get('docstring', 'No description')}\n"
                f"Tags: {', '.join(data.get('repo', []))}\n"
                f"URL: {data.get('url', 'N/A')}"
            )
            documents.append(Document(page_content=content, metadata=data))
    return documents

def process_xml(file_path: str) -> List[Document]:
    """Process XML files into LangChain Documents"""
    tree = ET.parse(file_path)
    root = tree.getroot()
    documents = []
    
    for record in root.findall('.//record'):
        service_name = record.find('func_name').text if record.find('func_name') is not None else 'N/A'
        description = record.find('docstring').text if record.find('docstring') is not None else 'No description'
        tags = [tag.text for tag in record.findall('repo/tag')] if record.find('repo') is not None else []
        url = record.find('url').text if record.find('url') is not None else 'N/A'
        
        content = (
            f"Service Name: {service_name}\n"
            f"Description: {description}\n"
            f"Tags: {', '.join(tags)}\n"
            f"URL: {url}"
        )
        metadata = {"service_name": service_name, "description": description, "tags": tags, "url": url}
        documents.append(Document(page_content=content, metadata=metadata))
    
    return documents

def process_uml(image_path: str) -> str:
    """Extract text from UML diagram and generate PlantUML"""
    img = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(img)
    
    prompt = (
        "Convert this UML diagram text into PlantUML code:\n\n"
        f"{extracted_text}\n\n"
        "Focus on extracting service descriptions and relationships."
    )
    return prompt  # Will be processed by query.py