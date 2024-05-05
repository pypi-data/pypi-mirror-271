import json
from typing import Any

from flask import render_template_string, session
from flask import request as req
from markupsafe import Markup

from ..utils import to_class


class HasRenders:
    def inital_render(self, component_name: str, *args, **kwargs):
        #print(f"Doing initial render {component_name}")
        # if key == "":
        #     key = f"mvlive_{component_name}_{secrets.token_urlsafe()}"
        component_name = component_name + "Component"
        _class: Any = to_class(f"templates.liveflask.{component_name}.{component_name}")
        component_instance = _class()
        component_name: str = _class.__name__

        # print("checking if key is sent via jinja funct")
        key = kwargs.get("key")
        if key:
            # print(f"key found ..... {key}")
            del kwargs["key"]
        else:
            key = getattr(component_instance, "key")
            # print(f"found key {key}")
            # print("Using generated key")
        setattr(component_instance, "key", key)

        # Get props from session
        for prop in component_instance.mvlive__session:
            setattr(
                component_instance,
                prop,
                session.get(
                    prop, getattr(component_instance, prop, None)
                )
            )

        for prop in component_instance.mvlive__url:
            if req.args.get(prop, None):
                setattr(
                    component_instance,
                    prop,
                    req.args.get(prop, None)
                )

        if hasattr(_class, 'boot'):
            component_instance.boot()

        if hasattr(_class, 'mount'):
            component_instance.mount(*args, **kwargs)

        if hasattr(_class, 'booted'):
            component_instance.booted()

        # set_attribute(component_instance, 'key', key)
        html, snapshot = self.to_snapshot(component_instance)
        snapshot_attr: str = json.dumps(snapshot)

        #print(f"Snapshot: {snapshot}")

        return Markup(
            render_template_string(
                """
                    <div data-component="{{ component_name }}" id="{{ key }}" data-snapshot="{{ snapshot_attr }}">
                        {{html|safe}}
                    </div>
                """, snapshot_attr=snapshot_attr, html=html, key=key, component_name=component_name
            )
        )
