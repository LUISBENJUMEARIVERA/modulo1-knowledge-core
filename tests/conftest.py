"""Configuración global de fixtures para pytest."""

import pytest


@pytest.fixture
def sample_html() -> str:
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Tecnoquímicas S.A. - Innovación Farmacéutica</title>
        <style>body { font-family: sans-serif; }</style>
        <script>console.log("tracking");</script>
    </head>
    <body>
        <nav><a href="/home">Inicio</a><a href="/nosotros">Nosotros</a></nav>
        <header><h1>Tecnoquímicas Farma</h1></header>
        <main>
            <article>
                <h2>Planta Farmacéutica de Villa Rica</h2>
                <p>Tecnoquímicas S.A. cuenta con una moderna planta de producción farmacéutica en Villa Rica, Cauca,
                equipada con estándares internacionales de manufactura (GMP) y tecnología de punta para la elaboración
                de medicamentos esenciales, sólidos y líquidos estériles.</p>
                <p>La compañía es líder en el mercado colombiano con marcas reconocidas como MK, Bonfiest, Noraver, Yodora
                y Sal de Frutas Lua, brindando confianza, bienestar y calidad garantizada a millones de hogares.</p>
            </article>
        </main>
        <footer><p>&copy; 2026 Tecnoquímicas S.A. Todos los derechos reservados.</p></footer>
    </body>
    </html>
    """


@pytest.fixture
def sample_short_html() -> str:
    return """
    <html>
        <head><title>Test</title></head>
        <body>
            <nav>Ignored Nav</nav>
            <p>Contenido limpio estructurado para prueba de fallback heuristico con longitud suficiente para superar el filtro.</p>
        </body>
    </html>
    """
