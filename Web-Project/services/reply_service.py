from data_.models import Vote, Reply
from data_.database import insert_query, read_query, update_query
from services import topic_service


def get_by_id(id):
    data = read_query('''
    SELECT id, date, content, likes_cnt, dislike_cnt, topic_id
    FROM reply
    WHERE id = ?''',
    (int(id),))

    return Reply.from_query_result(*data[0])


def create(reply, topic_id):

    topic = read_query('''
    SELECT id
    FROM topic
    WHERE id = ?''',
    (topic_id, ))

    if not topic:
        return None

    generated_id = insert_query('''
    INSERT INTO reply(date, content, topic_id)
    VALUES(?,?,?)''',
     (reply.cur_date, reply.content, topic_id[0][0]))

    reply.id = generated_id

    update_query('''
    UPDATE topic 
    SET last_reply = ?
    WHERE id = ?''',
    (reply.content, int(topic_id)))

    return {
        'content': reply.content,
        'date of publication': reply.cur_date.strftime('%d/%m/%Y'),
    }


def create_reply_response(reply):
    topic = topic_service.get_topic_by_id(reply.topic_id,cur_user=None) # трябва да има user

    return {
        'content': reply.content,
        'date of publication': reply.cur_date,
        'topic title': f'{topic['Topic'].title}'
    }


def create_vote(new_vote: Vote):
    generated_id = insert_query('''
        INSERT INTO vote(reply_id, user_id, vote)
        VALUES(?,?,?)''',
        (new_vote.reply_id, new_vote.users_id, new_vote.vote))

    return new_vote

def vote_change(new_vote:Vote, reply, cur_user):

    new_vote.reply_id = reply.id
    new_vote.users_id = cur_user.id

    vote_data = read_query('''
    SELECT reply_id, user_id, vote
    FROM vote
    WHERE reply_id = ? and user_id = ?''',
    (reply.id, cur_user.id))


    if not vote_data:
        create_vote(new_vote)

        if new_vote.vote == 1:
            reply.likes_cnt += 1
        else:
            reply.dislikes_cnt += 1

        result = 'like' if new_vote.vote == 1 else 'hate'
        vote_result = f'You {result} this reply!'

    else:

        reply_id, users_id, vote = vote_data[0]
        if vote == new_vote.vote:

            update_query('''
                DELETE vote
                FROM vote
                WHERE reply_id=? and user_id = ?''',
                (reply.id, cur_user.id))

            if new_vote.vote == 1:
                reply.likes_cnt -= 1
            else:
                reply.dislikes_cnt -= 1
            vote_result = 'You have deleted your vote!'


        elif new_vote.vote != vote:

            if new_vote.vote == 1:
                if not reply.dislikes_cnt == 0:
                    reply.dislikes_cnt -= 1
                reply.likes_cnt += 1

            elif new_vote.vote == 0:
                if not reply.likes_cnt == 0:
                    reply.likes_cnt -= 1
                reply.dislikes_cnt += 1

            update_query('''
               UPDATE vote
               SET vote =?
               WHERE reply_id = ? and  user_id = ?''',
                         (new_vote.vote, reply.id, cur_user.id))

            result = 'like' if new_vote.vote == 1 else 'hate'
            vote_result = f'You {result} this reply!'

    update_query('''
            UPDATE reply
            SET likes_cnt = ?, dislike_cnt = ?
            WHERE id = ?''',
            (reply.likes_cnt, reply.dislikes_cnt, reply.id))

    return vote_result



def get_category_id_from_reply(reply_id):

    data = read_query('''
    SELECT t.category_id
    FROM topic t 
    JOIN reply r
    WHERE r.id = ?  and t.id = r.topic_id''',
    (reply_id,))

    return data[0][0]















# def get_vote_by_reply_id(id):
#     data = read_query('''
#     SELECT reply_id, sender_id, vote
#     FROM vote
#     WHERE reply_id=?''',
#                (id, ))
#
#
#     return data[0]


# def vote_change(new_vote:Vote, reply, cur_user):
#
#     new_vote.reply_id = reply.id
#     new_vote.sender_id = cur_user.id
#
#     if new_vote.vote == 1:
#
#         if not reply.dislikes_cnt == 0:
#             reply.dislikes_cnt -= 1
#         reply.likes_cnt += 1
#
#         update_query('''
#         UPDATE reply
#         SET likes_cnt = ?''',
#         (reply.likes_cnt, ))
#
#     if new_vote.vote == 0:
#         if not reply.likes_cnt == 0:
#             reply.likes_cnt -= 1
#         reply.dislikes_cnt += 1
#         update_query('''
#         UPDATE reply
#         SET dislike_cnt = ?''',
#                  (reply.dislikes_cnt, ))
#
#     vote_result = 'like' if new_vote.vote == 1 else 'hate'
#     return f'You {vote_result} this reply!'