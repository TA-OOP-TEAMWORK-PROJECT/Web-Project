from typing import List
from data_.models import Category, Topic
from data_.database import read_query


def get_all_categories() -> List[Category]:
    sql = 'SELECT * FROM categories'
    categories = read_query(sql)
    return [Category.from_query_result(*category) for category in categories]


def get_topics_for_category(category_id: int, search: str = None, sort_by: str = None, page: int = 1,
                            limit: int = 10) -> List[Topic]:
    sql = 'SELECT id, title, date, reply_cnt, view_cnt, last_reply, users_id, category_id FROM topics WHERE category_id = %s'
    sql_params = (category_id,)

    if search:
        sql += ' AND title LIKE %s'
        sql_params += (f'%{search}%',)

    if sort_by:
        sql += f' ORDER BY {sort_by}'

    sql += ' LIMIT %s OFFSET %s'
    sql_params += (limit, (page - 1) * limit)

    rows = read_query(sql, sql_params)

    topics = []
    for row in rows:
        topic = Topic(
            id=row[0],
            title=row[1],
            date=row[2],
            reply_cnt=row[3] if row[3] is not None else 0,
            view_cnt=row[4] if row[4] is not None else 0,
            last_reply=row[5] if row[5] is not None else '',
            users_id=row[6],
            category_id=row[7]
        )
        topics.append(topic)

    return topics

def get_category_by_id(id):
    data = read_query(
        '''SELECT title
        FROM category WHERE id = ?''',
        (id,))

    return data[0][0]
