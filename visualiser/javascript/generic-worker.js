/**
 * Created by dingxiangfei on 17/2/16.
 */
'use strict';
addEventListener('message', process_configuration);

var el, util;
function process_configuration(e) {
    var config = e.data;
    importScripts(config.base_script);
    require(['el/el', 'util/util'], function() {
        el = arguments[0];
        util = arguments[1];
    });
}