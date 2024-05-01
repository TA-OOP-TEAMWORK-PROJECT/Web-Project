from data_.models import Topic, Vote, Reply
from data_.database import insert_query, read_query, update_query
from services import topic_service


def get_by_id(id):
    data = read_query('''
    SELECT id, date, content, likes_cnt, dislike_cnt, topic_id
    FROM reply
    WHERE id = ?''',
    (id,))

    return Reply.from_query_result(*data[0])


def get_reply(user):

    user_data = read_query('''
    SELECT user_id
    FROM topic
    WHERE id = ?''',
    (user.id))

    if user.user_id == user_data:
        data = read_query('''
        SELECT id, date, content, likes_cnt, dislike_cnt, topic_id, user_id
        FROM reply
        WHERE id = ?''',
        (input(), ))

        return create_reply_response(data[0])

    return


def create(reply):

    generated_id = insert_query('''
    INSERT INTO reply(date, content, likes_cnt, dislike_cnt, topic_id)
    VALUES(?,?,?,?,?)''',
     (reply.cur_date, reply.content, reply.likes_cnt,
      reply.dislikes_cnt, reply.topic_id))

    reply.id = generated_id
    return reply


def create_reply_response(reply):
    topic = topic_service.get_topic_by_id(reply.topic_id) # трябва да има user

    return {
        'content': reply.content,
        'date of publication': reply.cur_date,
        'topic title': f'{topic['Topic'].title}'
    }


def create_vote(new_vote:Vote):
    generated_id = insert_query('''
        INSERT INTO vote(reply_id, sender_id, vote)
        VALUES(?,?,?)''',
        (new_vote.reply_id, new_vote.sender_id, new_vote.vote))
    new_vote.id = generated_id
    return new_vote

def vote_change(new_vote:Vote, reply):

    if new_vote.vote == 1:

        if not reply.dislikes_cnt == 0:
            reply.dislikes_cnt -= 1
        reply.likes_cnt += 1

        update_query('''
        UPDATE reply
        SET likes_cnt''',
                 (reply.likes_cnt, ))

    if new_vote.vote == 0:
        if not reply.likes_cnt == 0:
            reply.likes_cnt -= 1
        reply.dislikes_cnt += 1
        update_query('''
        UPDATE reply
        SET dislike_cnt = ?''',
                 (reply.dislikes_cnt, ))


    return 'Vote has been changed'


def get_vote_by_reply_id(id):
    data = read_query('''
    SELECT reply_id, sender_id, vote
    FROM vote
    WHERE reply_id=?''',
               (id, ))


    return data[0]
