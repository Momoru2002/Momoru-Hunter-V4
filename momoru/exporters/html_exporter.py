import os
from jinja2 import Template
from momoru.logger import CyberpunkLogger

class HtmlExporter:
    @staticmethod
    def export(data: dict, output_path: str):
        template_content = """
        <html>
        <head><title>Cyberpunk Intelligence Report</title></head>
        <body style="background:#0d0d1a; color:#00ffcc; font-family:monospace; padding:40px;">
            <h1>🚨 MOMORU FORENSIC ANALYSIS: PROFILE REPORT</h1>
            <hr style="border-color:#ff0055;">
            <h3>TARGET: {{ username }}</h3>
            <h2>STATUS: <span style="color:#ff0055;">{{ status }}</span></h2>
            <p>CONFIDENCE SCORE: {{ confidence_score }}%</p>
            <p>SIMILARITY INDEX: {{ similarity_index }}</p>
            <p>TOTAL DATA DISCOVERED: {{ total_scanned_comments }}</p>
        </body>
        </html>
        """
        template = Template(template_content)
        rendered = template.render(data)
        with open(output_path, "w") as f:
            f.write(rendered)
        CyberpunkLogger.success(f"HTML Dossier compiled successfully: {output_path}")