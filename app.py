#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
from maps import *
from bar import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/search')
def search():
    form = LoginForm(request.form)
    return render_template('forms/search.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)

@app.route('/cluster')
def cluster():
    form = ClusterForm(request.form)
    return render_template('forms/search_cluster.html', form = form)


@app.route('/cluster/results', methods = ['POST'])
def output_clusters():
    input1 = request.form['name']
    run_BarCluster(input1)
    return render_template('pages/results_cluster.html')

@app.route('/recurse',methods = ['GET','POST'])
def recurse():
    try:
        for i in xrange(1,5):
            inp = request.form.getlist(str(i))

            if inp == []:
                continue
            inp = str(inp[0][1:-1])
            inp = inp.replace('\'', '')
            inp = inp.split(',')
            #input1,input2,input3,input4 = inp
            #inp = inp[]
            break 
        run_recurse(inp)
    except:
        return render_template('pages/results_cluster.html')        
    return render_template('pages/results_cluster.html')

@app.route('/search/results', methods = ['POST'])
def output_results():
    input1 = request.form['name']
    input2 = request.form['hours']
    input3 = request.form['track']
    input4 = request.form['transport']
    run_CookATour(input1,input2,input3, input4)
    return render_template('pages/results.html')


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    global feature_vector
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
