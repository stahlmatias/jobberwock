import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)

def parse_skills_from_xml(xml_string: str) -> list[str]:
    try:
        root = ET.fromstring(xml_string)
        return [e.text for e in root.findall("skill") if e.text]
    except ET.ParseError as e:
        logger.warning("Error parsing skills XML: %s", e)
        return []

