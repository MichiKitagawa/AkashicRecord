from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import tempfile
from pathlib import Path
from ..errors import PDFGenerationError

class PDFService:
    def __init__(self):
        self.template_dir = Path(__file__).parent.parent / "templates"
        self.css = CSS(string='''
            @page {
                size: A4;
                margin: 2.5cm;
                @top-center {
                    content: "アカシックAI占い";
                }
                @bottom-center {
                    content: counter(page);
                }
            }
            body {
                font-family: "Noto Sans JP", sans-serif;
                line-height: 1.6;
            }
            h1 {
                color: #6B46C1;
                font-size: 24px;
                text-align: center;
                margin-bottom: 2em;
            }
            .diagnosis-section {
                margin-bottom: 2em;
            }
            .diagnosis-section h2 {
                color: #4A5568;
                font-size: 18px;
                border-bottom: 2px solid #6B46C1;
                padding-bottom: 0.5em;
                margin-bottom: 1em;
            }
        ''')

    def generate_pdf(self, name: str, birth_date: str, result: str) -> bytes:
        """
        診断結果のPDFを生成する
        """
        try:
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>アカシックAI占い - 診断結果</title>
            </head>
            <body>
                <h1>アカシックAI占い - 診断結果</h1>
                
                <div class="diagnosis-section">
                    <h2>基本情報</h2>
                    <p>お名前: {name}</p>
                    <p>生年月日: {birth_date}</p>
                </div>
                
                <div class="diagnosis-section">
                    <h2>診断結果</h2>
                    <div class="result-content">
                        {result.replace('\n', '<br>')}
                    </div>
                </div>
            </body>
            </html>
            """

            # 一時ファイルを作成してPDFを生成
            with tempfile.NamedTemporaryFile(suffix='.html', mode='w', encoding='utf-8') as f:
                f.write(html_content)
                f.flush()
                
                font_config = FontConfiguration()
                html = HTML(filename=f.name)
                return html.write_pdf(stylesheets=[self.css], font_config=font_config)

        except Exception as e:
            raise PDFGenerationError(f"PDF生成エラー: {str(e)}")

pdf_service = PDFService() 