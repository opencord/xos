/**
 * © OpenCORD
 *
 * Visit http://guide.xosproject.org/devguide/addview/ for more information
 *
 * Created by teone on 10/17/16.
 */

'use strict';

(function () {
  'use strict';

  angular.module('xos.metronet').service('MetronetMap', function (NgMap, $rootScope) {
    var _this = this;

    NgMap.getMap().then(function (map) {
      _this.map = map;
    })['catch'](function (e) {
      throw new Error(e);
    });

    this.bounds = new google.maps.LatLngBounds();

    this.extendBounds = function (latlng) {
      _this.bounds.extend(latlng);
    };

    this.getBounds = function () {
      return _this.bounds;
    };

    this.drawLine = function (map, cfg, connection) {
      for (var _len = arguments.length, points = Array(_len > 3 ? _len - 3 : 0), _key = 3; _key < _len; _key++) {
        points[_key - 3] = arguments[_key];
      }

      var path = [];
      _.forEach(points, function (p) {
        path.push({
          lat: p.position.lat(),
          lng: p.position.lng()
        });
      });

      // create a new Line
      var poly = new google.maps.Polyline({
        path: path,
        clickable: cfg.clickable,
        strokeColor: cfg.color || '#000',
        strokeOpacity: 1.0,
        strokeWeight: 2,
        connection: connection
      });

      if (cfg.setMap === true) {
        poly.setMap(map);
      }

      // attach a click handler
      if (connection) {
        poly.addListener('click', function () {
          $rootScope.$emit('connection.details', connection);
        });
      }

      return poly;
    };
  });
})();