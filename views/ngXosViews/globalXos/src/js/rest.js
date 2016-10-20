/**
 * © OpenCORD
 *
 * Visit http://guide.xosproject.org/devguide/addview/ for more information
 *
 * Created by teone on 10/20/16.
 */

(function () {
  'use strict';
  angular.module('xos.globalXos')
  .service('Controllers', function($resource){
    return $resource('/api/core/controllers/:id', {id: '@id'});
  })
  .service('GXOS', function($q, $resource, _, LXOS){
    this.attachXosToItem = (items) => {
      return _.map(items, (lxos, i) => {
        let currentXos = LXOS[i];
        return _.map(lxos, (item) => {
          item.xos = currentXos;
          return item;
        });
      })
    };

    this.buildQueryEndpoint = (baseUrl) => {
      return () => {
        const d = $q.defer();

        // store generated $resource for each L-XOS
        let r = [];

        let p = [];
        _.forEach(LXOS, (xos, i) => {
          let resource = $resource(`${xos.auth_url}${baseUrl}`, {id: '@id'}, {
            query: {
              isArray: true,
              headers: {
                Authorization: `Basic ${btoa(xos.admin_user + ':' + xos.admin_password)}`
              }
            }
          });
          r.push(resource);
          p.push(r[i].query().$promise);
        });

        $q.all(p)
        .then(res => {
          res = this.attachXosToItem(res);
          d.resolve(_.flatten(res));
        })
        .catch(d.reject);

        return {$promise: d.promise};
      };
    };
  })
  .service('LocalAuth', function ($q, $http, _, LXOS) {
    const baseUrl = `api/utility/login/`;
    this.login = () => {
      const d = $q.defer();

      let p = [];
      _.forEach(LXOS, (xos, i) => {
        let loginRequest = $http.post(`${xos.auth_url}${baseUrl}`, {username: xos.admin_user, password: xos.admin_password});
        p.push(loginRequest);
      });

      $q.all(p)
      .then(auths => {
        _.forEach(auths, (auth, i) => {
          LXOS[i].xoscsrftoken = auth.data.xoscsrftoken;
          LXOS[i].xossessionid = auth.data.xossessionid;
        });
        d.resolve();
      })
      .catch(e => {
        d.reject(e);
      });

      return d.promise;
    }
  })
  .service('LocalSlices', function(GXOS){
    const baseUrl = `api/core/slices/`;

    this.query = GXOS.buildQueryEndpoint(baseUrl);
  })
  .service('LocalUsers', function(GXOS){
    const baseUrl = `api/core/users/`;

    this.query = GXOS.buildQueryEndpoint(baseUrl);
  });
})();

