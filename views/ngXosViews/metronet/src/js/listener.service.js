(function () {
  'use strict';
  angular.module('xos.metronet')
  .service('MetronetListener', function($timeout, MetronetState, MetronetCfg, MetronetPanel, MetronetForce, MetronetGraph){

    // we don't want to accept
    // new actions before transition has ended
    let enabled = true;

    const enable = () => {
      $timeout(() => {
        enabled = true;
      }, MetronetCfg.transition + 100);
    };

    const disable = () => enabled = false;

    const functionBinding = {
      toggleHelp: () => {
        MetronetPanel.toggleHelpPanel(keyBindings);
      },
      toglgeLabels: () => {
        MetronetState.showLabels = !MetronetState.showLabels;
        MetronetForce.redraw();
      },
      toggleAllPorts: () => {
        MetronetState.showAllPorts = !MetronetState.showAllPorts;
        MetronetGraph.toggleAllPorts();
        MetronetForce.redraw();
      },
      toggleEtree: () => {
        MetronetGraph.toggleEtree();
        MetronetState.showEtrees = !MetronetState.showEtrees;
        MetronetForce.redraw();
      },
      toggleEline: () => {
        MetronetGraph.toggleEline();
        MetronetState.showElines = !MetronetState.showElines;
        MetronetForce.redraw();
      }
    };

    const keyBindings = {
      l: {
        action: 'Toggle Central Office labels',
        key: 'l',
        cb: functionBinding.toglgeLabels
      },
      '/': {
        action: 'Toggle Help panel',
        key: '/',
        cb: functionBinding.toggleHelp
      },
      '\\': {
        action: 'Toggle Help panel',
        key: '\\',
        cb: functionBinding.toggleHelp
      },
      'Escape': {
        action: 'Toggle Help panel',
        key: 'Esc',
        cb: functionBinding.toggleHelp
      },
      u: {
        action: 'Toggle UNIs',
        key: 'u',
        cb: functionBinding.toggleAllPorts
      },
      t: {
        action: 'Toggle E-Trees',
        key: 't',
        cb: functionBinding.toggleEtree
      },
      i: {
        action: 'Toggle E-Lines',
        key: 'i',
        cb: functionBinding.toggleEline
      }
    };


    d3.select('body')
    .on('keydown', () => {
      console.log(d3.event.key);
      const action = keyBindings[d3.event.key];
      if(action && enabled){
        disable();
        action.cb();
        enable();
      }
    });
  })
  .service('MetronetPanel', function($rootScope){
    this.helpPanel = false;
    this.toggleHelpPanel = (data) => {
      if(this.helpPanel){
        $rootScope.$emit('metronet.panel.hide');
      }
      else{
        $rootScope.$emit('metronet.panel.display', data);
      }
      this.helpPanel = !this.helpPanel;
    };
  })
  .component('metronetPanel', {
    controllerAs: 'vm',
    template: `
      <div class="metronet-panel" ng-class="{rotated: vm.show}">
        <div class="row" ng-repeat="(m, action) in vm.actions">
          <div class="col-xs-3">
            <span ng-repeat="a in action">
              {{a.key}}
              <span ng-if="$index < action.length - 1">, </span>
            </span>
          </div>
          <div class="col-xs-8">
            {{m}}
          </div>
        </div>
      </div>
    `,
    controller: function($rootScope, _){
      this.show = false;
      $rootScope.$on('metronet.panel.display', (e, data) => {
        this.show = true;
        this.actions = _.groupBy(data, 'action');
      });

      $rootScope.$on('metronet.panel.hide', () => {
        this.show = false;
      });
    }
  })
})();