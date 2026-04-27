import os
import zipfile
import xml.etree.ElementTree as ET

def parse_hwpx(file_path: str) -> str:
    """
    HWPX 파일은 ZIP 아카이브입니다.
    보통 Contents/section0.xml (또는 section1.xml 등) 내부에 실제 텍스트 내용이 있습니다.
    """
    text_blocks = []
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            # Contents 폴더 내의 section XML 파일 찾기
            section_files = [f for f in zf.namelist() if f.startswith('Contents/section') and f.endswith('.xml')]
            
            for sec_file in section_files:
                xml_content = zf.read(sec_file)
                root = ET.fromstring(xml_content)
                
                # namespace 처리 (hp:t)
                # ElementTree에서 ns가 포함된 태그는 {namespace_uri}t 형태로 나옵니다.
                # 편의상 namespace 무시하고 모든 't'로 끝나는 태그를 찾거나, 
                # hp:t 형태를 잡기 위해 tag string의 endswith를 사용합니다.
                for elem in root.iter():
                    if elem.tag.endswith('}t') or elem.tag == 't':
                        if elem.text:
                            text_blocks.append(elem.text)
                            
    except Exception as e:
        print(f"HWPX parse error: {e}")
        
    return "\n".join(text_blocks)

def parse_docx(file_path: str) -> str:
    """
    DOCX 파일은 ZIP 아카이브입니다.
    word/document.xml 내부에 실제 텍스트 내용이 있습니다.
    """
    text_blocks = []
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            if 'word/document.xml' in zf.namelist():
                xml_content = zf.read('word/document.xml')
                root = ET.fromstring(xml_content)
                
                # namespace 처리 (w:t)
                for elem in root.iter():
                    if elem.tag.endswith('}t') or elem.tag == 't':
                        if elem.text:
                            text_blocks.append(elem.text)
                            
    except Exception as e:
        print(f"DOCX parse error: {e}")
        
    return "\n".join(text_blocks)

def parse_document(file_path: str) -> str:
    """확장자에 맞게 문서를 파싱하여 텍스트를 반환합니다."""
    if not os.path.exists(file_path):
        return ""
    
    ext = file_path.lower().split('.')[-1]
    if ext == 'hwpx':
        return parse_hwpx(file_path)
    elif ext == 'docx':
        return parse_docx(file_path)
    else:
        # 지원되지 않는 확장자의 경우 (txt 등일 경우 대비)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return ""
