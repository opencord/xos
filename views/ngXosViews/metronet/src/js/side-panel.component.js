/**
 * © OpenCORD
 *
 * Visit http://guide.xosproject.org/devguide/addview/ for more information
 *
 * Created by teone on 10/4/16.
 */

(function () {
  'use strict';
  angular.module('xos.metronet')
    .component('metronetSidePanel', {
      controllerAs: 'vm',
      template: `
        <div
            class="metronet-side-panel container-fluid"
            ng-class="{active: vm.connection}">
            <div class="row">
                <div class="col-xs-12 pull-right">
                    <a 
                        class="close"
                        ng-click="vm.connection = null">
                        <span>×</span>
                    </a>
                </div>
                <div class="col-xs-12">
                    <!--<pre>{{vm.connection | json}}</pre>-->
                    <xos-form ng-model="vm.connection" config="vm.config"></xos-form>
                </div>
            </div>
        </div>
      `,
      controller: function($rootScope, $q, Eline, ELan, ETree, MetronetEline, MetronetELineDrawer) {
        $rootScope.$on('connection.details', (evt, connection) => {
          this.connection = connection;
          $rootScope.$apply();
        });

        this.config = {
          exclude: ['eps', 'connectionType', 'root', 'uni1', 'uni2', 'kind'],
          formName: 'sampleForm',
          fields: {
            humanReadableName: {
              type: 'text',
              required: true
            },
            sid: {
              type: 'text',
              required: true
            },
            type: {
              type: 'select',
              options: [
                {id: 'ethernet', label: 'Ethernet'},
                {id: 'direct', label: 'Direct'}
              ]
            },
            operstate: {
              type: 'select',
              options: [
                {id: 'active', label: 'Active'},
                {id: 'inactive', label: 'Inactive'}
              ]
            },
            adminstate: {
              type: 'select',
              options: [
                {id: 'enabled', label: 'Enabled'},
                {id: 'disabled', label: 'Disabled'}
              ]
            }
          },
          actions: [
            {
              label: 'Save',
              icon: 'ok',
              class: 'success',
              cb: (item, form) => {
                console.log(item);
                let R;
                switch(item.kind){
                  case 'eline':
                    R = Eline;
                    break;
                }
                delete item.kind;
                const conn = new R(item);
                conn.$save()
                .then(res => {
                  MetronetELineDrawer.cleanLine();
                  MetronetEline.drawEline(res);
                  this.connection = null;
                });
              }
            },
            {
              label: 'Delete',
              icon: 'remove',
              class: 'danger',
              cb: (item) => {
                let p;
                try{
                  p = item.$delete()
                }
                catch(e){
                  p = $q.resolve();
                }

                p.then(() => {
                  MetronetELineDrawer.cleanLine();
                  if(item.id){
                    MetronetEline.removeElineById(item.id);
                  }
                  this.connection = null;
                })
              }
            }
          ]
        };


      }
    });
})();

