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
            <div class="row" ng-show="vm.kind === 'eline'">
              <div class="col-xs-6">
                <h5>Uni 1:</h5>
                <div class="well well-sm">
                  <h6>{{vm.connection.uni1.name}}</h6>
                </div>
              </div>
              <div class="col-xs-6">
                <h5>Uni 2:</h5>
                <div class="well well-sm">
                  <h6>{{vm.connection.uni2.name}}</h6>
                </div>
              </div>
            </div>
            <div class="row" ng-show="vm.kind === 'etree'">
              <div class="col-xs-6">
                <h5>Root:</h5>
                <div class="well well-sm">
                  <h6>{{vm.connection.root.name}}</h6>
                </div>
              </div>
              <div class="col-xs-6">
                <h5>Eps:</h5>
                <div class="well well-sm" ng-repeat="uni in vm.connection.eps">
                  <h6>{{uni.name}}</h6>
                </div>
              </div>
            </div>
        </div>
      `,
      controller: function($rootScope,
        $q,
      Eline,
      ELan,
      ETree,
      MetronetEline,
      MetronetELineDrawer,
      MetronetEtree,
      MetronetEtreeDrawer) {
        $rootScope.$on('connection.details', (evt, connection) => {
          this.connection = connection;

          if(connection.kind){
            this.kind = connection.kind;
          }
          else if (connection.type === 'direct'){
            this.kind = 'eline';
          }
          else if (connection.type === 'ethernet' && angular.isDefined(connection.root)){
            this.kind = 'etree';
          }

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
                delete item.kind;

                let R;
                switch(this.kind){
                case 'eline':
                  R = Eline;
                  break;
                case 'etree':
                  R = ETree;
                  break;
                }
                const conn = new R(item);
                conn.$save()
                .then(res => {
                  switch(this.kind){
                  case 'eline':
                    MetronetELineDrawer.cleanLine();
                    MetronetEline.drawEline(res);
                    break;
                  case 'etree':
                    MetronetEtreeDrawer.cleanLine();
                    MetronetEtreeDrawer.resetRootMarker();
                    MetronetEtree.drawEtree(res);
                    break;
                  }
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
                  switch(this.kind){
                  case 'eline':
                    MetronetELineDrawer.cleanLine();
                    if(item.id){
                      MetronetEline.removeElineById(item.id);
                    }
                    break;
                  case 'etree':
                    MetronetEtreeDrawer.cleanLine();
                    MetronetEtreeDrawer.resetRootMarker();
                    if(item.id){
                      MetronetEtree.removeEtreeById(item.id);
                    }
                    break;
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

