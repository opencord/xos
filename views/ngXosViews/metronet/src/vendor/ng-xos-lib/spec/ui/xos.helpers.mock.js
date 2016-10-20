(function () {
  'use strict';
  angular.module('xos.helpers', ['xos.uiComponents'])
  .factory('_', $window => $window._ );
})();