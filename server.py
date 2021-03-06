from tornado import web, ioloop

from app import Main, Delete, Add, Update


def make_app():
    return web.Application([
        (r'/', Main),
        (r'/delete-music/', Delete),
        (r'/add-music/', Add),
        (r'/update/', Update)
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    ioloop.IOLoop.current().start()
