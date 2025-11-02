"""数据库初始化脚本"""

from app.shared.database import engine, Base
from app.infrastructure.database.models import Card


def create_tables():
    """创建所有数据库表"""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("数据库表创建完成！")