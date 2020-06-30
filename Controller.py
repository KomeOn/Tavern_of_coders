import web
from Models import RegisterModel, LoginModel, Posts
import os

web.config.debug = False

urls = (
    '/profile/(.*)/about', 'UserAbout',
    '/profile/(.*)', 'UserProfile',
    '/update-settings', 'UpdateSettings',
    '/settings', 'UserSettings',
    '/register', 'Register',
    '/login', 'Login',
    '/logout', 'Logout',
    '/check-login', 'CheckLogin',
    '/postregistration', 'PostRegistration',
    '/post-activity', 'PostActivity',
    '/', 'Home',
    '/submit-comment', "SubmitComment",
    '/upload-image/(.*)', "UploadImage"
)

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore("sessions"), initializer={'user': None})
session_data = session._initializer

render = web.template.render("Views/Templates", base="MainLayout",
                             globals={'session': session_data, 'current_user': session_data['user']})


# Classes/Routes

class Home:
    def GET(self):   
        post_model = Posts.Posts()
        posts = post_model.get_all_posts()

        return render.Home(posts)


class UserProfile:
    def GET(self, user):
        post_model = Posts.Posts()
        posts = post_model.get_user_posts(user)

        login = LoginModel.LoginModel()
        user_info = login.get_profile(user)

        return render.Profile(posts, user_info)


class UserSettings:
    def GET(self):
        return render.Settings()


class UpdateSettings:
    def POST(self):
        data = web.input()
        data.username = session_data['user']['username']

        settings_model = LoginModel.LoginModel()
        if settings_model.update_info(data):
            return 'success'
        else:
            return 'Fatal error'


class Register:
    def GET(self):
        return render.Register()


class Login:
    def GET(self):
        log = LoginModel.LoginModel()
        images = log.get_image("login")
        return render.Login(images)


class PostRegistration:
    def POST(self):
        data = web.input()
        print("data:", data)
        reg_model = RegisterModel.RegisterModel()
        reg_model.insert_user(data)
        return data


class CheckLogin:
    def POST(self):
        data = web.input()
        login = LoginModel.LoginModel()
        isCorrect = login.check_user(data)

        if isCorrect:
            session_data['user'] = isCorrect
            return isCorrect

        return "error"


class Logout:
    def GET(self):
        session['user'] = None
        session_data['user'] = None
        session.kill()
        return "success"


class PostActivity:
    def POST(self):
        data = web.input()
        data.username = session_data['user']['username']

        post_model = Posts.Posts()
        post_model.insert_posts(data)

        return 'success'

class UserAbout:
    def GET(self, user):
        login = LoginModel.LoginModel()
        user_info = login.get_profile(user)
        
        return render.About(user_info)

class SubmitComment:
    def POST(self):
        data = web.input()
        data.username = session_data['user']['username']

        post_model = Posts.Posts()
        added_comment = post_model.add_comment(data)

        if added_comment:
            return added_comment
        else:
            return {'error': '403'}

class UploadImage:
    def POST(self, categor):
        file = web.input(avatar={}, background={})
        file_dir = os.getcwd() + "/static/uploads/" + session_data['user']['username']

        if not os.path.exists(file_dir):
            os.mkdir(file_dir)


        if "avatar" or "background" in file:
            filepath = file[categor].filename.replace("\\", "/")
            filename = filepath.split('/')[-1]
            f = open(file_dir + '/' + filename, "wb")
            f.write(file[categor].file.read())
            f.close()

            update = {}
            update['type'] = categor
            update['img'] = '/static/uploads/' + session_data['user']['username'] + '/' + filename
            update['username'] = session_data['user']['username']

            account_model = LoginModel.LoginModel()
            update_img = account_model.update_image(update)

        raise web.seeother("/settings")

'''class UploadImage:
    def POST(self, categor):
        file = web.input(login={}, register={})
        file_dir = os.getcwd() + '/source/images/' + categor 
        print("sd:", file_dir)

        if not os.path.exists(file_dir):
            os.mkdir(file_dir)

        if "login" or "register" in file:
            filepath = file[categor].filename.replace("\\", "/")
            filename = filepath.split('/')[-1]
            f = open(file_dir + '/' + filename, "wb")
            f.write(file[categor].file.read())
            f.close()

        update = {}
        update['type'] = categor
        update['img'] = '/sources/images/' + categor + '/' + filename
        update['username'] = session_data['user']['username']

        account_model = LoginModel.LoginModel()
        update_img = account_model.update_image(update)'''


if __name__ == "__main__":
    app.run()
