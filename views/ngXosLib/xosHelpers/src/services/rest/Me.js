(function() {
  'use strict';

  angular.module('xos.helpers')
  /**
  * @ngdoc service
  * @name xos.helpers.Me
  * @description Angular resource to fetch /api/utility/me/
  **/
  .service('Me', function($q,$http){

    this.get = () => {
      let deferred = $q.defer();

      $http.get('/api/utility/me/')
      .then(res => {
        deferred.resolve(res);
      })
      .catch(res => {
        deferred.reject(res);
      });
      return deferred.promise;

    };
  })
})();