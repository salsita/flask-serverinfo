"""Flask server info view for inspecting server app and user requests."""

__all__ = 'setup view dumps logging_info logger_info server_info JSONEncoder'.split()
__version__ = '0.1.0'

import flask
from flask import json, Flask, Request, Response
from logging import Logger, getLogger, root
from werkzeug.local import LocalProxy
from werkzeug.routing import Map
from werkzeug.datastructures import MultiDict, Headers

class JSONEncoder(json.JSONEncoder):
    base_types = (basestring, int, float, bool, type(None))
    iter_types = (dict, tuple, list, set)
    inspect_types = (LocalProxy, Flask, Map, Request, Response)

    def default(self, o):
        if isinstance(o, self.inspect_types):
            return dict((k, getattr(o, k)) for k in dir(o) if not isinstance(k, basestring) or not k.startswith('__'))
        elif isinstance(o, MultiDict):
            return o.lists()
        elif isinstance(o, Headers):
            return o.items()
        elif isinstance(o, Logger):
            return logger_info(o)

        try:
            return super(JSONEncoder, self).default(o)
        except TypeError:
            return '{} {!r}'.format(type(o), o)

    def iterencode(self, o, _one_shot=False):
        o = self.replace_circular_refs(o)
        try:
            for chunk in super(JSONEncoder, self).iterencode(o, _one_shot):
                yield chunk
        except ValueError as error:
            yield '"{}: {} {!r}"'.format(error, type(o), o)

    def replace_circular_refs(self, o, path='', cache=None):
        if cache is None:
            cache = {}
        if not isinstance(o, self.base_types):
            if not isinstance(o, self.iter_types):
                return self.replace_circular_refs(self.default(o), path, cache)
            o = (dict if isinstance(o, dict) else list)(o)
            for key, value in (o.iteritems() if isinstance(o, dict) else enumerate(o)):
                if not isinstance(value, self.base_types):
                    if id(value) in cache:
                        o[key] = '<$ref: {}>'.format(cache[id(value)])
                    else:
                        cache[id(value)] = '{}{}'.format(path, key)
                        o[key] = self.replace_circular_refs(value, '{}{}.'.format(path, key), cache)
        return o

DUMP_OPTIONS = dict(
    indent = 2,
    sort_keys = True,
    cls = JSONEncoder,
    )

def dumps(data, **options):
    options = dict(DUMP_OPTIONS, **options)
    return json.dumps(data, **options)

def logging_info(*additional_logger_names):
    return [logger_info(getLogger(name)) for name in
        ['root'] + list(additional_logger_names) + sorted(root.manager.loggerDict.keys())]

def logger_info(l):
    p = l.parent or l
    return '<Logger> [%02d/%02d] %01d%1s %s' % (
        l.level, l.getEffectiveLevel(), len(l.handlers),
        '+' if l.propagate else '',
        l.name if p is l or l.name.startswith(p.name + '.') else p.name + ' :: ' + l.name,
        )

def server_info(app=None, *additional_logger_names):
    return dict(
        app = app or flask.current_app,
        logging = logging_info(*additional_logger_names),
        )

def view():
    return Response(dumps(dict(
        request = flask.request,
        response = Response(mimetype = 'application/json'),
        server = server_info(),
        )),
        mimetype = 'application/json',
        )

def setup(app, uri, endpoint='serverinfo_view', **options):
    app.route(uri, endpoint=endpoint, **options)(view)
