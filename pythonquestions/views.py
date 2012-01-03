from flask import redirect

from pythonquestions import app, mongo


@app.route('/')
def sayit():
    return redirect('http://stackoverflow.com/questions/tagged/python', 307)

@app.route('/so/<int:question_id>')
def redirect_stackoverflow(question_id):
    question = mongo.db.questions.stackoverflow.find_one_or_404(question_id)
    mongo.db.questions.stackoverflow.update(
        {'_id': question['_id']},
        {'$inc': {'clicks': 1}},
        safe=False)
    return redirect('http://stackoverflow.com/questions/%s' % question_id, 301)

