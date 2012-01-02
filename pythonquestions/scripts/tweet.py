from pythonquestions import mongo, twitter
from pythonquestions.scripts import manager


@manager.command
def tweet(since='1d'):
    mongo.db.questions.stackoverflow.ensure_index([('tweeted', 1)])

    cursor = mongo.db.questions.stackoverflow.find({'tweeted': {'$exists': False}})
    for question in list(cursor):
        url = 'http://pyq.io/so/%s' % question['_id']
        title = question['title']
        remaining = 140 - len(url) - len('#python') - 2
        if len(title) > remaining:
            title = title[:len(remaining)-2]
            title = title[:title.rfind(' ')]
            title = '%s...' % title
        tweet = '%s %s %s' % (title, url, '#python')
        twitter.api.update_status(tweet)

        mongo.db.questions.stackoverflow.update(
            {'_id': question['_id']},
            {'$set': {'tweeted': True}},
            safe=True)

        break

    print "Synced", count, "questions"


if __name__ == '__main__':
    import doctest
    doctest.testmod()