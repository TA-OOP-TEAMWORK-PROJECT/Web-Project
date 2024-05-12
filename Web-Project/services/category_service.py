from fastapi import Response, HTTPException
from data_.models import Category, Topic, User, CategoryAccess, Role
from data_.database import read_query, insert_query, update_query
from services.users_service import users_access_state


def get_all_categories(user):
    data = read_query('''SELECT id, title, description, last_topic, topic_cnt, is_private, is_locked
         FROM category''')

    result = (Category.from_query_result(*row) for row in data)

    if result is not None:
        return get_category_response(user, result)


def create(category):

    generated_id = insert_query('''
    INSERT INTO category(title, description)
    VALUES(?,?)''',
    (category.title, category.description))

    category.id = generated_id
    return f'Category with title {category.title} was created successfully!'


def get_topics_for_category(user_id: int, category_id: int, search: str = None, sort_by: str = None,
                            page: int = 1, limit: int = 10, is_admin: bool = False):
    category = read_query(
        "SELECT is_private FROM category WHERE id = ?",
        (category_id,)
    )

    if category:
        is_private = category[0][0]

        if not is_private or is_admin:
            return fetch_all_topics_for_category(category_id, search, sort_by, page, limit)
        else:
            if check_category_read_access(user_id, category_id):
                return fetch_all_topics_for_category(category_id, search, sort_by, page, limit)
            else:
                raise HTTPException(status_code=403, detail="Access denied")

    raise HTTPException(status_code=404, detail="Category not found")


def fetch_all_topics_for_category(category_id: int, search: str, sort_by: str, page: int, limit: int):

    sql = 'SELECT id, title, date, last_reply, user_id, category_id, is_locked FROM topic WHERE category_id = %s'
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


def user_access_state(visibility, category_id):

    update_query('''
    UPDATE category
    SET is_private = ?
    WHERE id = ? ''',
    (visibility.visibility, category_id))

    if visibility.visibility == 1:
        return 'Category is changed to private'
    return 'Category can be seen from all users'


def get_category_by_id(id):
    data = read_query(
        '''SELECT id, title, description, last_topic, topic_cnt, is_private, is_locked
        FROM category WHERE id = ?''',
        (id,))


    category = next((Category.from_query_result(*row) for row in data), None)
    return category


def get_user_access_state(user: User):
    data = read_query('''
    SELECT user_id, category_id, can_read, can_write
    FROM category_access
    WHERE users_id = ?''',
    (user.id, ))

    return CategoryAccess.from_query_result(*data[0])


def get_category_response(user, category):

    cat_dict = {}
    for cat in category:

        is_category = category_is_private(cat.id)

        if is_category:

            user_access = users_access_state(user.id, cat.id)
            if not user_access:
                continue
        cat_dict[f'Category name: {cat.title}'] = {

            "Category title": cat.title,
            "Description": cat.description,
            "Number of topics in category": cat.topic_cnt,
            "Last topic is:": cat.last_topic
                                        }

    return cat_dict


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
    return {"message": f"Read access granted to user {user_id}."}


def check_category_read_access(user_id: int, category_id: int):
    access = read_query(
        "SELECT can_read FROM category_access WHERE user_id = ? AND category_id = ?",
        (user_id, category_id)
    )
    return access and access[0][0]


def grant_category_write_access(user_id: int, category_id: int):
    existing_access = read_query(
        "SELECT 1 FROM category_access WHERE user_id = ? AND category_id = ?",
        (user_id, category_id)
    )
    if existing_access:
        update_query(
            "UPDATE category_access SET can_read = TRUE, can_write = TRUE WHERE user_id = ? AND category_id = ?",
            (user_id, category_id)
        )
    else:
        insert_query(
            "INSERT INTO category_access (user_id, category_id, can_read, can_write) VALUES (?, ?, TRUE, TRUE)",
            (user_id, category_id)
        )
    return {"message": f"Read & write access granted to user {user_id}."}


def revoke_category_read_or_write_access(user_id: int, category_id: int, revoke_read: bool, revoke_write: bool):
    current_access = read_query(
        "SELECT can_read, can_write FROM category_access WHERE user_id = ? AND category_id = ?",
        (user_id, category_id)
    )

    if current_access:
        can_read, can_write = current_access[0]

        new_can_read = can_read and not revoke_read
        new_can_write = can_write and not revoke_write

        if not new_can_read:          ### Updated
            update_query(
                "DELETE FROM category_access WHERE user_id = ? AND category_id = ?",
                (user_id, category_id)
            )
            return {"message": "User removed completely from the category."}

        elif can_read != new_can_read or can_write != new_can_write:
            update_query(
                "UPDATE category_access SET can_read = ?, can_write = ? WHERE user_id = ? AND category_id = ?",
                (new_can_read, new_can_write, user_id, category_id)
            )
            return {"message": "Access rights updated successfully."}
    else:
        return {"message": "User has no access. No changes made."}

    return {"message": "No changes required based on current access rights."}


def get_privileged_users(category_id: int):
    is_private = read_query(
        "SELECT is_private FROM category WHERE id = ?",
        (category_id,)
    )

    if not is_private or not is_private[0][0]:
        return None, "Category is not private or does not exist."

    users_access = read_query(
        """
        SELECT users.username, category_access.can_read, category_access.can_write
        FROM users
        JOIN category_access ON users.id = category_access.user_id
        WHERE category_access.category_id = ?
        """,
        (category_id,)
    )

    access_list = [
        {"username": user[0], "can_read": user[1], "can_write": user[2]}
        for user in users_access
    ]
    return access_list


def lock(category_id, current_user): #да проверя дали вече не е заключена?

    if not current_user.role == 'admin':
        return Response(status_code=401, content='You are not authorized!')

    update_query('''
    Update category
    SET is_locked = 1
    WHERE id = ?''',
    (category_id, ))

    return 'Category has been locked!'


def category_is_private(category_id):

    category_data = read_query(
        '''SELECT is_private
        FROM category 
        WHERE id = ?''',
        (category_id,))

    if category_data[0][0] == 0:
        return False
    return True










