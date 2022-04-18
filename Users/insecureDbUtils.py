

from sqlite3 import Timestamp
"""
All these queries are compatable with sqlite
"""

def loginQuery(username,password):
    query =  f'''SELECT * FROM Users_user WHERE username="{username}" AND password="{password}"'''
    return query

def registerQuery(username,email,fn,ln,password,ts):
    query = f'''INSERT INTO Users_user(username,email,first_name,last_name,password,is_superuser,is_staff,is_active,date_joined) VALUES("{username}","{email}","{fn}","{ln}","{password}",0,0,1,"{ts}");'''
    return query

def projectQuery(title,description,link,user,type):
    user_id = user.id
    query = f'''INSERT INTO Users_projects(title,description,link,user_id,type) VALUES("{title}","{description}","{link}",{user_id},"{type}");'''
    return query


def getProjects(project):
    if len(project) == 0:
        query = f'''SELECT * FROM Users_projects WHERE type="Public";'''
        return query
    query = f'''SELECT * FROM Users_projects WHERE title like "%{project}%" AND type="Public";'''
    return query


# not being used 
def SearchQuery(user,project):
    if len(project) == 0: 
        if len(user) == 0: # no project and no user
            query = f'''SELECT * FROM Users_projects WHERE type="Public";'''
            return query
        else: # no project but user 
            query = f'''SELECT A.title,A.description,A.link,A.user_id FROM Users_projects AS A,Users_user AS U  WHERE U.id == A.user_id and U.username like "%{user}%" AND A.type="Public";'''
            return query
    if len(user) == 0: # no user but project
        if len(project) == 0:
            query = f'''SELECT * FROM Users_projects WHERE type="Public";'''
            return query
        else:
            query = f'''SELECT * FROM Users_projects WHERE title like "%{project}%" AND type="Public";'''
            return query
    else: # both user and project
        query = f'''SELECT A.title,A.description,A.link,A.user_id FROM Users_projects AS A,Users_user AS U  WHERE A.title like "%{project}%" AND U.id == A.user_id and U.username like "%{user}%" AND A.type="Public";'''
        return query

