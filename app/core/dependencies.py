import json
import os
import zipfile
import xml.etree.ElementTree as ET
from typing import List, Dict, Tuple, Optional
import nltk
from nltk.corpus import wordnet as wn
from pathlib import Path

from .exceptions import AspectDefinition, ServiceMatch, AspectMatchResult, OverallMatchResult

class DirectParallel:
    def __init__(self):
        """Initialize the DIRECT parallel service with NLTK resources."""
        nltk.download('wordnet', quiet=True, force=True)
        nltk.download('omw-1.4', quiet=True, force=True)
        nltk.download('punkt', quiet=True, force=True)
        nltk.data.path.append('/usr/local/share/nltk_data')

    def extract_zip(self, zip_file_path: str, extract_path: str) -> str:
        """Extracts the contents of a ZIP file to a given directory."""
        if not os.path.exists(extract_path):
            os.makedirs(extract_path)
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        return extract_path

    @staticmethod
    def preprocess_text(text: str) -> str:
        """Lowercases text and removes extra spaces."""
        return " ".join(text.lower().split())

    def enhanced_similarity(self, aspect: str, field_value: str) -> float:
        """
        Computes a similarity score between the aspect and a field value.
        If the aspect string is found as a substring (ignoring case) in the field value,
        returns 1.0. Otherwise, falls back to WordNet-based semantic similarity.
        """
        aspect_proc = self.preprocess_text(aspect)
        field_proc = self.preprocess_text(field_value)
        
        # Check for substring match:
        if aspect_proc in field_proc:
            return 1.0
        
        # Otherwise, compute WordNet-based similarity
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

    def load_registry(self, file_path: str) -> List[Dict]:
        """
        Loads the service registry from a JSONL (NDJSON) file.
        Each line in the file should be a valid JSON object.
        """
        data = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            raise FileNotFoundError(f"Registry file not found: {file_path}")
        return data

    def parse_xml(self, xml_file: str) -> Dict[str, str]:
        """
        Parses an XML file to extract user-defined aspects.
        The XML should have a structure where each Aspect element contains a Key and a Value.
        """
        aspects = {}
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for aspect in root.findall("Aspect"):
                key_elem = aspect.find("Key")
                value_elem = aspect.find("Value")
                if key_elem is not None and value_elem is not None:
                    key = key_elem.text.strip()
                    value = value_elem.text.strip() if value_elem.text else ""
                    aspects[key] = value
        except ET.ParseError as e:
            raise ValueError(f"Error parsing XML: {e}")
        return aspects

    def generate_xml(self, aspects: List[AspectDefinition], output_path: str) -> str:
        """
        Generates an XML file from aspect definitions.
        """
        root = ET.Element("Aspects")
        for aspect in aspects:
            aspect_elem = ET.SubElement(root, "Aspect")
            ET.SubElement(aspect_elem, "Key").text = aspect.key
            ET.SubElement(aspect_elem, "Value").text = aspect.value
        
        tree = ET.ElementTree(root)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)
        return output_path

    def match_services(
        self,
        query: str,
        registry: List[Dict],
        aspects: Dict[str, str],
        top_n: int = 5,
        min_threshold: float = 0.3,
        required_matches: int = 1
    ) -> OverallMatchResult:
        """
        Computes overall matching scores for registry entries.
        Returns an OverallMatchResult containing the top matches.
        """
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
                scored_entries.append((
                    total_score,
                    ServiceMatch(
                        func_name=entry.get("func_name", "Unknown"),
                        repo=entry.get("repo", "Unknown"),
                        path=entry.get("path", "Unknown"),
                        docstring=entry.get("docstring", "No docstring available"),
                        url=entry.get("url", "Unknown"),
                        score=total_score
                    )
                ))

        scored_entries.sort(key=lambda x: x[0], reverse=True)
        matches = [entry for score, entry in scored_entries[:top_n]]
        
        return OverallMatchResult(
            query=query,
            matches=matches,
            aspects_used=list(aspects.keys()),
            min_threshold=min_threshold
        )

    def match_services_per_aspect(
        self,
        registry: List[Dict],
        aspect_key: str,
        aspect_value: str,
        top_n: int = 3,
        min_threshold: float = 0.3
    ) -> AspectMatchResult:
        """
        Computes matching scores for a single aspect.
        Returns an AspectMatchResult containing the top matches for the aspect.
        """
        scored_entries = []

        for entry in registry:
            if aspect_key in entry:
                sim = self.enhanced_similarity(aspect_value, entry[aspect_key])
                if sim >= min_threshold:
                    scored_entries.append((
                        sim,
                        ServiceMatch(
                            func_name=entry.get("func_name", "Unknown"),
                            repo=entry.get("repo", "Unknown"),
                            path=entry.get("path", "Unknown"),
                            docstring=entry.get("docstring", "No docstring available"),
                            url=entry.get("url", "Unknown"),
                            score=sim
                        )
                    ))

        scored_entries.sort(key=lambda x: x[0], reverse=True)
        matches = [entry for sim, entry in scored_entries[:top_n]]
        
        return AspectMatchResult(
            aspect_key=aspect_key,
            aspect_value=aspect_value,
            matches=matches,
            min_threshold=min_threshold
        )

    def suggest_missing_aspects(self, existing_aspects: Dict[str, str]) -> List[str]:
        """
        Suggests additional aspect keys from a predefined set.
        """
        all_aspects = {
            "repo", "path", "func_name", "original_string", "docstring",
            "code", "code_tokens", "docstring_tokens", "url", "language", "partition"
        }
        return list(all_aspects - set(existing_aspects.keys()))