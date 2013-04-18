import cherrypy
import spwd, crypt, getpass, pwd

class Login:
    
    _cp_config = {'tools.sessions.on': True}
    
    def verif(self,login,passwd):
        try :
            cryptedpasswd = pwd.getpwnam(login)[1]
            if cryptedpasswd:
                if cryptedpasswd == 'x' or cryptedpasswd == '*':
                     cryptedpasswd = spwd.getspnam(login)[1]
                return crypt.crypt(passwd, cryptedpasswd) == cryptedpasswd
            else:
                return 1
        except KeyError:
            print "error"

    def index(self,login,passwd):
	if self.verif(login,passwd):
	    cherrypy.session['login'] = login
	    return "ok"
	else:
            return "not ok"

    def logout(self):
       cherrypy.lib.sessions.expire()
       return "ok"

    index.exposed = True
    logout.exposed = True
import os.path
tutconf = os.path.join(os.path.dirname(__file__), 'tutorial.conf')

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    cherrypy.quickstart(Login(), config=tutconf)
else:
    # This branch is for the test suite; you can ignore it.
    cherrypy.tree.mount(Login(), config=tutconf)

