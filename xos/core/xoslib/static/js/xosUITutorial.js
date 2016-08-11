"use strict";angular.module("xos.UITutorial",["ngResource","ngCookies","ui.router","xos.helpers"]).config(["$stateProvider",function(e){e.state("shell",{url:"/",template:"<js-shell></js-shell>"})}]).config(["$httpProvider",function(e){e.interceptors.push("NoHyperlinks")}]).directive("jsShell",["TemplateHandler",function(e){return{restrict:"E",scope:{},bindToController:!0,controllerAs:"vm",templateUrl:"templates/js-shell.tpl.html",controller:["ExploreCmd",function(r){var t=this,o=new Josh.History({key:"jsshell.history"});this.shell=Josh.Shell({history:o}),this.shell.onNewPrompt(function(e){e("[ngXosLib] $ ")}),this.shell.setCommandHandler("explore",{exec:function(o,s,n){r.setup(t.shell),n(e.instructions({title:"You can now explore the API use angular $resouces!",messages:["Use <code>resource list</code> to list all the available resources and <code>resource {resoureName} {method} {?paramters}</code> to call the API.","An example command is <code>resource Slices query</code>","You can also provide paramters with <code>resource Slices query {max_instances: 10}</code>"]}))}}),this.shell.activate()}]}}]),angular.module("xos.UITutorial").run(["$templateCache",function(e){e.put("templates/js-shell.tpl.html",'<div id="shell-panel">\n  <div>\n    Type <code>help</code> or hit <code>TAB</code> for a list of commands.\n  </div>\n  <div id="shell-view"></div>\n</div>')}]),function(){angular.module("xos.UITutorial").service("TemplateHandler",["_",function(e){this.error=e.template('<span class="error">[ERROR] <%= msg %></span>'),this.instructions=e.template("\n      <div>\n        <strong><%= title %></strong>\n        <% _.forEach(messages, function(m) { %><p><%= m %></p><% }); %>\n      </div>\n    "),this.resourcesResponse=e.template('\n      <div>\n        <p>Corresponding js code: <code><%= jsCode %></code></p>\n        <div class="json"><%= res %></div>\n      </div>\n    '),this.jsonObject=e.template('<div class="jsonObject"><%= JSON.stringify(obj) %><%=comma%></code></div>'),this.jsonCollection=e.template('<div class="jsonCollection">[<% _.forEach(collection, function(item) { %><%= item %><%}); %>]</div>')}])}(),function(){angular.module("xos.UITutorial").service("ResponseHandler",["TemplateHandler",function(e){var r=this,t=["deleted","enabled","enacted","exposed_ports","lazy_blocked","created","validators","controllers","backend_status","backend_register","policed","no_policy","write_protect","no_sync","updated"];this.parseObject=function(r){var o=arguments.length<=1||void 0===arguments[1]?"":arguments[1];return r=_.omit(r,t),e.jsonObject({obj:r,comma:o})},this.parseCollection=function(t){return t=t.map(function(e,o){return""+r.parseObject(e,o===t.length-1?"":",")}),e.jsonCollection({collection:t})},this.parse=function(t,o,s){t=_.isArray(t)?r.parseCollection(t):r.parseObject(t),s(e.resourcesResponse({jsCode:o,res:t}))}}])}(),function(){angular.module("xos.UITutorial").service("ExploreCmd",["$injector","ResponseHandler","ErrorHandler",function($injector,ResponseHandler,ErrorHandler){var _this=this;this.resourceExec=function(e,r,t){switch(r[0]){case"list":return _this.listAvailableResources(t);default:var o=r.shift(),s=r.shift();return _this.consumeResource(o,s,r,t)}},this.resourceCompletion=function(e,r,t,o){var s=["list"].concat(_this.getAvailableResources());if(t.text.match(/resource\s[A-Z][a-z]+\s/)){s.indexOf(r)!==-1&&(r="");var n=["query","get","save","$save","delete"];return o(_this.shell.bestMatch(r,n))}return o(_this.shell.bestMatch(r,s))},this.setup=function(e){_this.shell=e,e.setCommandHandler("resource",{exec:_this.resourceExec,completion:_this.resourceCompletion})},this.getAvailableResources=function(){return angular.module("xos.helpers")._invokeQueue.filter(function(e){if("service"!==e[1])return!1;var r=e[2][1];return r.indexOf("$resource")!==-1}).reduce(function(e,r){return e.concat([r[2][0]])},[])},this.listAvailableResources=function(e){var r=_this.getAvailableResources().reduce(function(e,r){return""+e+r+"<br/>"},"");e(r)},this.consumeResource=function(resourceName,method,args,done){if(_this.getAvailableResources().indexOf(resourceName)===-1)return ErrorHandler.print('Resource "'+resourceName+'" does not exists',done);if(["query","get","save","$save","delete"].indexOf(method)===-1)return ErrorHandler.print('Method "'+method+'" not allowed',done);var params={};if(["get","$save","delete"].indexOf(method)!==-1&&0===args.length)return ErrorHandler.print('Method "'+method+'" require parameters',done);if(args.length>0&&(params=eval("("+args[0]+")")),"query"===method&&angular.isDefined(params.id))return ErrorHandler.print('Is not possible to use "id" as filter in method "'+method+'", use "get" instead!',done);var Resource=void 0;try{Resource=$injector.get(resourceName),Resource[method](params).$promise.then(function(e){var r=resourceName+"."+method+"("+(Object.keys(params).length>0?JSON.stringify(params):"")+")";return ResponseHandler.parse(e,r,done)})["catch"](function(e){if(404===e.status)return ErrorHandler.print(resourceName+' with method "'+method+'" and parameters '+JSON.stringify(params)+" "+e.data.detail,done)})}catch(e){return console.error(e),ErrorHandler.print('Failed to inject resource "'+resourceName+'"',done)}}}])}(),function(){angular.module("xos.UITutorial").service("ErrorHandler",["TemplateHandler",function(e){this.print=function(r,t){t(e.error({msg:r}))}}])}(),angular.module("xos.UITutorial").run(["$location",function(e){e.path("/")}]);