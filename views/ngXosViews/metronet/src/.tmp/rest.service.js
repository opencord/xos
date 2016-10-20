'use strict';

(function () {
  'use strict';

  var apiPrefix = '/api/service/metronetworkservice';

  angular.module('xos.metronet').service('Uni', function ($resource) {
    return $resource(apiPrefix + '/UNI/:id', { id: '@id' });
  }).service('Eline', function ($resource) {
    return $resource(apiPrefix + '/ELINE/:id', { id: '@id' });
  }).service('ETree', function ($resource) {
    return $resource(apiPrefix + '/ETREE/:id', { id: '@id' });
  }).service('ELan', function ($resource) {
    return $resource(apiPrefix + '/ELAN/:id', { id: '@id' });
  });
})();