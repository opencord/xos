'use strict';

var _slicedToArray = (function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i['return']) _i['return'](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError('Invalid attempt to destructure non-iterable instance'); } }; })();

angular.module('xos.globalXos', ['ngResource', 'ngCookies', 'ui.router', 'xos.helpers', 'ui.bootstrap.modal', 'ui.bootstrap.tpls']).config(function ($stateProvider) {
  $stateProvider.state('xos-list', {
    url: '/',
    template: '<xos-list></xos-list>'
  });
}).config(function ($httpProvider) {
  $httpProvider.interceptors.push('NoHyperlinks');
}).value('LXOS', []).directive('xosList', function () {
  return {
    restrict: 'E',
    scope: {},
    bindToController: true,
    controllerAs: 'vm',
    templateUrl: 'templates/xos-list.tpl.html',
    controller: function controller($window, $q, _, Controllers, LXOS, LocalAuth, LocalSlices, LocalUsers, $uibModal, Slices) {
      var _this = this;

      var self = this;
      $q.all([Controllers.query({ backend_type: 'XOS' }).$promise, Slices.query().$promise // NOTE why this is queryFromAll??
      ]).then(function (res) {
        var _res = _slicedToArray(res, 2);

        _this.xoss = _res[0];
        _this.gSlices = _res[1];
      });

      this.openLocally = function (itemKind) {
        return function (item) {
          $window.open(item.xos.auth_url + 'admin/core/' + itemKind + '/' + item.id, '_blank');
        };
      };

      var baseSliceCols = [{
        label: 'Name',
        prop: 'name'
      }, {
        label: 'Mount Data Sets',
        prop: 'mount_data_sets'
      }];

      var lXosSliceCols = [{
        label: 'Max Instances',
        prop: 'max_instances'
      }, {
        label: 'Instances',
        prop: 'instance_total'
      }, {
        label: 'L-XOS',
        type: 'custom',
        formatter: function formatter(item) {
          return item.xos.name;
        }
      }];

      this.gSliceTableCgf = {
        columns: baseSliceCols,
        filter: 'field',
        order: true,
        actions: [{
          label: 'Get Instances',
          icon: 'search',
          cb: function cb(item) {
            $uibModal.open({
              animation: true,
              size: 'lg',
              templateUrl: 'listInstances.html',
              controllerAs: 'vm',
              resolve: {
                slice: function slice() {
                  return {
                    name: item.name,
                    xos: {
                      name: 'G-XOS'
                    }
                  };
                }
              },
              controller: function controller($uibModalInstance, slice, LocalInstances, LocalSlices) {
                var _this2 = this;

                this.slice = slice;

                this.config = {
                  columns: [{
                    label: 'Name',
                    prop: 'name'
                  }]
                };

                LocalSlices.queryFromAll(self.xoss).$promise.then(function (slices) {
                  // keep only the slice that match the name
                  _this2.slicesId = slices.filter(function (s) {
                    return s.name.indexOf(_this2.slice.name) > -1;
                  }).reduce(function (o, s) {
                    o[s.xos.id] = s.id;
                    return o;
                  }, {});
                  return LocalInstances.queryFromAll(self.xoss).$promise;
                }).then(function (instances) {
                  _this2.instances = instances.filter(function (i) {
                    return _this2.slicesId[i.xos.id] === i.slice;
                  });
                })['catch'](function (e) {
                  _this2.instances = [];
                });

                this.close = function () {
                  $uibModalInstance.dismiss('cancel');
                };
              }
            });
          }
        }]
      };

      this.sliceTableCfg = {
        columns: baseSliceCols.concat(lXosSliceCols),
        actions: [{
          label: 'open locally',
          icon: 'open',
          cb: this.openLocally('slice')
        }, {
          label: 'Get Instances',
          icon: 'search',
          cb: function cb(item) {
            $uibModal.open({
              animation: true,
              size: 'lg',
              templateUrl: 'listInstances.html',
              controllerAs: 'vm',
              resolve: {
                slice: function slice() {
                  return item;
                }
              },
              controller: function controller($uibModalInstance, slice, LocalInstances) {
                var _this3 = this;

                this.slice = slice;

                this.config = {
                  columns: [{
                    label: 'Name',
                    prop: 'name'
                  }, {
                    label: 'deployment',
                    prop: 'deployment'
                  }]
                };

                LocalInstances.getFromLocal(slice.xos).then(function (instances) {
                  _this3.instances = instances.filter(function (i) {
                    return i.slice === slice.id;
                  });
                });

                this.close = function () {
                  $uibModalInstance.dismiss('cancel');
                };
              }
            });
          }
        }, {
          label: 'Add Instance',
          icon: 'plus',
          cb: function cb(item) {
            $uibModal.open({
              animation: true,
              size: 'lg',
              templateUrl: 'addInstance.html',
              controller: function controller($uibModalInstance, slice, LocalInstances) {
                var _this4 = this;

                this.slice = slice;

                this.model = {};

                LocalInstances.getLocalInfo(slice.xos).then(function (res) {
                  var _res2 = _slicedToArray(res, 4);

                  _this4.config.fields['deployment'].options = _res2[0];
                  _this4.config.fields['image'].options = _res2[1];
                  _this4.config.fields['flavor'].options = _res2[2];
                  _this4.config.fields['node'].options = _res2[3];
                });

                this.config = {
                  formName: 'instanceForm',
                  excludedFields: ['xos', 'slice'],
                  actions: [{
                    label: 'Save',
                    icon: 'ok',
                    cb: function cb(instance) {
                      instance.xos = slice.xos;
                      instance.slice = slice.id;
                      instance.creator = instance.xos.user.id;
                      LocalInstances.createOnLocal(instance).then(function (res) {
                        slice.instance_total = slice.instance_total + 1;
                        $uibModalInstance.close();
                      });
                    },
                    'class': 'success'
                  }, {
                    label: 'Cancel',
                    icon: 'remove',
                    cb: function cb() {
                      $uibModalInstance.dismiss('cancel');
                    },
                    'class': 'warning'
                  }],
                  fields: {
                    name: {
                      type: 'text',
                      validators: {
                        required: true
                      }
                    },
                    deployment: {
                      type: 'select',
                      validators: {
                        required: true
                      }
                    },
                    node: {
                      type: 'select',
                      validators: {
                        required: true
                      }
                    },
                    image: {
                      type: 'select',
                      validators: {
                        required: true
                      }
                    },
                    flavor: {
                      type: 'select',
                      validators: {
                        required: true
                      }
                    },
                    isolation: {
                      type: 'select',
                      options: [{ id: 'vm', label: 'VM' }, { id: 'container', label: 'Container' }, { id: 'container_vm', label: 'Container in VM' }],
                      validators: {
                        required: true
                      }
                    }
                  }
                };
              },
              controllerAs: 'vm',
              resolve: {
                slice: function slice() {
                  return item;
                }
              }
            });
          }
        }],
        filter: 'field',
        order: true
      };

      this.usersTableCfg = {
        columns: [{
          label: 'Name',
          type: 'custom',
          formatter: function formatter(item) {
            return item.firstname + ' ' + item.lastname;
          }
        }, {
          label: 'E-Mail',
          prop: 'email'
        }, {
          label: 'User Name',
          prop: 'username'
        }, {
          label: 'Time Zone',
          prop: 'timezone'
        }, {
          label: 'L-XOS',
          type: 'custom',
          formatter: function formatter(item) {
            return item.xos.name;
          }
        }],
        actions: [{
          label: 'open locally',
          icon: 'open',
          cb: this.openLocally('user')
        }],
        filter: 'field',
        order: true
      };

      this.toggleXos = function (xos) {
        if (_.findIndex(LXOS, { id: xos.id }) > -1) {
          xos.active = false;
          _.remove(LXOS, { id: xos.id });
        } else {
          xos.active = true;
          LXOS.push(xos);
        }

        // authenticate on L-XOS
        LocalAuth.login().then(function () {
          // fetch slices
          return $q.all([LocalSlices.queryFromAll().$promise, LocalUsers.queryFromAll().$promise]);
        }).then(function (res) {
          var _res3 = _slicedToArray(res, 2);

          _this.localSlices = _res3[0];
          _this.localUsers = _res3[1];
        })['catch'](function (e) {
          console.log(e);
        });
      };
    }
  };
});