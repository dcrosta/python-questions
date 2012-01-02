from datetime import datetime, timedelta
from os.path import join
import pytz
import re

from pythonquestions import app, mongo
from pythonquestions.scripts import manager
from pythonquestions.lib.stackoverflow import get_questions_and_answers

def parse_timediff(diff):
    """
    Parse timedeltas in the form 'Nu' where N is some positive integer,
    and u is one of "s" (seconds), "m" (minutes), "h" (hours), "d"
    (days), or "w" (weeks).

    >>> parse_timediff('1d')
    datetime.timedelta(1)
    >>> parse_timediff('1h')
    datetime.timedelta(0, 3600)
    >>> parse_timediff('60s')
    datetime.timedelta(0, 60)
    >>> parse_timediff('3w')
    datetime.timedelta(21)
    """
    match = re.match(r'^(\d+)([smhdw])$', diff)
    if not match:
        raise Exception('Could not parse timediff "%s"' % diff)

    num, unit = match.groups()
    unit_to_kwarg = {
        's': 'seconds',
        'm': 'minutes',
        'h': 'hours',
        'd': 'days',
        'w': 'weeks',
    }
    kwargs = {unit_to_kwarg[unit]: int(num)}
    return timedelta(**kwargs)

@manager.command
@manager.option('-s', '--since', help='Get questions from SINCE to current time [1 day]')
def stackoverflow(since='1d'):
    mongo.db.questions.stackoverflow.ensure_index([('updated', -1)])

    fromdate = datetime.utcnow() - parse_timediff(since)
    fromdate = fromdate.replace(tzinfo=pytz.utc)

    tags = app.config.get('STACKOVERFLOW_TAGS', ['python'])
    questions = get_questions_and_answers(tags, fromdate=fromdate)
    count = 0
    for question in questions:
        doc = {
            'url': join('questions', str(question['question_id'])),
            'title': question['title'],
            'author': question['owner']['display_name'],
            'created': datetime.utcfromtimestamp(question['creation_date']),
            'updated': datetime.utcfromtimestamp(
                question.get('last_activity_date', question['creation_date'])),
        }

        mongo.db.questions.stackoverflow.update(
            {'_id': question['question_id']},
            {'$set': doc},
            upsert=True, safe=True)
        count += 1

    print "Synced", count, "questions"


if __name__ == '__main__':
    import doctest
    doctest.testmod()
