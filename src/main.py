import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_async_session
from src.models import News, Comment

app = FastAPI(title="News")


@app.get("/news")
async def get_all_news(session: AsyncSession = Depends(get_async_session)):
    query = select(News).filter(News.deleted == False)
    news = await session.execute(query)
    news = [n.News.to_dict() for n in news.mappings().all()]

    for i, n in enumerate(news):
        comments_query = select(Comment).where(Comment.news_id == n["id"])
        comments = await session.execute(comments_query)
        news[i]['comments_count'] = len(comments.mappings().all())

    return {"news": news, "news_count": len(news)}


@app.get("/news/{news_id}")
async def get_news_by_id(news_id: int, session: AsyncSession = Depends(get_async_session)):
    news = await session.get(News, news_id)
    if not news or news.deleted:
        return HTTPException(status_code=404, detail="News with this id doesn't exist")

    news = news.to_dict()
    query = select(Comment).filter(Comment.news_id == news_id)
    comments = await session.execute(query)
    news['comments'] = [c.Comment for c in comments.mappings().all()]
    news['comments_count'] = len(news['comments'])
    return news


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
