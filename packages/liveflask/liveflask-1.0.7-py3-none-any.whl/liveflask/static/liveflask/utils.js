///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// UTILITIES
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

const MODIFIERS = [
    "defer",
    "lazy",
    "debounce"
];

const ATTRIBUTES = [
    "wire:model",
    "wire:poll",
    "wire:snapshot"
];

const print_ = console.log;


function createElementFromHTML(htmlString) {
    const parser = new DOMParser();
    const htmlDoc = parser.parseFromString(htmlString, 'text/xml');


    // Change this to div.childNodes to support multiple top-level nodes.
    return htmlDoc;
}

const attr_beginswith = (prefix, target, exclude_children = true) =>
    Array.from(target.querySelectorAll('*'))
        .filter(
            (e) => Array.from(e.attributes).filter(
                ({name, value}) => name.startsWith(prefix)).length
        );

function get_model_prop_value(el, attribute) {
    let property = el.getAttribute(attribute);
    let value = el.value;
    if (value === undefined) {
        value = el.innerHTML;
    }
    let modifier = "";
    if (property !== null) {

        if (property.split("|").length === 1) {

            return [property, modifier, value];
        }

        if (property.split("|").length === 2) {
            modifier = value.split("|")[0];
            value = value.split("|")[1];
            //console.log(property.split("|")[0], modifier, value)
            return [property, modifier, value];
        }
    }
}

const parse_model_attributes = el => {
    let property = el.getAttribute("data-model");
    return [];
};

function resolve(path, obj = self, separator = '.') {
    if (path.includes('undefined')) {
        path = path.split('.')[0];
    }
    let properties = Array.isArray(path) ? path : path.split(separator);
    let res = properties.reduce((prev, curr) => prev?.[curr], obj);
    if (typeof res === 'object') {
        return res[`${path.split('.')}`];
    } else {
        return res;
    }
}

function replace_undefined(item) {
    var str = JSON.stringify(item, function (key, value) {
            return (value === undefined || value.includes('.')) ? "" : value;
        }
    );
    return JSON.parse(str);
}

function parse_interval(str) {
    if (str === undefined) {
        return undefined;
    }
    if (str.slice(-2) === "ms") {
        return parseFloat(str.slice(0, -2)) || undefined;
    }
    if (str.slice(-1) === "s") {
        return (parseFloat(str.slice(0, -1)) * 1000) || undefined;
    }
    if (str.slice(-1) === "m") {
        return (parseFloat(str.slice(0, -1)) * 1000 * 60) || undefined;
    }
    return parseFloat(str) || undefined;
}

var debounce = (function () {
    var timers = {};

    return function (callback, delay, id) {
        delay = delay || 500;
        id = id || "duplicated event";

        if (timers[id]) {
            clearTimeout(timers[id]);
        }

        timers[id] = setTimeout(callback, delay);
    };
})(); // note the call here so the call for `func_to_param` is omitted


const debounceModel = _.debounce((el, payload) => {
    send_request(el, payload);
}, parse_interval('150ms'))


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// SERVER CALL
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function send_request(el, add_to_payload, target) {
    let updated_element;
    let emits;
    let snapshot = el.__liveflask
    let children = attr_beginswith('data-component', el);
    fetch("/liveflask/", {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRF-Token": csrfToken} ,
        body: JSON.stringify({
            snapshot: snapshot,
            ...add_to_payload
        })
    }).then(i => i.json()).then(response => {
        let {html, snapshot} = response
        el.__liveflask = snapshot
        el.__liveflask['children'] = children

        if (target.hasAttribute("data-poll") === true) {
            morphdom(target, createElementFromHTML(html).querySelector(`[data-poll=${target.getAttribute('data-poll')}]`).outerHTML)
            return;
        }

        update_dom(el, html)

        let emits = el.__liveflask?.data?.emits;

        if (emits !== undefined) {
            /* loop through the emits and fire the events */
            Object.keys(emits).forEach(event => {
                let current_event = emits[event]
                // Love this one console.log("Current Event: ", current_event)
                let event_name = current_event['event']
                let event_params = current_event['params']
                let kwargs = current_event['kwargs']
                let to = current_event['to']
                let final_params = event_name
                // Love this one console.log("Emitted Event: ", event_name, " with params: ", event_params, " to: ", to)
                document.dispatchEvent(new CustomEvent(event_name, {
                    detail: {
                        event: event_name,
                        params: event_params,
                        kwargs: kwargs,
                    }
                }));
                if (to === "self") {
                    send_request(el, {method: "emit", args: final_params, kwargs: kwargs}, target).then(() => {
                        // Update DOM synchronously after emitting events
                        update_dom(el, el.innerHTML);
                    });
                } else if (to === "all") {
                    let components = document.querySelectorAll(`[data-component]`)
                    components.forEach(component => {
                        // Love this one console.log("Emitting to all component - ", component, " with params: ", final_params)
                        send_request(component, {
                            method: "emit",
                            args: final_params,
                            kwargs: kwargs
                        }, target);
                    })
                } else {
                    let components = document.querySelectorAll(`[data-component=${to}]`)
                    components.forEach(component => {
                        send_request(component, {
                            method: "emit",
                            args: final_params,
                            kwargs: kwargs
                        }, target).then(() => {
                            // Update DOM synchronously after emitting events
                            update_dom(component, component.innerHTML);
                        });
                    })
                }

            })
        }

        // loop through el.__liveflask.data.url and update the page url with the new url
        let url_object = el.__liveflask?.data?.url;
        // url_object is a key-value pair object with key as the query parameter and value as the value
        if (url_object !== undefined) {
            let url = new URL(window.location.href);
            Object.keys(url_object).forEach(key => {
                url.searchParams.set(key, url_object[key]);
            });
            window.history.pushState({}, '', url);
        }

    }).then(el => {


    })
}


function update_dom(el, html) {
    let class_name = el.__liveflask['class']
    html = `<div data-component="${class_name}" id="${el.id}">${html}</div>`
    morphdom(el, html, {
        onBeforeElUpdated: function (fromEl, toEl) {
            // spec - https://dom.spec.whatwg.org/#concept-node-equals
            if (fromEl.isEqualNode(toEl)) {
                return false
            }
            return true
        },

        onElUpdated: function (element) {
            if (el.__liveflask['children'].length !== 0) {
                update_children(el.__liveflask['children'])
            }
        },

    });

    init_action(el)
}


function update_children(children = []) {
    let matched_component;
    children.forEach(i => {
        matched_component = document.getElementById(`${i.__liveflask['key']}`);
        morphdom(matched_component, i.outerHTML)
    })
}


