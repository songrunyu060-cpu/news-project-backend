from app.models.news import Category, News
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update


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

# 新增浏览量
async def increase_news_views(db: AsyncSession, news_id: int):
    result = await db.execute(
        update(News)
            .where(News.id == news_id)
            .values(views=News.views + 1)
    )
    await db.commit()
    # rowcount 表示受影响的行数
    return result.rowcount > 0

# 获取相关新闻
async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    result = await db.execute(
        select(News)
            .where(News.id != news_id, News.category_id == category_id)
            .order_by(
                News.views.desc(),
                News.publish_time.desc()
            )
            .limit(limit)
    )
    related_news = result.scalars().all()
    # 将查询结果转换为列表
    related_list = [
        {
            "id": item.id,
            "title": item.title,
            "content": item.content,
            "image": item.image,
            "author": item.author,
            "publishTime": item.publish_time,
            "categoryId": item.category_id,
            "views": item.views
        }
        for item in related_news
    ]
    return related_list
