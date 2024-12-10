from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pyppeteer import launch

app = FastAPI()

# Permitir solicitudes desde cualquier origen (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puede especificar un dominio si lo deseas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/scrape-noticias")
async def scrape_noticias():
    try:
        # Lanzar el navegador
        browser = await launch()
        page = await browser.newPage()
        await page.goto('https://www.milenio.com/temas/contabilidad')  # Cambia la URL según el sitio

        # Realizar scraping
        noticias = await page.evaluate('''() => {
            const data = [];
            document.querySelectorAll('.clase-noticia').forEach((noticia) => {
                const titulo = noticia.querySelector('.titulo')?.innerText;
                const enlace = noticia.querySelector('a')?.href;
                if (titulo && enlace) {
                    data.push({ titulo, enlace });
                }
            });
            return data;
        }''')

        # Cerrar el navegador
        await browser.close()

        # Devolver las noticias
        return JSONResponse(content=noticias)
    except Exception as e:
        return JSONResponse(content={"error": f"Error en el scraping: {str(e)}"}, status_code=500)
