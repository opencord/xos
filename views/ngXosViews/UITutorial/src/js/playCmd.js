(function () {
  'use strict';
  angular.module('xos.UITutorial')
  .service('PlayCmd', function($compile, $rootScope, ErrorHandler){

    // TODO investigate if we can load directives from an app
    const components = [
      'xosTable',
      'xosForm'
    ];

    this.componentCompletion = (cmd, arg, line, done) => {
      return done(this.shell.bestMatch(arg, components));
    };

    this.componentExec = (cmd, args, done) => {
      const targetComponent = args[0];

      if(!targetComponent){
        return ErrorHandler.print(`Component "${targetComponent}" does not exists`, done);
      }

      this.attachComponent(targetComponent, done);
    };

    this.attachComponent = (targetComponent, done) => {
      this.scope = $rootScope.$new();
      this.scope.config = {
        columns: [
          {label: 'Data', prop: 'data'}
        ]
      };
      this.scope.data = [
        {data: 1},
        {data: 2}
      ];

      $rootScope.$emit('uiTutorial.attachScope', this.scope);

      const directive = $compile('<xos-table config="config" data="data"></xos-table>')(this.scope);
      const container = $('#directive-container');
      container.append( directive );
      done('bella');
    };

    $rootScope.$on('uiTutorial.applyScope', (e, scope) => {
      console.log('applyScope', scope);
      this.scope.config = scope.config;
      this.scope.data = scope.data;
    });

    this.setup = (shell) => {
      this.shell = shell;
      shell.setCommandHandler('component', {
        exec: this.componentExec,
        completion: this.componentCompletion
      });

      // activate listener to enable/disable shell
      $('textarea').click((e) => {
        this.shell.deactivate();
      });

      $('#shell-panel').click((e) => {
        this.shell.activate();
      });
    };

    
  });
})();