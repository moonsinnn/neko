from fastapi import FastAPI
import httpx
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/hanime")
async def get_hanime_links():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/hanime")
        links = response.json().get("links", [])
        
        iframe_links = []
        for link in links:
            page_response = await client.get(link)
            soup = BeautifulSoup(page_response.text, 'html.parser')
            iframes = soup.find_all('iframe')
            iframe_links.extend([iframe['src'] for iframe in iframes if 'src' in iframe.attrs])
        
        return {"iframe_links": iframe_links}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000)
