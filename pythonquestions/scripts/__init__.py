__all__ = ('manager',)

from pythonquestions import app
from flask.ext.script import Manager

manager = Manager(app)

# TODO: can we magically import modules?
import pythonquestions.scripts.stackoverflow
import pythonquestions.scripts.tweet

