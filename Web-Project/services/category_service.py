from fastapi import HTTPException

from data_.models import Category, Topic, CategoryAccess
from data_.database import read_query, update_query, insert_query
from services.users_service import find_by_id


def get_all_categories():
    data = read_query('''SELECT id, title, description, last_topic, topic_cnt
         FROM category''')

    result = (Category.from_query_result(*row) for row in data)

    if result is not None:
        return get_category_response(result)


def get_category_response(category):

    cat_dict = {}
    for cat in category:
        cat_dict[f'Category name: {cat.title}'] = {

            "Category title": cat.title,
            "Description": cat.description,
            "Number of topics in category": cat.topic_cnt,
            "Last topic is:": cat.last_topic
                                        }

    return cat_dict



def get_topics_for_category(user_id:int, category_id: int, search: str = None, sort_by: str = None,
                            page: int = 1, limit: int = 10):
    category = read_query(
        "SELECT is_private FROM category WHERE id = ?",
        (category_id,)
    )

    if category:
        is_private = category[0][0]

        if not is_private:
            return fetch_all_topics_for_category(category_id, search, sort_by, page, limit)
        else:
            if check_category_read_access(user_id, category_id):
                return fetch_all_topics_for_category(category_id, search, sort_by, page, limit)
            else:
                raise HTTPException(status_code=403, detail="Access denied")

    raise HTTPException(status_code=404, detail="Category not found")


def fetch_all_topics_for_category(category_id: int, search: str, sort_by: str, page: int, limit: int):

    sql = 'SELECT id, title, date, last_reply, users_id, category_id FROM topic WHERE category_id = %s'
    sql_params = (category_id,)

    if search:
        sql += ' AND title LIKE %s'
        sql_params += (f'%{search}%',)

    if sort_by:
        sql += f' ORDER BY 1 {sort_by}'

    sql += ' LIMIT %s OFFSET %s'
    sql_params += (limit, (page - 1) * limit)

    rows = read_query(sql, sql_params)

    topics_dict = {}
    for row in rows:
        topic = Topic.from_query_result(*row)
        topics_dict[f'Topic name: {topic.title}'] = {

            'Topic title': topic.title,
            'Date': topic.cur_date.strftime('%d/%m/%Y'),
            "Last reply is:": topic.last_reply
        }

    return topics_dict

def get_category_by_id(id):
    data = read_query(
        '''SELECT title
        FROM category WHERE id = ?''',
        (id,))

    return data[0][0]


def grant_category_read_access(user_id: int, category_id: int):
    existing_access = read_query(
        "SELECT 1 FROM category_access WHERE user_id = ? AND category_id = ?",
        (user_id, category_id)
    )
    if existing_access:
        update_query(
            "UPDATE category_access SET can_read = TRUE WHERE user_id = ? AND category_id = ?",
            (user_id, category_id)
        )
    else:
        insert_query(
            "INSERT INTO category_access (user_id, category_id, can_read, can_write) VALUES (?, ?, TRUE, FALSE)",
            (user_id, category_id)
        )
    return {"message": "Read access granted to the user."}


def check_category_read_access(user_id: int, category_id: int):
    access = read_query(
        "SELECT can_read FROM category_access WHERE user_id = ? AND category_id = ?",
        (user_id, category_id)
    )
    return access and access[0][0]
