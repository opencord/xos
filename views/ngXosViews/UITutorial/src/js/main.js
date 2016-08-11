'use strict';

angular.module('xos.UITutorial', [
  'ngResource',
  'ngCookies',
  'ui.router',
  'xos.helpers'
])
.config(($stateProvider) => {
  $stateProvider
  .state('shell', {
    url: '/',
    template: '<js-shell></js-shell>'
  });
})
.config(function($httpProvider){
  $httpProvider.interceptors.push('NoHyperlinks');
})
.directive('jsShell', function(){
  return {
    restrict: 'E',
    scope: {},
    bindToController: true,
    controllerAs: 'vm',
    templateUrl: 'templates/js-shell.tpl.html',
    controller: function($injector){
      var history = new Josh.History({ key: 'helloworld.history'});
      var shell = Josh.Shell({history: history});

      shell.onNewPrompt(function(callback) {
        callback('[ngXosLib] $ ');
      });

      const errorHandler = (msg, done) => {
        const errorTpl = _.template(`<span class="error">[ERROR] <%= msg %></span>`);
        done(errorTpl({msg: msg}));
      }

      const parseResponse = (res, done) => {
        // TODO @Arpit format res (it can be an array or an object),
        // it is better if the output is a valid JSON (that we can copy and paste)
        res = res.map(i => {
          return JSON.stringify(i, ['id', 'name', 'max_instances'], 2) + '<br/>';
        });

        done(res);
      }

      const getAvailableResources = () => {
        return angular.module('xos.helpers')._invokeQueue
            .filter((d) => {
              if(d[1] !== 'service'){
                return false;
              }
              const serviceDeps = d[2][1];
              return serviceDeps.indexOf('$resource') !== -1;
            })
            .reduce((list, i) => list.concat([i[2][0]]), []);
      }

      const listAvailableResources = (done) => {
        const resources = getAvailableResources()
            .reduce((html, i) => `${html}${i}<br/>`, '');
        done(resources);
      }

      const consumeResource = (resourceName, method, done) => {

        if(getAvailableResources().indexOf(resourceName) === -1){
          return errorHandler(`Resource "${resourceName}" does not exists`, done);
        }

        if(['query', 'get', 'save', 'delete'].indexOf(method) === -1){
          return errorHandler(`Method "${method}" not allowed`, done);
        }

        let Resource;
        try{
          Resource = $injector.get(resourceName);

          // TODO @Teo if get/delete check for arguments

          Resource[method]().$promise
          .then(res => {
            return parseResponse(res, done);
          });
        }
        catch(e){
          console.log(e);
          return errorHandler(`Failed to inject resource "${resourceName}"`, done);
        }
      }

      shell.setCommandHandler('resource', {
        exec: (cmd, args, done) => {
          switch(args[0]){
            case 'list':
              return listAvailableResources(done);
              break;
            default:
              // use the resource
              return consumeResource(args[0], args[1], done);
          }
        },
        completion: function(cmd, arg, line, callback) {
          const args = ['list'].concat(getAvailableResources());
          callback(shell.bestMatch(arg, args))
        }
      })

      shell.setCommandHandler('slices', {
        exec: (cmd, args, done) => {
          Slices.query().$promise
          .then(res => {
            res = res.map(i => {
              return JSON.stringify(i, ['id', 'name', 'max_instances'], 2);
            });
            
            res = res.reduce((response, item) => {
              return `${response},<br>${item}`;
            });

            done(res);
          })
          .catch(err => {
            console.log(err);
            done('An error occurred');
          })
        }
      });

      // shell.setCommandHandler("hello", {
      //   exec: function(cmd, args, callback) {
      //     var arg = args[0] || '';
      //     var response = "who is this " + arg + " you are talking to?";
      //     if(arg === 'josh') {
      //         response = 'pleased to meet you.';
      //     } else if(arg === 'world') {
      //         response = 'world says hi.'
      //     } else if(!arg) {
      //         response = 'who are you saying hello to?';
      //     }
      //     callback(response);
      //   },
      //   completion: function(cmd, arg, line, callback) {
      //       callback(shell.bestMatch(arg, ['world', 'josh']))
      //   }
      // });

      shell.activate();
    }
  };
});