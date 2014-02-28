import webapp2, os, uuid, jinja2, json
from google.appengine.api import channel


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers.add_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.response.headers.add_header("Access-Control-Allow-Credentials", "true")
        self.response.headers.add_header("Access-Control-Allow-Headers", "origin, x-requested-with, content-type, accept")
        key = str(uuid.uuid4());
        token = channel.create_channel(key)
        template_values = {'token': token, 'key': key}
        template = jinja_environment.get_template('qrcode.html')
        self.response.out.write(template.render(template_values)) 

class Commands(webapp2.RequestHandler):
     
    def new(self):
        ret = {
            "err":False,
            "music_data": json.loads(self.music_data)
            }
        message = json.dumps(ret)
        channel.send_message(self.key, message)
        
        return json.dumps(ret)
            
    
    
    def post(self):
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers.add_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.response.headers.add_header("Access-Control-Allow-Credentials", "true")
        self.response.headers.add_header("Access-Control-Allow-Headers", "origin, x-requested-with, content-type, accept")
        self.response.headers.add_header('Content-Type', 'application/json')
        commands = {  
            "new": self.new,
        }
        self.key = self.request.get("k") if self.request.get("k") else ""
        self.music_data = self.request.get("md") if self.request.get("md") else ""
        self.command = self.request.get("command") if self.request.get("command") else ""
        self.response.out.write(commands[self.command]())
    
    def options(self):      
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers.add_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.response.headers.add_header("Access-Control-Allow-Credentials", "true")
        self.response.headers.add_header("Access-Control-Allow-Headers", "origin, x-requested-with, content-type, accept")
        self.response.headers.add_header('Content-Type', 'text/plain')
        self.response.out.write('Access-Control-Allow-Origin: *')

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/commands', Commands)
], debug=True)
