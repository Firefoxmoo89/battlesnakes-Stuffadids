import os
import random
import cherrypy

class Battlesnake(object):
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def index(self):
		return {
		"apiversion": "1",
		"author": "firefoxmoo",
		"color": "#4B8B48",  
		"head": "evil",  
		"tail": "bolt"}

	@cherrypy.expose
	@cherrypy.tools.json_in()
	def start(self):
		data = cherrypy.request.json
		with open('gameplay.txt', 'w') as file:
			file.write('##### Starting Game! #####\n')
		with open('teststuff.txt', 'w') as file:
			file.write('##### Starting Game! #####\n')
		return "ok"

	@cherrypy.expose
	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()
	def move(self):
		from move import move
		data = cherrypy.request.json
		decision = move(self,data)
		return decision

	@cherrypy.expose
	@cherrypy.tools.json_in()
	def end(self):
		data = cherrypy.request.json

		print("END")
		with open('gameplay.txt', 'a') as file:
			file.write('##### It\'s over! #####\n')
		with open('teststuff.txt', 'a') as file:
			file.write('##### It\'s over! #####\n')
		return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
