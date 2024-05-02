


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// INITIALIZERS
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
document.querySelectorAll('[data-component]').forEach(el => {
    let live_flask_children = [];

    el.__liveflask = JSON.parse(el.getAttribute('data-snapshot'));
    el.removeAttribute('data-snapshot')


    init_model(el)
    init_action(el)
    init_polling(el)

    el.__liveflask.set = function (key, value) {
        el.__liveflask[key] = value
        send_request(el, {update_property: [key, value]}, undefined)
    }

    // register event named liveflask:initialized
    document.dispatchEvent(new CustomEvent('liveflask:initialized', {detail: el.__liveflask, target: el}))

})