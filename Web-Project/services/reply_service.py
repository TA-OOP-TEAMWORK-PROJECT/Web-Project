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

def vote_change(new_vote:Vote, old_vote_data, reply):

    update_query('''
    DELETE  FROM vote
    WHERE reply_id = ?''',
                 (reply.id,))

    insert_query('''
    INSERT INTO vote(reply_id, sender_id, vote)
    VALUES(?,?,?)''',
                 (reply.id, old_vote_data[1], new_vote.vote))

    if reply.is_voted_cnt is None:
        reply.is_voted_cnt = 1
    else:
        reply.is_voted_cnt += 1

    return new_vote.vote

def get_vote_by_reply_id(id):
    data = read_query('''
    SELECT reply_id, sender_id, vote
    FROM vote
    WHERE reply_id=?''',
               (id, ))


    return data[0]