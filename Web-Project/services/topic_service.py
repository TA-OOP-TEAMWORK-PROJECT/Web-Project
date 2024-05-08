from data_.models import Topic, Reply
from data_.database import insert_query, read_query, update_query
from services import reply_service
from services.users_service import find_by_id
from services.category_service import get_category_by_id


def search_all_topics(search: str = None or None):
    if search is None:
        data = read_query(
            '''SELECT id, title, date, last_reply, user_id, category_id
               FROM topic''')

        #за да излезе резултат отивам в get_user_by_id/ get_categoy_by_id
    else:
        data = read_query(
            '''SELECT id, title, date, last_reply, user_id, category_id
               FROM topic 
               WHERE title LIKE ?''', (f'%{search}%',)) # ако искаме да се търси и по дата например, може да се добави още един ?

    result = [Topic.from_query_result(*row) for row in data]
    return get_all_topic_response(result)


def sort_all_topics(topics: list[Topic], sort_by, is_reverse ):

    sorted_topics = None
    if sort_by == 'title':
        sorted_topics = sorted(topics, key=lambda x: x.title, reverse=is_reverse)
    if sort_by == 'cur_date':
        sorted_topics = sorted(topics, key=lambda x: x.cur_date, reverse=is_reverse)

    return sorted_topics


def get_topic_by_id(id, cur_user):
    data = read_query(
        '''SELECT id, title, date, last_reply, users_id, category_id
               FROM topic
               WHERE id = ?''',
            (id,))

    replies_data = read_query('''
    SELECT id, date, content, likes_cnt, dislike_cnt, topic_id
    FROM reply
    WHERE id = ?''',
                              (data[0][-1], ))
    a = replies_data

    replies = [Reply.from_query_result(*r) for r in replies_data if not r==None]
    topic = Topic.from_query_result(*data[0])
    return {f'Topic {topic.title}': create_topic_response(topic, cur_user),     #votes
            'Topic replies': get_topic_replies(replies)}

def get_topic_replies(replies):

    topic_rep = []
    for r in replies:
        topic_rep.append(
            {
             'Reply date': r.cur_date.strftime('%d/%m/%Y'),
            'Content' : r.content
            }
        )
    return topic_rep

def create(topic: Topic, cur_user, category_id):

    generated_id = insert_query('''
    INSERT INTO topic(title, date, user_id, category_id) 
    VALUES(?,?,?,?)''',
    (topic.title, topic.cur_date, cur_user.id, category_id))

    topic.id = generated_id
    topic.category_id = category_id
    return topic


def best_reply(topic_id, reply_id, user):

    topic_user = read_query('''
    SELECT user_id
    FROM topic
    WHERE id=?''',
    (topic_id, ))

    if topic_user[0][0] == user.id:

        insert_best_reply = insert_query('''
        UPDATE topic
        SET best_reply = ?
        WHERE id = ? ''',
        (reply_id, topic_id))

    reply = reply_service.get_by_id(reply_id)
    return (f' The best reply is :'
            f'{reply_service.create_reply_response(reply)}')


def create_topic_response(topic, user):

    category = get_category_by_id(topic.category_id)
    return {
        'title': topic.title,
        'date of publication': topic.cur_date.strftime('%Y/%m/%d'),
        'published by': f'{user.username}',
        'category title': f'{category}'
    }


def get_all_topic_response(topics):

    topics_dict = {}
    for data in topics:
        topics_dict[f'Topic name: {data.title}'] = {

            'Topic title': data.title,
            'Date': data.cur_date.strftime('%d/%m/%Y'),
            "Last reply is:": data.last_reply
        }

    return topics_dict












# def get_topic_response(topic):
#
#     topic_dict = {}
#
#     for top in topic:
#         topic_dict[f'Topic name: {topic.title}'] = {
#
#             'Topic title': topic.title,
#             'Date': topic.cur_date.strftime('%d/%m/%Y'),
#             'All Replies': topic.reply_cnt,
#             'All views': topic.view_cnt,
#             'Last reply is:': topic.last_reply,
#             'Topic is created by:': topic.user_id,
#             'Best reply is:': topic.best_reply
#         }
#
#     return topic_dict




 #взимаме отгпвпр по желание на автора на топика:
 # data = read_query('''
 #        SELECT id, date, content, likes_cnt, dislike_cnt, topic_id, user_id
 #        FROM reply
 #        WHERE id = ?''',
 #        (input(), ))