from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import httpx
from selectolax.parser import HTMLParser
from datetime import datetime
import uvicorn

app = FastAPI(
    title="Path of Exile Forum API",
    description="API for retrieving Path of Exile forum thread information",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class Thread(BaseModel):
    title: str
    url: str
    thread_id: str
    author: Optional[str]
    post_date: Optional[str]
    replies: int


class ForumResponse(BaseModel):
    status: str
    timestamp: str
    total_threads: int
    threads: List[Thread]


async def fetch_forum_data(url: str) -> List[Thread]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()

        parser = HTMLParser(response.text)
        threads = []

        for row in parser.css("tr"):
            title_elem = row.css_first("div.title a")
            if title_elem:
                replies_elem = row.css_first("td.views span")
                replies = int(replies_elem.text()) if replies_elem else 0

                post_date_elem = row.css_first("span.post_date")
                post_date = (
                    post_date_elem.text().strip(", ") if post_date_elem else None
                )

                author_elem = row.css_first("span.post_by_account a")
                author = author_elem.text() if author_elem else None

                thread = Thread(
                    title=title_elem.text().strip(),
                    url=f"https://www.pathofexile.com{title_elem.attributes['href']}",
                    thread_id=title_elem.attributes["href"].split("/")[-1],
                    author=author,
                    post_date=post_date,
                    replies=replies,
                )
                threads.append(thread)

        return threads


@app.get("/api/forum", response_model=ForumResponse, tags=["forum"])
async def get_forum_threads():
    """
    Retrieve all threads from Path of Exile announcement forums.
    Returns a list of threads with their details.
    """
    try:
        # List of forum URLs to fetch from
        forums = [
            "https://www.pathofexile.com/forum/view-forum/2212",  # Important announcements
            # "https://www.pathofexile.com/forum/view-forum/3",  # Game announcements
            # "https://www.pathofexile.com/forum/view-forum/366",  # Development manifestos
            # "https://www.pathofexile.com/forum/view-forum/54",  # Technical news
        ]

        all_threads = []
        for forum_url in forums:
            try:
                threads = await fetch_forum_data(forum_url)
                all_threads.extend(threads)
            except Exception as e:
                print(f"Error fetching {forum_url}: {str(e)}")
                continue

        # Sort threads by post date (newest first)
        all_threads.sort(key=lambda x: x.post_date if x.post_date else "", reverse=True)

        return ForumResponse(
            status="success",
            timestamp=datetime.now().isoformat(),
            total_threads=len(all_threads),
            threads=all_threads,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health", tags=["health"])
async def health_check():
    """
    Simple health check endpoint to verify the API is running.
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
