import zipfile
from defusedxml import ElementTree 
from xml.etree.ElementTree import fromstring
import os,re
from .myutility import xml_tags,tag_to_latex_exp


class Document:
    n_images = 0
    def __init__(self, document, inline_delimiter='$', block_delimiter='$$'):
        self.document = document
        self.inline_delimiter = inline_delimiter
        self.block_delimiter = block_delimiter

    
    def get_text(self, get_header_text=False, get_footer_text=False, image_dir=None, extensions=None):
        print("get text call")
        if extensions is None:
            extensions = ['.jpg', '.jpeg', '.png', '.svg', '.bmp', '.gif']
        zip_f = zipfile.ZipFile(self.document)
        text = ''
        for f in zip_f.namelist():
            if get_header_text and f.startswith('word/header'):
                text += self.xml_to_text(zip_f.read(f))
            if f.startswith('word/document'):
                text += self.xml_to_text(zip_f.read(f))
            if get_footer_text and f.startswith('word/footer'):
                text += self.xml_to_text(zip_f.read(f))
        
        if image_dir is not None:
            for f in zip_f.namelist():
                _, extension = os.path.splitext(f)
                if extension in extensions:
                    destination = os.path.join(image_dir, os.path.basename(f))
                    with open(destination, 'wb') as destination_file:
                        destination_file.write(zip_f.read(f))
        zip_f.close()
        return text


    def extract_images_from_docx(self, extract_to_folder='images'):
        docx_path = self.document
        with zipfile.ZipFile(docx_path, 'r') as docx:
            # Ensure the target folder exists
            if not os.path.exists(extract_to_folder):
                os.makedirs(extract_to_folder)
            
            for item in docx.namelist():
                if item.startswith('word/media/'):
                    print(f'Found image: {item}')
                    new_filename = os.path.basename(item)
                    source = docx.open(item)
                    target = open(os.path.join(extract_to_folder, new_filename), "wb")
                    with source, target:
                        target.write(source.read())


    def get_html_code(self, get_header_text=False, get_footer_text=False, image_dir=None, extensions=None):
        print("get text call")
        if extensions is None:
            extensions = ['.jpg', '.jpeg', '.png', '.svg', '.bmp', '.gif']
        zip_f = zipfile.ZipFile(self.document)
        text = ''
        for f in zip_f.namelist():
            if get_header_text and f.startswith('word/header'):
                text += self.xml_to_text(zip_f.read(f))
            if f.startswith('word/document'):
                text += self.xml_to_html(zip_f.read(f))
            if get_footer_text and f.startswith('word/footer'):
                text += self.xml_to_text(zip_f.read(f))
        
        if image_dir is not None:
            for f in zip_f.namelist():
                _, extension = os.path.splitext(f)
                if extension in extensions:
                    destination = os.path.join(image_dir, os.path.basename(f))
                    with open(destination, 'wb') as destination_file:
                        destination_file.write(zip_f.read(f))
        zip_f.close()
        return text    
    
    def xml_to_text(self, xml): 
        text = ''
        n_images = 0
        root = ElementTree.fromstring(xml)
        for child in root.iter():
            if child.get('docxlatex_skip_iteration', False):
                continue
        
            if child.tag == xml_tags('w:t'):
                text += child.text if child.text is not None else ''
            elif child.tag == xml_tags('m:oMath'):
                text += self.inline_delimiter + ' '
                text += tag_to_latex_exp(child)
                text += ' ' + self.inline_delimiter
            elif child.tag == xml_tags('m:r'):
                text += ''.join(child.itertext())
            elif child.tag == xml_tags('w:drawing'):
                print("img")
                n_images += 1
                text += f'\nIMAGE#{n_images}-image{n_images}\n'
        
            elif child.tag == xml_tags('w:tab'):
                text += '\t'
            elif child.tag == xml_tags('w:br') or child.tag == xml_tags('w:cr'):
                text += '\n'
            elif child.tag == xml_tags('w:p'):
                text += '\n\n'
        
        text = re.sub(r'\n(\n+)\$(\s*.+\s*)\$\n', r'\n\1$ \2 $', text)
        return text

    def get_t(self,xml):
      global n_images  # Assuming n_images is initialized elsewhere
      text=''
      for e in xml:
        if e.tag == xml_tags('w:t'):
          text += e.text
        elif e.tag == xml_tags('w:drawing'):
          n_images += 1
          text += f'<img src="word/media/image{n_images}.png" alt="Image{n_images}"/>\n'
      if len(text)>0:
        return text
      return ''


    def get_paragraphs(self, xml):
      text = ''
      for e in xml: #r,omath
        if e.tag == xml_tags("w:r"):
          text += self.get_t(e)
        elif e.tag == xml_tags("w:hyperlink"):
          hyperlink_text = ''.join(e.itertext())
          text += f'<a href="link_placeholder.html">{hyperlink_text}</a>'
        elif e.tag == xml_tags('m:oMath'):
          math_latex =  ' ' + self.inline_delimiter + tag_to_latex_exp(e) + ' ' + self.inline_delimiter
          text += math_latex
      if len(text)>0:
        return "<p>"+text+"</p>"
      return ''

    def xml_to_html(self, xml):
        self.extract_images_from_docx()
        root = fromstring(xml)
        html = ''
        in_table = False  
        for doc in root:
          if doc.tag==xml_tags('w:body') :
            html+= "<body>"
            for doc_element in doc:
              if doc_element.tag == xml_tags('w:p'):
                html +=self.get_paragraphs(doc_element)
              elif doc_element.tag == xml_tags('w:tbl'):
                html+=self.get_table(doc_element)

        html += '</body>'
        html = html.replace("$ $", "$ ")  # Example replacement, modify as necessary
        return html




    def get_table(self, element, depth=0):
        global n_images
        html = ""
        if element.tag == xml_tags('w:tbl'):
            # Start a new table
            html += f"{'  ' * depth}<table border='1'>\n"

            for child in element:
                if child.tag == xml_tags('w:tr'):
                    html += f"{'  ' * depth} <tr>\n"
                    for cell in child.findall(xml_tags('w:tc')):
                        cell_html = ''
                        # Check for nested tables or special tags like m:oMath in the cell
                        for item in cell:
                            if item.tag == xml_tags('w:tbl'):
                                # Handle nested table recursively
                                cell_html += self.get_table(item, depth + 1)
                            elif item.tag == xml_tags('w:p'):
                                # Handle paragraph
                                cell_html +=self.get_paragraphs(item)
                        
                        html += f"{'  ' * depth}  <td>{cell_html}</td>\n" if len(cell_html)> 0 else '' 
                    html += f"{'  ' * depth} </tr>\n"
            
            html += f"{'  ' * depth}</table>\n"
            return html
        else:
            # Process non-table elements or skip
            for child in element:
                html += self.get_html(child, depth)
        return html



