(function () {
  'use strict';

  angular.module('xos.mcord-slicing')
  .value('sliceElOrder', [
    'ue',
    'profile',
    'ran-ru',
    'ran-cu',
    'sgw',
    'pgw',
    'upstream'
  ])
  .service('slicePositioner', function(sliceElOrder){
    this.getNodePosition = (node, totalSlices, el) => {

      let y = (el.clientHeight / (totalSlices + 1)) * (node.sliceId || 1);

      let elPos = sliceElOrder.indexOf(node.type) + 1;

      let x = (el.clientWidth / (sliceElOrder.length + 1)) * elPos;

      return [x, y];
    };
  });

})();
