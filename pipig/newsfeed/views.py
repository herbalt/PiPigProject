from flask import render_template, flash, redirect

import config
from forms import LoginForm
from run import app


def view_index():
    """

    :return:
    """
    user = {'nickname': 'Tim'}  # fake user
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/')
@app.route('/index')
def ctrl_index():
    return view_index()