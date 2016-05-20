from keepasshttp import session


def start(appname):
    return session.Session.start(appname)
