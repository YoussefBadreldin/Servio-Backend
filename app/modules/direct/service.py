import json
import os
import xml.etree.ElementTree as ET
from typing import List, Dict
import nltk
from nltk.corpus import wordnet as wn
import uuid
from pathlib import Path
from ...shared.exceptions import DirectModuleError

nltk.download('wordnet', quiet=True, force=True)
nltk.download('omw-1.4', quiet=True, force=True)
nltk.download('punkt', quiet=True, force=True)

class DirectService:
    def __init__(self):
        self.registry_path = "data/servio_data.jsonl"
        self.xml_storage_path = "data/xml_aspects"
        os.makedirs(self.xml_storage_path, exist_ok=True)
        
    def preprocess_text(self, text: str) -> str:
        return " ".join(text.lower().split())

    def enhanced_similarity(self, aspect: str, field_value: str) -> float:
        aspect_proc = self.preprocess_text(aspect)
        field_proc = self.preprocess_text(field_value)
        if aspect_proc in field_proc:
            return 1.0
        synsets_aspect = wn.synsets(aspect_proc)
        synsets_field = wn.synsets(field_proc)
        max_sim = 0.0
        if not synsets_aspect or not synsets_field:
            return max_sim
        for syn1 in synsets_aspect:
            for syn2 in synsets_field:
                sim = syn1.wup_similarity(syn2) or 0.0
                if sim > max_sim:
                    max_sim = sim
        return max_sim

    def load_registry(self) -> List[Dict]:
        try:
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                return [json.loads(line) for line in f if line.strip()]
        except Exception as e:
            raise DirectModuleError(f"Failed to load registry: {str(e)}")

    def parse_xml(self, xml_file: str) -> Dict[str, str]:
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            aspects = {}
            for aspect in root.findall("Aspect"):
                key_elem = aspect.find("Key")
                value_elem = aspect.find("Value")
                if key_elem is not None and value_elem is not None:
                    key = key_elem.text.strip()
                    value = value_elem.text.strip() if value_elem.text else ""
                    aspects[key] = value
            return aspects
        except Exception as e:
            raise DirectModuleError(f"XML parsing failed: {str(e)}")

    def generate_xml(self, aspects: List[Dict[str, str]]) -> str:
        try:
            xml_id = str(uuid.uuid4())
            xml_path = os.path.join(self.xml_storage_path, f"{xml_id}.xml")
            
            root = ET.Element("Aspects")
            for aspect in aspects:
                aspect_elem = ET.SubElement(root, "Aspect")
                key_elem = ET.SubElement(aspect_elem, "Key")
                key_elem.text = aspect["key"]
                value_elem = ET.SubElement(aspect_elem, "Value")
                value_elem.text = aspect["value"]
            
            tree = ET.ElementTree(root)
            tree.write(xml_path, encoding="utf-8", xml_declaration=True)
            return xml_path
        except Exception as e:
            raise DirectModuleError(f"XML generation failed: {str(e)}")

    def suggest_aspects(self) -> List[str]:
        return ["repo", "path", "func_name", "original_string", "docstring",
                "code", "code_tokens", "docstring_tokens", "url", "language", "partition"]

    def match_services(self, query: str, aspects: Dict[str, str], top_n: int = 5) -> List[Dict]:
        try:
            registry = self.load_registry()
            min_threshold = 0.3
            required_matches = 1
            scored_entries = []

            for entry in registry:
                total_score = 0.0
                matched_aspects = 0
                for aspect_key, aspect_value in aspects.items():
                    if aspect_key in entry:
                        sim = self.enhanced_similarity(aspect_value, entry[aspect_key])
                        if sim >= min_threshold:
                            total_score += sim
                            matched_aspects += 1
                if matched_aspects >= required_matches:
                    scored_entries.append((total_score, entry))

            scored_entries.sort(key=lambda x: x[0], reverse=True)
            return [{"similarity_score": score, **entry} for score, entry in scored_entries[:top_n]]
        except Exception as e:
            raise DirectModuleError(f"Service matching failed: {str(e)}")