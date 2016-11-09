/* eslint-disable angular/ng_module_name */
(function () {
  'use strict';
  console.log('hello!');
  angular.module('ngXosLib', ['xos.helpers'])
  .run(function(){
    console.info('Dev Environment ready!')
  })
  .controller('testCtrl', function(){

    // TODO add styles

    this.config = {
      columns: [
        {
          label: '#',
          prop: 'id',
        },
        {
          label: 'Name:',
          prop: 'name',
        }
      ]
    };

    this.data = [
      {id: 1, name: 'Jhon'}
    ];
  });
})();