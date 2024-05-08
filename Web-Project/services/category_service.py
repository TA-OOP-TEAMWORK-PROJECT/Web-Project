from data_.models import Category, Topic
from data_.database import read_query


def get_all_categories():
    data = read_query('''SELECT id, title, description, last_topic, topic_cnt, user_id
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



def get_topics_for_category(category_id: int, search: str = None, sort_by: str = None,
                            page: int = 1, limit: int = 10):
    sql = 'SELECT id, title, date, last_reply, user_id, category_id FROM topic WHERE category_id = %s'
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
