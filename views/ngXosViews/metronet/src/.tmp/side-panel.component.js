/**
 * © OpenCORD
 *
 * Visit http://guide.xosproject.org/devguide/addview/ for more information
 *
 * Created by teone on 10/4/16.
 */

'use strict';

(function () {
  'use strict';
  angular.module('xos.metronet').component('metronetSidePanel', {
    controllerAs: 'vm',
    template: '\n        <div\n            class="metronet-side-panel container-fluid"\n            ng-class="{active: vm.connection}">\n            <div class="row">\n                <div class="col-xs-12 pull-right">\n                    <a \n                        class="close"\n                        ng-click="vm.connection = null">\n                        <span>×</span>\n                    </a>\n                </div>\n                <div class="col-xs-12">\n                    <!--<pre>{{vm.connection | json}}</pre>-->\n                    <xos-form ng-model="vm.connection" config="vm.config"></xos-form>\n                </div>\n            </div>\n        </div>\n      ',
    controller: function controller($rootScope, Eline, ELan, ETree, MetronetEline, MetronetLineDrawer) {
      var _this = this;

      $rootScope.$on('connection.details', function (evt, connection) {
        _this.connection = connection;
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
            options: [{ id: 'ethernet', label: 'Ethernet' }, { id: 'direct', label: 'Direct' }]
          },
          operstate: {
            type: 'select',
            options: [{ id: 'active', label: 'Active' }, { id: 'inactive', label: 'Inactive' }]
          },
          adminstate: {
            type: 'select',
            options: [{ id: 'enabled', label: 'Enabled' }, { id: 'disabled', label: 'Disabled' }]
          }
        },
        actions: [{
          label: 'Save',
          icon: 'ok',
          'class': 'success',
          cb: function cb(item, form) {
            console.log(item);
            var R = undefined;
            switch (item.kind) {
              case 'eline':
                R = Eline;
                break;
            }
            delete item.kind;
            var conn = new R(item);
            conn.$save().then(function (res) {
              MetronetLineDrawer.cleanLine();
              MetronetEline.drawEline(res);
              _this.connection = null;
            });
          }
        }, {
          label: 'Delete',
          icon: 'remove',
          'class': 'danger',
          cb: function cb(item) {
            item.$delete().then(function () {
              MetronetLineDrawer.cleanLine();
              MetronetEline.removeElineById(item.id);
              _this.connection = null;
            });
          }
        }]
      };
    }
  });
})();