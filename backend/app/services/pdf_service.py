from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import tempfile
from pathlib import Path
from ..errors import PDFGenerationError
import logging
import platform

# ロガーの設定
logger = logging.getLogger(__name__)

class PDFService:
    def __init__(self):
        try:
            self.template_dir = Path(__file__).parent.parent / "templates"
            
            # OSに応じたフォント設定
            if platform.system() == 'Windows':
                font_family = '"Yu Gothic", "Meiryo", sans-serif'
            else:
                font_family = '"Noto Sans JP", "Hiragino Sans", sans-serif'
                
            self.css = CSS(string=f'''
                @page {{
                    size: A4;
                    margin: 2.5cm;
                    @top-center {{
                        content: "アカシックAI占い";
                        font-family: {font_family};
                    }}
                    @bottom-center {{
                        content: counter(page);
                    }}
                }}
                body {{
                    font-family: {font_family};
                    line-height: 1.6;
                    font-size: 12pt;
                }}
                h1 {{
                    color: #6B46C1;
                    font-size: 24pt;
                    text-align: center;
                    margin-bottom: 2em;
                    font-weight: bold;
                }}
                .diagnosis-section {{
                    margin-bottom: 2em;
                }}
                .diagnosis-section h2 {{
                    color: #4A5568;
                    font-size: 18pt;
                    border-bottom: 2px solid #6B46C1;
                    padding-bottom: 0.5em;
                    margin-bottom: 1em;
                    font-weight: bold;
                }}
                .result-content {{
                    white-space: pre-line;
                    line-height: 1.8;
                }}
            ''')
            logger.debug(f"PDFサービスの初期化が完了しました（OS: {platform.system()}）")
        except Exception as e:
            logger.error(f"PDFサービスの初期化に失敗しました: {str(e)}")
            raise PDFGenerationError(f"PDFサービスの初期化に失敗しました: {str(e)}")

    def generate_pdf(self, name: str, birth_date: str, result: str) -> bytes:
        """
        診断結果のPDFを生成する
        """
        try:
            logger.debug(f"PDF生成開始: {name}")
            
            # 入力値の検証
            if not name or not birth_date or not result:
                raise PDFGenerationError("必要な情報が不足しています")
                
            html_content = f"""
            <!DOCTYPE html>
            <html lang="ja">
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
            with tempfile.NamedTemporaryFile(suffix='.html', mode='w', encoding='utf-8', delete=False) as f:
                try:
                    f.write(html_content)
                    f.flush()
                    logger.debug("一時HTMLファイルを作成しました")
                    
                    font_config = FontConfiguration()
                    html = HTML(filename=f.name)
                    pdf_content = html.write_pdf(
                        stylesheets=[self.css],
                        font_config=font_config,
                        optimize_size=('fonts', 'images')
                    )
                    logger.debug("PDF生成が完了しました")
                    return pdf_content
                    
                except Exception as e:
                    logger.error(f"PDF生成中にエラーが発生しました: {str(e)}")
                    raise PDFGenerationError(f"PDF生成中にエラーが発生しました: {str(e)}")
                finally:
                    # 一時ファイルを確実に削除
                    try:
                        Path(f.name).unlink(missing_ok=True)
                    except Exception as e:
                        logger.warning(f"一時ファイルの削除に失敗しました: {str(e)}")

        except Exception as e:
            logger.error(f"PDF生成処理全体でエラーが発生しました: {str(e)}")
            raise PDFGenerationError(f"PDF生成処理全体でエラーが発生しました: {str(e)}")

pdf_service = PDFService() 