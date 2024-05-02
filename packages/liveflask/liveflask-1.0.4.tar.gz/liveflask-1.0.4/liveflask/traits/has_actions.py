from typing import Any, NoReturn

from flask import session
from ..traits.Bootable import Bootable
from ..utils import dict_diff_changed_values


class HasActions:
    def call_method(self, component: Any, method: str, *args) -> NoReturn:
        props = self.get_props(component)
        Bootable.init_bootable_hook(_class=component)

        if "__NOVAL__" in args:
            args: tuple | list = ()

        # Perform action then get new props
        getattr(component, method)(*args)
        new_props = self.get_props(component)
        for item in dict_diff_changed_values(props, new_props):
            self.set_props(component, item, new_props.get(item))
            session[item] = new_props.get(item)
        #print(new_props, ":::::::::::::::::::::")
        return component

    def call_event_handler(self, component: Any, parsed_method: str, *args, **kwargs):
        """
        Call the event handler method on the component with given arguments and keyword arguments.

        Args:
            component (Any): The component object.
            parsed_method (str): The parsed method name.
            *args: Positional arguments to pass to the event handler method.
            **kwargs: Keyword arguments to pass to the event handler method.

        Returns:
            Any: The modified component object.
        """
        props: dict[str, Any] = self.get_props(component)
        Bootable.init_bootable_hook(_class=component)

        if 'listeners' in props:
            event: str = args[0]
            args = args[1:]
            listener_method = props['listeners'].get(event)
            if listener_method:
                getattr(component, listener_method)(*args, **kwargs)
                # Remove the event from emits
                component.emits = [emit for emit in component.emits if emit['event'] != event]
            else:
                component.emits = [emit for emit in component.emits if emit['event'] != event]

        return component