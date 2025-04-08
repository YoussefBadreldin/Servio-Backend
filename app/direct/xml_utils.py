import xml.etree.ElementTree as ET
from typing import Dict, Optional

class AspectHandler:
    @staticmethod
    def parse_xml(xml_path: str) -> Dict[str, str]:
        """Parse aspects from XML file"""
        aspects = {}
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            for aspect in root.findall("Aspect"):
                key = aspect.find("Key").text.strip() if aspect.find("Key") is not None else None
                value = aspect.find("Value").text.strip() if aspect.find("Value") is not None else None
                
                if key and value:
                    aspects[key] = value
                    
        except Exception as e:
            print(f"XML parsing error: {e}")
            
        return aspects

    @staticmethod
    def generate_xml(aspects: Dict[str, str], output_path: str):
        """Generate XML from aspects dictionary"""
        root = ET.Element("Aspects")
        
        for key, value in aspects.items():
            aspect = ET.SubElement(root, "Aspect")
            ET.SubElement(aspect, "Key").text = key
            ET.SubElement(aspect, "Value").text = value
            
        tree = ET.ElementTree(root)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)