from data_.models import Topic
from data_.database import insert_query, read_query, update_query
from services.users_service import find_by_id
from services.category_service import get_category_by_id


def search_all_topics(search: str = None or None):
    if search is None:
        data = read_query(
            '''SELECT id, title, date, reply_cnt, view_cnt, last_reply, user_id, category_id
               FROM topic''')

        #за да излезе резултат отивам в get_user_by_id/ get_categoy_by_id
    else:
        data = read_query(
            '''SELECT id, title, date, reply_cnt, view_cnt, last_reply, user_id, category_id
               FROM topic 
               WHERE title LIKE ?''', (f'%{search}%',)) # ако искаме да се търси и по дата например, може да се добави още един ?


    return [Topic.from_query_result(*row) for row in data]



def sort_all_topics(topics: list[Topic], sort_by, is_reverse ): #да напиша и с име на категория

    sorted_topics = None
    if sort_by == 'title':
        sorted_topics = sorted(topics, key=lambda x: x.title, reverse=is_reverse)
    if sort_by == 'cur_date':
        sorted_topics = sorted(topics, key=lambda x: x.cur_date, reverse=is_reverse)

    return sorted_topics


def get_topic_by_id(id):
    data = read_query(
        '''SELECT id, title, date, reply_cnt, view_cnt, last_reply, user_id, category_id
               FROM topic
               WHERE id = ?''',
            (id,))

    replies_data = read_query('''
    SELECT id, date, content, likes_cnt, dislike_cnt, topic_id
    FROM reply
    WHERE id = ?''',
                              (data[0][-1], ))
    replies = [r for r in replies_data[0] if not r==None]
    return {'Topic': Topic.from_query_result(*data[0]),     #votes
            'Topic replies': replies}


def create(topic: Topic):

    generated_id = insert_query('''
    INSERT INTO topic(title, date, reply_cnt, view_cnt, last_reply, user_id, category_id) 
     VALUES(?,?,?,?,?,?,?)''',
    (topic.title, topic.cur_date, topic.reply_cnt, topic.view_cnt,
     topic.last_reply, topic.user_id, topic.category_id))

    topic.id = generated_id
    return topic


def update(id, topic: Topic):
    pass


def create_topic_response(topic):
    user = find_by_id(topic.user_id)
    category = get_category_by_id(topic.category_id)
    return {
        'title': topic.title,
        'date of publication': topic.cur_date,
        'published by': f'{user['first_name']} {user['last_name']}',
        'category title': f'{category['title']}'
    }


