import requests
import pdfplumber
from pathlib import Path
from datetime import datetime

# URL do currículo Lattes (seu ID)
LATTES_URL = "https://lattes.cnpq.br/2224107126204328"
PDF_PATH = Path("curriculo.pdf")
HTML_PATH = Path("curriculo.html")

def baixar_pdf():
    """Baixa o PDF do currículo Lattes"""
    response = requests.get(LATTES_URL)
    if response.status_code == 200:
        with open(PDF_PATH, "wb") as f:
            f.write(response.content)
        print("✅ PDF baixado com sucesso!")
    else:
        raise Exception(f"❌ Erro ao baixar PDF: {response.status_code}")

def extrair_texto():
    """Extrai texto do PDF usando pdfplumber"""
    texto = ""
    with pdfplumber.open(PDF_PATH) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                texto += content + "\n"
    return texto.strip()

def gerar_html(texto):
    """Gera um HTML estilizado com base no texto extraído"""
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Currículo — Francisco Taylan Santos de Lima</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Inter', sans-serif;
      max-width: 900px;
      margin: auto;
      padding: 20px;
      background: #f9fafb;
      color: #1f2937;
      line-height: 1.6;
    }}
    h1 {{
      color: #2156d6;
      text-align: center;
    }}
    h2 {{
      margin-top: 32px;
      color: #374151;
      border-bottom: 2px solid #e5e7eb;
      padding-bottom: 6px;
    }}
    pre {{
      white-space: pre-wrap;
      background: #ffffff;
      padding: 16px;
      border: 1px solid #e5e7eb;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    footer {{
      margin-top: 40px;
      text-align: center;
      font-size: 14px;
      color: #6b7280;
    }}
  </style>
</head>
<body>
  <h1>Currículo Lattes — Francisco Taylan Santos de Lima</h1>
  <h2>Versão automática</h2>
  <pre>{texto}</pre>
  <footer>Atualizado automaticamente em {data}</footer>
</body>
</html>
"""
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"📄 HTML gerado em: {HTML_PATH}")

if __name__ == "__main__":
    baixar_pdf()
    texto = extrair_texto()
    gerar_html(texto)
