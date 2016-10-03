'use strict';

// fix for google maps
const google = {
  maps: {
    Point: function(a, b){
      this.a = a;
      this.b = b;
    }
  }
};

angular.module('templates', []);