import ast
import functools
import os
import secrets
import gzip
from flask import Blueprint, render_template, Response, Flask
from flask import request
from markupsafe import Markup
from flask_wtf import CSRFProtect
from .traits.has_actions import HasActions
from .traits.has_props import HasProps
from .traits.has_renders import HasRenders
from .traits.has_snapshots import HasSnapshots


def parse_argument(arg):
    try:
        return ast.literal_eval(arg)
    except (SyntaxError, ValueError):
        # If the literal is not valid, return the string itself
        return arg


def parse_arguments(args_str):
    # Remove leading/trailing whitespaces and parentheses if any
    args_str = args_str.strip("[]{}()")
    # Split arguments by comma
    args_list = args_str.split(",")
    # Parse each argument
    parsed_args = [parse_argument(arg.strip()) for arg in args_list]
    return parsed_args


def return_arguments(*args_str):
    if len(args_str) == 1 and args_str[0] == "__NOVAL__":
        return ()
    if len(args_str) == 1 and args_str[0] != "__NOVAL__":
        return (parse_argument(args_str[0]),)
    return tuple(parse_arguments(arg_str) for arg_str in args_str)


def component(cls) -> 'cls':
    @functools.wraps(cls, updated=())
    class DecoratedClass(cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.__class__.__name__ = cls.__name__
            cls.key = f"mvlive_{cls.__name__.lower()}_{secrets.token_urlsafe(4)}"
            cls.emits = []

            def emit_to_self(self, event: str, *args, **kwargs):
                self.emits.append({
                    "event": event,
                    "params": args,
                    "kwargs": kwargs,
                    "to": "self"
                })

            def emit_to(self, component: str, event: str, *args, **kwargs):
                self.emits.append({
                    "event": event,
                    "params": args,
                    "kwargs": kwargs,
                    "to": component
                })

            def emit(self, event: str, *args, **kwargs):
                self.emits.append({
                    "event": event,
                    "params": args,
                    "kwargs": kwargs,
                    "to": "all"
                })

            cls.emit_to_self = emit_to_self
            cls.emit_to = emit_to
            cls.emit = emit
            cls.mvlive__locked = []
            cls.mvlive__session = []
            cls.mvlive__url = []

    DecoratedClass.__name__ = cls.__name__
    return DecoratedClass


class LiveFlask(HasRenders, HasProps, HasSnapshots, HasActions):
    pass


def LiveFlaskExt(app: Flask):
    app.add_template_global(
        LiveFlask().inital_render, 'live'
    )

    if "csrf" not in list(app.extensions.keys()):
        # register CSRF protection
        csrf = CSRFProtect(app)


    package_dir = os.path.dirname(os.path.abspath(__file__))
    enduser_project_dir = os.getcwd()
    # check if the project directory has a templates folder
    if not os.path.exists(f"{enduser_project_dir}/templates"):
        os.makedirs(f"{enduser_project_dir}/templates")

    # check if the templates folder has a liveflask folder
    if not os.path.exists(f"{enduser_project_dir}/templates/liveflask"):
        os.makedirs(f"{enduser_project_dir}/templates/liveflask")

    liveflask_bp = Blueprint('live', __name__, static_folder='static',
                             template_folder='templates')

    @liveflask_bp.post('/')
    def live():
        req = request.json
        _class: object = LiveFlask().from_snapshot(req)

        if req.get('method'):
            method = req.get('method')
            args = req.get('args')
            kwargs = req.get('kwargs') or {}
            if method == "emit":
                component = LiveFlask().call_event_handler(_class, method, *return_arguments(args), **kwargs)
            elif method == "emit_to":
                component = LiveFlask().call_event_handler(_class, method, *return_arguments(args), **kwargs)
            else:
                component = LiveFlask().call_method(_class, method, *return_arguments(args))

        if req.get('update_property'):
            req_updated_prop = req.get('update_property')
            LiveFlask().set_props(_class, req_updated_prop[0], req_updated_prop[1])
            component = _class

        LiveFlask().set_props(_class, 'emits', _class.emits)
        component = _class

        html, snapshot = LiveFlask().to_snapshot(component)
        return {
            "html": html, "snapshot": snapshot
        }

    @liveflask_bp.route('/bundle.js')
    def bundle_js():
        js_files = [
            # 'liveflask.js',
            'utils.js',
            'model.js',
            'action.js',
            'polling.js',
            'events.js'
        ]
        combined_js = ''
        for js_file in js_files:
            with open(f'{package_dir}/static/liveflask/{js_file}', 'r') as f:
                combined_js += f.read()
        resp = Response(
            gzip.compress(combined_js.encode('utf-8'))
        )
        resp.headers['Content-Encoding'] = 'gzip'
        resp.mimetype = 'application/javascript'
        resp.headers['Cache-Control'] = 'public, max-age=3600'
        return resp

    @liveflask_bp.route("/liveflask.js")
    def liveflask_js():
        combined_js = ''
        # serve liveflask.js from static directory with the mimetype of 'application/javascript'
        with open(f'{package_dir}/static/liveflask/liveflask.js', 'r') as f:
            combined_js += f.read()
        resp = Response(
            gzip.compress(combined_js.encode('utf-8'))
        )
        resp.headers['Content-Encoding'] = 'gzip'
        resp.mimetype = 'application/javascript'
        resp.headers['Cache-Control'] = 'public, max-age=3600'

        return resp

    @app.template_global()
    def liveflask_scripts():
        return Markup(render_template("liveflask-scripts.html"))

    app.register_blueprint(liveflask_bp, url_prefix='/liveflask')
    return app
