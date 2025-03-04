from xml.etree.ElementTree import Element, SubElement
from typing import List, Dict, Optional, Union, Tuple, Any

def to_xml(parent: Element, children: List[Tuple[str, Union[str, List, Any], Optional[Dict[str, str]]]]):
    """
    Recursively builds XML structure from a list of tuples.
    
    Args:
        parent: Parent XML element to add children to
        children: List of tuples (tag, value, attributes) where:
            - tag is the element tag name
            - value is either a string (for text content) or a list (for nested elements)
            - attributes is an optional dictionary of element attributes
    
    Returns:
        The parent element with all children added
    """
    for child in children:
        if (len(child) > 2):
            key, value, attr = child
            if isinstance(value, list):
                to_xml(SubElement(parent, key, attrib=attr), value)
            else:
                SubElement(parent, key, attrib=attr).text = str(value)
        else:
            key, value = child
            if isinstance(value, list):
                to_xml(SubElement(parent, key), value)
            else:
                SubElement(parent, key).text = str(value)

    return parent
