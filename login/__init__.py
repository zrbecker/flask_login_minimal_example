import flask
import flask_login

app = flask.Flask(__name__)
app.secret_key = 'development secret'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Mock Database
users = {'foo@bar.tld': {'pw': 'secret'}}

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    print('USER_LOADER')
    if email not in users:
        return
    user = User()
    user.id = email
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
            <form action="login" method="POST">
              <input type="text" name="email" id="email" placeholder="email">
              <input type="password" name="pw" id="pw" placeholder="password">
              <button type="submit">Submit</button>
            </form>
        '''
    
    email = flask.request.form['email']
    if flask.request.form['pw'] == users[email]['pw']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'
