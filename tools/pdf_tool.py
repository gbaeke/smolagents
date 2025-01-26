from smolagents import Tool
from weasyprint import HTML, CSS
from markdown2 import Markdown
import os
from datetime import datetime
from typing import Optional
import requests
from urllib.parse import urlparse

class PDFTool(Tool):
    name = "pdf_creator"
    description = """
    This tool creates PDF documents from text and images and saves them locally.
    It can include text, web images, and basic formatting.
    The input text can be in markdown format.
    Perfect for creating reports, saving search results, or documenting information.
    The PDF will be saved in the current directory with a timestamp.
    Text needs to be in markdown format.
    """
    
    inputs = {
        "content": {
            "type": "string",
            "description": "The content to include in the PDF. Can contain text and image URLs. Text needs to be in markdown format.",
        },
        "title": {
            "type": "string",
            "description": "The title of the PDF document",
            "default": "Report",
            "nullable": True
        },
        "filename": {
            "type": "string",
            "description": "The filename for the PDF (without extension)",
            "nullable": True
        }
    }
    output_type = "string"

    def _download_image(self, url: str) -> Optional[str]:
        """Download image from URL and save locally"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            parsed_url = urlparse(url)
            image_filename = os.path.basename(parsed_url.path) or f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            image_path = os.path.join("images", image_filename)
            os.makedirs("images", exist_ok=True)
            
            with open(image_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return image_path
        except Exception as e:
            print(f"Failed to download image from {url}: {str(e)}")
            return None

    def _create_pdf(self, content: str, title: str, filename: str) -> str:
        """Create PDF with content and images"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{title.lower().replace(' ', '_')}_{timestamp}"
        
        # Create pdfs directory if it doesn't exist
        os.makedirs("pdfs", exist_ok=True)
        pdf_path = os.path.join("pdfs", f"{filename}.pdf")

        # Convert markdown to HTML
        markdowner = Markdown(extras=['fenced-code-blocks', 'tables', 'code-friendly'])
        html_content = markdowner.convert(content)

        # Add some basic styling
        html_template = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; }}
                    h1 {{ color: #2C3E50; }}
                    img {{ max-width: 100%; height: auto; }}
                    pre {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; }}
                    code {{ background-color: #f5f5f5; padding: 2px 5px; border-radius: 3px; }}
                    blockquote {{ border-left: 4px solid #ccc; margin-left: 0; padding-left: 15px; }}
                </style>
            </head>
            <body>
                {html_content}
            </body>
        </html>
        """

        # Convert HTML to PDF
        HTML(string=html_template).write_pdf(pdf_path)
        return pdf_path

    def forward(self, content: str, title: str = "Report", filename: str = None) -> str:
        try:
            pdf_path = self._create_pdf(content, title, filename)
            return f"PDF created successfully: {pdf_path}"
        except Exception as e:
            raise Exception(f"PDF creation failed: {str(e)}") 