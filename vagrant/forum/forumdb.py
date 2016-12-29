#
# Database access functions for the web forum.
# 
import psycopg2
import time
import bleach
# import logging

## Database connection
# DB = []




## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    pg = psycopg2.connect("dbname = forum")
    cursor = pg.cursor()
    cursor.execute("select * from posts")
    DB = cursor.fetchall()
    pg.close()
    posts = [{'content': str(bleach.clean(row[0])), 'time': row[1]} for row in DB]
    posts.sort(key=lambda row: row['time'], reverse=True)
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    pg = psycopg2.connect("dbname = forum")
    cursor = pg.cursor()
    t = time.strftime('%c', time.localtime())
    cursor.execute("insert into posts (content) values (%s)",(content,))
    pg.commit()
    pg.close()
    # DB.append((t, content))
