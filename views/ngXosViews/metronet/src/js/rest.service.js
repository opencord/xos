(function () {
  'use strict';

  const apiPrefix = '/api/service/metronetworkservice';

  angular.module('xos.metronet')
    .service('Uni', function ($resource) {
      return $resource(`${apiPrefix}/UNI/`)
    })
    .service('Eline', function ($resource) {
      return $resource(`${apiPrefix}/ELINE/`)
    })
    .service('ETree', function ($resource) {
      return $resource(`${apiPrefix}/ETREE/`)
    })
    .service('ELan', function ($resource) {
      return $resource(`${apiPrefix}/ELAN/`)
    });

}());