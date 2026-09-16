from app.models.news import Category, News
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


# 获取新闻分类
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Category).offset(skip).limit(limit)
    )
    return result.scalars().all()

# 获取新闻列表
async def get_news_list(db: AsyncSession, category_id: int = None, offset: int = 0, limit: int = 100):
    result = await db.execute(
        select(News)
            .where(News.category_id == category_id)
            .offset(offset)
            .limit(limit)
    )
    return result.scalars().all()

# 获取分类新闻总数
async def get_category_news_count(db: AsyncSession, category_id: int):
    result = await db.execute(
        select(func.count(News.id))
            .where(News.category_id == category_id)
    )
    return result.scalar_one()

# 获取新闻详情
async def get_news_detail(db: AsyncSession, news_id: int):
    result = await db.execute(
        select(News).where(News.id == news_id)
    )
    return result.scalar_one_or_none()
