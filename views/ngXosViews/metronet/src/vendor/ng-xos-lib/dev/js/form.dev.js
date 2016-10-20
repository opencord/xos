'use strict';

angular.module('ngXosLib')
  .component('formTest', {
    restrict: 'E',
    bindings: {},
    bindToController: true,
    controllerAs: 'vm',
    templateUrl: 'templates/form.dev.html',
    controller: function () {
      this.model = {
        first_name: 'Jhon',
        last_name: 'Doe',
      },
      this.config = {
        exclude: ['password', 'last_login'],
        formName: 'sampleForm',
        actions: [
          {
            label: 'Save',
            icon: 'ok', // refers to bootstraps glyphicon
            cb: (user) => { // receive the model
              console.log(user);
            },
            class: 'success'
          }
        ],
        order: ['last_name', 'select'],
        fields: {
          first_name: {
            type: 'string',
            validators: {
              required: true
            }
          },
          last_name: {
            label: 'Surname',
            type: 'string',
            validators: {
              required: true,
              minlength: 10
            }
          },
          select: {
            label: 'select',
            type: 'select',
            options: [
              {id: 1, label: 'a'},
              {id: 2, label: 'b'}
            ]
          },
          details_field: {
            label: 'Empty Object Field',
            type: 'object',
            properties: {
              foo: {
                label: 'FooLabel:',
                type: 'string',
                validators: {
                  required: true
                }
              },
              bar: {
                type: 'number'
              }
            }
          }
        }
      }
    }
  })
