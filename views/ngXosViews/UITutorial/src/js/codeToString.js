(function () {
  angular.module('xos.UITutorial')
  .service('codeToString', function(){
    this.toString = code => {
      if(angular.isArray(code)){
        return code.map(item => this.toString(item));
      }
      else if(angular.isObject(code)){
        let tmp = {};
        Object.keys(code).forEach(key => {
          tmp[key] = this.toString(code[key])
        });
        return tmp;
      }
      else{
        return code.toString().split('\n').join('').replace(/ +(?= )/gmi, '');
      }
    }
  });
})();