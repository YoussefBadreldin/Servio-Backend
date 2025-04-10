import os
import json
import zipfile
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
import nltk
from nltk.corpus import wordnet as wn
from ...shared.exceptions import DirectMatchError
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Tuple
from .models import DiscoveryMode
from datetime import datetime

class DirectService:
    def __init__(self):
        self.initialize_nltk()
        self.registry = self.load_registry()

    def initialize_nltk(self):
        """Initialize NLTK resources"""
        try:
            nltk.download('wordnet', quiet=True, force=True)
            nltk.download('omw-1.4', quiet=True, force=True)
            nltk.download('punkt', quiet=True, force=True)
            nltk.data.path.append('/usr/local/share/nltk_data')
        except Exception as e:
            raise DirectMatchError(f"NLTK initialization failed: {str(e)}")

    def load_registry(self) -> List[Dict]:
        """Load the service registry from JSONL file"""
        registry_file = "data/servio_data.jsonl"
        try:
            with open(registry_file, 'r', encoding='utf-8') as f:
                return [json.loads(line) for line in f if line.strip()]
        except Exception as e:
            raise DirectMatchError(f"Failed to load registry: {str(e)}")

    @staticmethod
    def preprocess_text(text: str) -> str:
        """Lowercases text and removes extra spaces"""
        return " ".join(text.lower().split())

    def enhanced_similarity(self, aspect: str, field_value: str) -> float:
        """Compute similarity between aspect and field value"""
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

    def generate_xml(self, aspects: List[Dict[str, str]]) -> str:
        """Generate XML string from aspects and store in data folder"""
        root = ET.Element("Aspects")
        for aspect in aspects:
            aspect_elem = ET.SubElement(root, "Aspect")
            ET.SubElement(aspect_elem, "Key").text = aspect['key']
            ET.SubElement(aspect_elem, "Value").text = aspect['value']
        
        xml_str = ET.tostring(root, encoding='unicode')
        
        # Store XML in data folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"aspects_{timestamp}.xml"
        os.makedirs("data/xml_aspects", exist_ok=True)
        with open(f"data/xml_aspects/{filename}", "w") as f:
            f.write(xml_str)
            
        return xml_str

    def get_latest_xml(self) -> Optional[str]:
        """Get the most recently generated XML file"""
        xml_dir = "data/xml_aspects"
        if not os.path.exists(xml_dir):
            return None
            
        xml_files = [f for f in os.listdir(xml_dir) if f.endswith(".xml")]
        if not xml_files:
            return None
            
        latest_file = max(xml_files, key=lambda f: os.path.getmtime(f"{xml_dir}/{f}"))
        with open(f"{xml_dir}/{latest_file}", "r") as f:
            return f.read()

    def discover_services(
        self,
        query: str,
        aspects: List[Dict[str, str]],
        mode: DiscoveryMode = DiscoveryMode.PARALLEL,
        top_n: int = 5
    ) -> Tuple[List[Dict], float]:
        """Perform service discovery with timing"""
        start_time = time.time()
        
        if mode == DiscoveryMode.PARALLEL:
            matches = self._match_parallel(query, aspects, top_n)
        else:
            matches = self._match_sequential(query, aspects, top_n)
            
        exec_time = (time.time() - start_time) * 1000  # ms
        return matches, exec_time

    def _match_parallel(self, query: str, aspects: List[Dict[str, str]], top_n: int) -> List[Dict]:
        """Match services using all aspects in parallel"""
        with ThreadPoolExecutor() as executor:
            # Process each aspect in parallel
            future_matches = [
                executor.submit(self._match_per_aspect, aspect['key'], aspect['value'], top_n)
                for aspect in aspects
            ]
            
            # Combine results from all aspects
            aspect_results = [future.result() for future in future_matches]
            
        # Aggregate and rank matches
        all_matches = {}
        for aspect_key, matches in zip([a['key'] for a in aspects], aspect_results):
            for match in matches:
                service_id = match['func_name']
                if service_id not in all_matches:
                    all_matches[service_id] = match
                    all_matches[service_id]['matched_aspects'] = []
                all_matches[service_id]['matched_aspects'].append