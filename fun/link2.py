from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import httpx
from bs4 import BeautifulSoup
import os

app = FastAPI()

# Environment variables for API endpoints
api = "localhost:5000" #os.getenv("API_ENDPOINT")
api2 = "localhost:8000" #os.getenv("API2_ENDPOINT")

@app.get("/scrape", response_class=JSONResponse)
async def scrape():
    url = f'http://{api}/random'

    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=str(exc))

    soup = BeautifulSoup(response.text, 'html.parser')

    links = extract_links(soup)
    img = extract_img(soup)

    return {"links": links, "covers": img}

def extract_links(soup):
    return [item['href'] for item in soup.select('.list-group-item a') if 'href' in item.attrs]

def extract_img(soup):
    return [item['src'] for item in soup.select('.card-body img') if 'src' in item.attrs]

@app.get("/hanime")
async def get_links():
    url = f"http://{api2}/scrape"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        links = data.get("links", [])
        return {"links": [f"http://{api}/hanime/{link}" for link in links]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

"""from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import httpx
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/scrape", response_class=JSONResponse)
async def scrape():
    url = 'http://'+ api + '/random'

    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=str(exc))

    soup = BeautifulSoup(response.text, 'html.parser')
    links = extract_links(soup)
    img = extract_img(soup)

    #return {"covers": img}
    return {"links": links}

def extract_links(soup):
    return [item['href'] for item in soup.select('.list-group-item a') if 'href' in item.attrs]
def extract_img(soup):
    return [item['src'] for item in soup.select('.card-body img') if 'src' in item.attrs]

@app.get("/hanime/")
async def get_links():
    url = "http://"+ api2 +"/scrape"  # Replace with the actual URL
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        links = data.get("links", [])
        return {"links": [f"http://"+ api +"/hanime/{link}" for link in links]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""
