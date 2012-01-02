__all__ = ('get_questions_and_answers', )

from datetime import datetime
import json
import pytz
import requests
import time

from pythonquestions import app

api_key = app.config.get('STACKOVERFLOW_API_KEY', '')

def req(tags, pagesize=100, pagenum=1, sort='activity', fromdate=None, todate=None):
    url = 'http://api.stackoverflow.com/1.1/questions?'
    params = dict(
        tagged=';'.join(tags),
        page=pagenum,
        pagesize=pagesize,
        key=api_key,
        sort=sort,
        # body='true',
        # answers='true',
    )
    if fromdate:
        if type(fromdate) == datetime:
            tm = fromdate.astimezone(pytz.utc).timetuple()
            fromdate = time.mktime(tm)
        params['fromdate'] = int(fromdate)
    if todate:
        if type(todate) == datetime:
            tm = todate.astimezone(pytz.utc).timetuple()
            todate = time.mktime(tm)
        params['todate'] = int(todate)

    response = requests.get(url, params=params)
    body = json.loads(response.content)
    return body

def get_questions_and_answers(tags, fromdate=None, todate=None):
    if type(tags) in (str, unicode):
        tags = [tags]

    pagenum = 1
    questions = []
    question_ids = set()

    while True:
        response = req(tags, pagenum=pagenum, fromdate=fromdate, todate=todate)
        pagenum += 1

        num_added = 0
        for question in response['questions']:
            # skip duplicates
            if question['question_id'] not in question_ids:
                question_ids.add(question['question_id'])
                questions.append(question)
                num_added += 1

        if num_added == 0:
            break

    return questions

