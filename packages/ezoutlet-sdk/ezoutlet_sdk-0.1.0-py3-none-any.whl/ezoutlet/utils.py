import xml.etree.ElementTree as ET


def xml_to_dict(xml_string: str) -> dict:
    """Convert XML string to dictionary."""
    root = ET.fromstring(xml_string)  # noqa: S314
    xml_dict = {}
    for elem in root:
        xml_dict[elem.tag] = elem.text
    return xml_dict
