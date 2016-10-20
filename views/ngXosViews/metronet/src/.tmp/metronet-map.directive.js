"use strict";

var _slicedToArray = (function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; })();

function _toConsumableArray(arr) { if (Array.isArray(arr)) { for (var i = 0, arr2 = Array(arr.length); i < arr.length; i++) arr2[i] = arr[i]; return arr2; } else { return Array.from(arr); } }

(function () {
  'use strict';

  // https://snazzymaps.com/explore
  // const mapStyles = [{"featureType":"water","elementType":"geometry","stylers":[{"color":"#e9e9e9"},{"lightness":17}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":20}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#ffffff"},{"lightness":17}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#ffffff"},{"lightness":29},{"weight":0.2}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":18}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":16}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":21}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#dedede"},{"lightness":21}]},{"elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#ffffff"},{"lightness":16}]},{"elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#333333"},{"lightness":40}]},{"elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#f2f2f2"},{"lightness":19}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#fefefe"},{"lightness":20}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#fefefe"},{"lightness":17},{"weight":1.2}]}];
  var mapStyles = [{ "featureType": "administrative", "elementType": "labels.text.fill", "stylers": [{ "color": "#444444" }] }, { "featureType": "landscape", "elementType": "all", "stylers": [{ "color": "#f2f2f2" }] }, { "featureType": "poi", "elementType": "all", "stylers": [{ "visibility": "off" }] }, { "featureType": "road", "elementType": "all", "stylers": [{ "saturation": -100 }, { "lightness": 45 }] }, { "featureType": "road.highway", "elementType": "all", "stylers": [{ "visibility": "simplified" }] }, { "featureType": "road.arterial", "elementType": "labels.icon", "stylers": [{ "visibility": "off" }] }, { "featureType": "transit", "elementType": "all", "stylers": [{ "visibility": "off" }] }, { "featureType": "water", "elementType": "all", "stylers": [{ "color": "#46bcec" }, { "visibility": "on" }] }];

  angular.module('xos.metronet').component('metronetMap', {
    controllerAs: 'vm',
    template: "\n        <ng-map zoom=\"7\" center=\"0, 0\" styles=\"{{vm.mapStyles}}\"></ng-map>\n        <metronet-side-panel></metronet-side-panel>\n      ",
    controller: function controller($q, $rootScope, _, Eline, ELan, ETree, Uni, NgMap, CentralOffice, MetronetMap, MetronetEline, MetronetLineDrawer) {
      var _this = this;

      this.mapStyles = mapStyles;
      this.markers = [];
      this.elinesPath = [];
      this.etreesPath = [];
      this.elansPath = [];

      var startUni = undefined,
          endUni = undefined;

      this.bounds = new google.maps.LatLngBounds();

      $q.all([Uni.query().$promise, Eline.query().$promise, ELan.query().$promise, ETree.query().$promise, NgMap.getMap()]).then(function (res) {
        var _res = _slicedToArray(res, 5);

        _this.unis = _res[0];
        _this.elines = _res[1];
        _this.elans = _res[2];
        _this.etrees = _res[3];
        _this.map = _res[4];

        _this.cos = CentralOffice.unisToCo(_this.unis);

        _.forEach(_this.cos, function (co) {
          CentralOffice.addCoToMap(co, _this.map);
        });

        // TODO
        // [ ] if no result send to creation form

        // render info on the map
        MetronetEline.renderElines(_this.map, _this.elines);
        // this.renderEtrees(this.etrees, this.map);
        // this.renderElans(this.elans, this.map);

        // center the map
        _this.map.setCenter(MetronetMap.getBounds().getCenter());
        _this.map.fitBounds(MetronetMap.getBounds());

        // this.attachLineHandler();
        MetronetLineDrawer.attachDrawingEvents(_this.map);
      })["catch"](function (e) {
        throw new Error(e);
      });
      this.user = { name: 'world' };

      // draw Etrees on map
      this.renderEtrees = function (etrees, map) {
        _.forEach(etrees, function (etree) {

          // augment with info
          etree.connectionType = 'etree';

          _this.addMarker(etree.root);
          _.forEach(etree.eps, function (uni) {
            _this.addMarker(uni);
          });

          var unis = _.reduce(etree.eps, function (unis, uni) {
            unis.push(uni);
            return unis;
          }, [etree.root]);

          _this.addPath.apply(_this, [etree].concat(_toConsumableArray(unis)));
        });
      };

      this.renderElans = function (elans, map) {
        _.forEach(elans, function (elan) {

          // augment with info
          elan.connectionType = 'elan';

          _.forEach(elan.eps, function (uni) {
            _this.addMarker(uni);
          });
          // NOTE should we close the line?
          var unis = angular.copy(elan.eps);
          unis.push(elan.eps[0]);
          _this.addPath.apply(_this, [elan].concat(_toConsumableArray(unis)));
        });
      };

      this.addMarker = function (uni) {
        var _JSON$parse = JSON.parse(uni.latlng);

        var _JSON$parse2 = _slicedToArray(_JSON$parse, 2);

        var lng = _JSON$parse2[0];
        var lat = _JSON$parse2[1];

        angular.extend(uni, { lat: lat, lng: lng });

        // add markers
        var latlng = new google.maps.LatLng(lat, lng);
        var marker = new google.maps.Marker({
          position: latlng,
          map: _this.map,
          icon: markerIcon,
          title: uni.name,
          optimized: false,
          uni: uni
        });
        marker.setMap(_this.map);

        // extend maps bounds
        _this.bounds.extend(latlng);

        // add the info window
        _this.addInfoWindow(marker);
      };

      this.addPath = function (connection) {
        for (var _len = arguments.length, unis = Array(_len > 1 ? _len - 1 : 0), _key = 1; _key < _len; _key++) {
          unis[_key - 1] = arguments[_key];
        }

        // create a new Line
        var poly = new google.maps.Polyline({
          map: _this.map,
          clickable: true,
          connection: connection,
          strokeColor: lineColors[connection.connectionType]
        });

        // attach a click handler
        poly.addListener('click', function () {
          $rootScope.$emit('connection.details', connection);
        });

        // attach all the point to the line
        var latlng = function latlng(uni) {
          return {
            lat: function lat() {
              return uni.lat;
            },
            lng: function lng() {
              return uni.lng;
            }
          };
        };
        _.forEach(unis, function (uni) {
          return poly.getPath().push(latlng(uni));
        });
      };
    }
  });
})();