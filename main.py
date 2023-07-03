from aiofauna import AioFauna, WebSocketResponse

from src.tools.sitemap import SiteMapTool

app = AioFauna()

@app.get("/sitemap")
async def ingest_sitemap(url:str):
    tool = SiteMapTool(url)
    await tool.run(url)
    return {
        "url": url,
        "results": tool.urls
    }
    
@app.get("/")
async def root():
    html = """<html>
    <head>
        <title>SiteMap Tool</title>
    </head>
    <body>
        <h1>SiteMap Tool</h1>
            <input type="text" id="url" name="url" value="" placeholder="https://example.com" style="width: 100%; height: 50px; font-size: 20px; padding: 10px; margin-bottom: 10px;">

            <button onclick="connect()">Connect</button>
            
            <div id="progress" style="width: 100%; height: 50px; font-size: 20px; padding: 10px; margin-bottom: 10px;"></div>
            
            <div id="results" style="width: 100%; height: 50px; font-size: 20px; padding: 10px; margin-bottom: 10px;"></div>
            
            <script>
                var ws = null;
                var progress = document.getElementById("progress");
                var results = document.getElementById("results");
                var url = document.getElementById("url");
                
                function connect() {
                    ws = new WebSocket("ws://localhost:4444/ws?url=" + url.value);
                    ws.onmessage = function(event) {
                        var data = JSON.parse(event.data);
                        if (data.type == "progress") {
                            progress.innerHTML = data.progress;
                        } else if (data.type == "done") {
                            results.innerHTML = JSON.stringify(data.data);
                        }
                    }
                }
            </script>
    </body>
    </html>"""
    
    return html


from aiohttp import web

web.run_app(app, port=4444)
