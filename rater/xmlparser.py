import xml.etree.ElementTree as ET

def parse_xml(xml_data: str) -> dict[str, int]:
    root = ET.fromstring(xml_data)

    # Build dictionary: {name attribute -> text content as int}
    skill_dict = {skill.get('name'): int(skill.text) for skill in root.findall('Skill')}

    return skill_dict