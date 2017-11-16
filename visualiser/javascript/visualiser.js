define('health-watch-visualiser',
['module_struct', 'el/el', 'presenter/presenter', 'util/util', 'worker'],
function(module, el, presenter, util, worker) {
'use strict';
var $p = el.runtime.wrap_proxy, $$p = el.runtime.unwrap_proxy;

function VisualiserControllerImpl(worker_url) {
    this.json_decode_worker = worker(worker_url);
    this.model = {
        graph: {
            width: 500,
            height: 400
        }
    };
    var context = new el.shadow.ShadowContext;
    var scope = new el.scope.Scope({});
    el.shadow.object(new Map([
        ['data', el.shadow.value(context, scope, x => x)]
    ]));
    this.query_url = '/visualiser/query';
}
Object.assign(VisualiserControllerImpl.prototype, {
    fetch(filter) {
        var request = new Request(this.query_url, {
            method: 'POST',
            redirect: 'follow',
            body: JSON.stringify(filter)
        });
        fetch(request).then(response =>
            response.json().then(data => this.interpret(data)));
    },
    interpret(data) {
    },
    categorise() {}
});

return module('VisualiserController', {instance: VisualiserControllerImpl});

});

require(['health-watch-visualiser', 'bind'],
function(VisualiserController, bind){
$(function() {
'use strict';
var instance = VisualiserController.instance($('#worker-url').val());
bind.bind(
    '.visualiser.program-definitions, .visualiser.program-area',
    instance,
    {
        start: '%{',
        end: '}%'
    });
instance.fetch({});
});
});