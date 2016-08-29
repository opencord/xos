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
  .service('elementPositioner', function(sliceElOrder){
    this.getNodePosition = (node, el) => {

      let y = (el.clientHeight / (node.vTotal + 1)) * (node.vPos);

      if(node.plane === 'control'){
        y = y - 75;
      }

      let elPos = sliceElOrder.indexOf(node.type) + 1;

      if(node.type === 'mme'){
        elPos = sliceElOrder.indexOf('sgw') + 1
        y = y - 100;
      }

      let x = (el.clientWidth / (sliceElOrder.length + 1)) * elPos;

      return [x, y];
    };
  });

})();
