/**
 * © OpenCORD
 *
 * Visit http://guide.xosproject.org/devguide/addview/ for more information
 *
 * Created by teone on 10/20/16.
 */

'use strict';

(function () {
  'use strict';
  angular.module('xos.globalXos').service('Controllers', function ($resource) {
    return $resource('/api/core/controllers/:id', { id: '@id' });
  }).service('GXOS', function ($q, $resource, _, LXOS) {
    var _this = this;

    this.attachXosToItem = function (items) {
      var target = arguments.length <= 1 || arguments[1] === undefined ? LXOS : arguments[1];

      return _.map(items, function (lxos, i) {
        var currentXos = target[i];
        return _.map(lxos, function (item) {
          item.xos = currentXos;
          return item;
        });
      });
    };

    this.buildQueryEndpoint = function (baseUrl) {
      var target = arguments.length <= 1 || arguments[1] === undefined ? LXOS : arguments[1];

      return function () {
        var d = $q.defer();

        // store generated $resource for each L-XOS
        var r = [];

        var p = [];
        _.forEach(target, function (xos, i) {
          var resource = $resource('' + xos.auth_url + baseUrl, { id: '@id' }, {
            query: {
              isArray: true,
              headers: {
                Authorization: 'Basic ' + btoa(xos.admin_user + ':' + xos.admin_password)
              }
            }
          });
          r.push(resource);
          p.push(r[i].query().$promise);
        });

        $q.all(p).then(function (res) {
          res = _this.attachXosToItem(res, target);
          d.resolve(_.flatten(res));
        })['catch'](d.reject);

        return { $promise: d.promise };
      };
    };

    // TODO evaluate
    this.buildLocalResource = function (baseUrl, xos) {
      var headers = {
        Authorization: 'Basic ' + btoa(xos.admin_user + ':' + xos.admin_password)
      };
      var resource = $resource('' + xos.auth_url + baseUrl, { id: '@id' }, {
        query: {
          isArray: true,
          headers: headers
        }
      });
      return resource;
    };
  }).service('LocalAuth', function ($q, $http, _, LXOS) {
    var baseUrl = 'api/utility/login/';
    this.login = function () {
      var d = $q.defer();

      var p = [];
      _.forEach(LXOS, function (xos, i) {
        var loginRequest = $http.post('' + xos.auth_url + baseUrl, { username: xos.admin_user, password: xos.admin_password });
        p.push(loginRequest);
      });

      $q.all(p).then(function (auths) {
        _.forEach(auths, function (auth, i) {
          LXOS[i].xoscsrftoken = auth.data.xoscsrftoken;
          LXOS[i].xossessionid = auth.data.xossessionid;
          LXOS[i].user = JSON.parse(auth.data.user);
        });
        d.resolve();
      })['catch'](function (e) {
        d.reject(e);
      });

      return d.promise;
    };
  }).service('LocalSlices', function (GXOS) {
    var baseUrl = 'api/utility/slicesplus/';

    // TODO build a global resource
    this.queryFromAll = function (targets) {
      return GXOS.buildQueryEndpoint(baseUrl, targets)();
    };
  }).service('LocalUsers', function (GXOS) {
    var baseUrl = 'api/core/users/';

    // TODO build a global resource
    this.queryFromAll = GXOS.buildQueryEndpoint(baseUrl);
  }).service('LocalInstances', function ($q, $http, GXOS, LocalDeployments, LocalImages, LocalFlavor, LocalNode) {
    var baseUrl = 'api/core/instances/';

    // NOTE Evaluate to dinamically create a resource targeted to a L-XOS

    this.queryFromAll = function (targets) {
      return GXOS.buildQueryEndpoint(baseUrl, targets)();
    };
    this.createOnLocal = function (instance) {
      var d = $q.defer();
      var xos = instance.xos;
      delete instance.xos;
      $http.post('' + xos.auth_url + baseUrl, instance, {
        headers: {
          Authorization: 'Basic ' + btoa(xos.admin_user + ':' + xos.admin_password)
        }
      }).then(function (inst) {
        d.resolve(inst);
      })['catch'](function (e) {
        d.reject(e);
      });

      return d.promise;
    };

    this.getFromLocal = function (xos, params) {
      var d = $q.defer();
      $http.get('' + xos.auth_url + baseUrl, {
        params: params,
        headers: {
          Authorization: 'Basic ' + btoa(xos.admin_user + ':' + xos.admin_password)
        }
      }).then(function (inst) {
        d.resolve(inst.data);
      })['catch'](function (e) {
        d.reject(e);
      });

      return d.promise;
    };

    this.getLocalInfo = function (xos) {
      var d = $q.defer();
      $q.all([LocalDeployments.queryFromLocal(xos), LocalImages.queryFromLocal(xos), LocalFlavor.queryFromLocal(xos), LocalNode.queryFromLocal(xos)]).then(function (res) {
        res = _.map(res, function (collection) {
          return _.map(collection, function (item) {
            return { id: item.id, label: item.name };
          });
        });
        d.resolve(res);
      })['catch'](d.reject);
      return d.promise;
    };
  }).service('LocalDeployments', function ($q, $http) {

    var baseUrl = 'api/core/deployments/';

    this.queryFromLocal = function (xos) {
      var d = $q.defer();

      $http.get('' + xos.auth_url + baseUrl, {
        headers: {
          Authorization: 'Basic ' + btoa(xos.admin_user + ':' + xos.admin_password)
        }
      }).then(function (res) {
        d.resolve(res.data);
      })['catch'](function (e) {
        d.reject(e);
      });

      return d.promise;
    };
  }).service('LocalImages', function ($q, $http) {

    var baseUrl = 'api/core/images/';

    this.queryFromLocal = function (xos) {
      var d = $q.defer();

      $http.get('' + xos.auth_url + baseUrl, {
        headers: {
          Authorization: 'Basic ' + btoa(xos.admin_user + ':' + xos.admin_password)
        }
      }).then(function (res) {
        d.resolve(res.data);
      })['catch'](function (e) {
        d.reject(e);
      });

      return d.promise;
    };
  }).service('LocalFlavor', function ($q, $http) {

    var baseUrl = 'api/core/flavors/';

    this.queryFromLocal = function (xos) {
      var d = $q.defer();

      $http.get('' + xos.auth_url + baseUrl, {
        headers: {
          Authorization: 'Basic ' + btoa(xos.admin_user + ':' + xos.admin_password)
        }
      }).then(function (res) {
        d.resolve(res.data);
      })['catch'](function (e) {
        d.reject(e);
      });

      return d.promise;
    };
  }).service('LocalNode', function ($q, $http) {

    var baseUrl = 'api/core/nodes/';

    this.queryFromLocal = function (xos) {
      var d = $q.defer();

      $http.get('' + xos.auth_url + baseUrl, {
        headers: {
          Authorization: 'Basic ' + btoa(xos.admin_user + ':' + xos.admin_password)
        }
      }).then(function (res) {
        d.resolve(res.data);
      })['catch'](function (e) {
        d.reject(e);
      });

      return d.promise;
    };
  });
})();