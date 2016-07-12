(function() {
  'use strict';

  angular.module('xos.helpers')
  /**
  * @ngdoc service
  * @name xos.helpers.Dashboards
  * @description Angular resource to fetch /api/core/dashboardviews/:id/
  **/
  .service('Dashboards', function($resource){
    return $resource('/api/core/dashboardviews/:id/', { id: '@id' }, {
      update: { method: 'PUT' }
    });
  })
})();