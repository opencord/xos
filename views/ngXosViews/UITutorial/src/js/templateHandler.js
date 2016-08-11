(function () {
  'use strict';
  angular.module('xos.UITutorial')
  .service('TemplateHandler', function(_){
    
    this.error = _.template(`<span class="error">[ERROR] <%= msg %></span>`);

    this.instructions = _.template(`
      <div>
        <strong><%= title %></strong>
        <% _.forEach(messages, function(m) { %><p><%= m %></p><% }); %>
      </div>
    `);

    this.resourcesResponse = _.template(`
      <div>
      <p>Corresponding js code: <code><%= jsCode %></code></p>
        <p><%= res %></p>
      </div>
    `);
  });
})();