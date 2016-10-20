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
  });
})();

