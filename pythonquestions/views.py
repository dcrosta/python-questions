from flask import redirect

from pythonquestions import app, mongo


@app.route('/')
def sayit():
    return redirect('http://stackoverflow.com/questions/tagged/python', 307)

@app.route('/so/<int:question_id>')
def redirect_stackoverflow(question_id):
    mongo.db.questions.stackoverflow.find_one_or_404(question_id)
    return redirect('http://stackoverflow.com/questions/%s' % question_id, 301)

