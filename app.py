import urllib
from tornado import web, websocket, ioloop
from sqlalchemy.orm import sessionmaker
from tornado.websocket import WebSocketClosedError

from db import engine, Music


class Main(web.RequestHandler):

	def get(self):
		session = sessionmaker(bind=engine)()
		content = {
			'music': session.query(Music).all(), 
			'error': False
		}
		self.render('templates/index.html', **content)


class Delete(web.RequestHandler):

	def post(self):
		session = sessionmaker(bind=engine)()
		treck = session.query(Music).filter_by(
            id = int(self.get_body_argument('id'))
        ).first()
		session.delete(treck)
		session.commit()

		Update.send_message(
            	self.render_string('templates/music-list.html', **{'music': session.query(Music).all()})
        )
        
		self.redirect('/')


class Add(web.RequestHandler):

	def post(self):
		name = self.get_body_argument('name')
		autor = self.get_body_argument('autor')
		minutes = self.get_body_argument('min')
		seconds = self.get_body_argument('sec')

		if (len(autor.replace(" ", "")) != 0 
		and len(name.replace(" ", "")) != 0 
		and minutes.isdigit() 
		and seconds.isdigit() 
		and 0 <= int(minutes) <= 180 
		and 0 <= int(seconds) <= 59):

			if len("0" + minutes) == 2:
				minutes = "0" + minutes

			if len("0" + seconds) == 2:
				seconds = "0" + seconds

			session = sessionmaker(bind=engine)()
			session.add(Music(
	            name = name,
	            autor = autor,
	            len = minutes + ":" + seconds
	        ))
			session.commit()

			Update.send_message(
            	self.render_string('templates/music-list.html', **{'music': session.query(Music).all()})
        	)

			self.redirect('/')

		else:
			session = sessionmaker(bind=engine)()
			content = {
						'music': session.query(Music).all(), 
						'error': True
					}

			self.render('templates/index.html', **content)


class Update(websocket.WebSocketHandler):
    clients = []

    def open(self, *args: str, **kwargs: str):
        Update.clients.append(self)
        super(Update, self).open(*args, **kwargs)

    def close(self, code=None, reason=None):
        Update.clients.remove(self)

    @classmethod
    def send_message(cls, message):
        for client in cls.clients:

            try:
                client.write_message(message)
            except WebSocketClosedError:
                pass
