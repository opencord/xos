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

  angular.module('xos.metronet').service('MetronetEline', function ($rootScope, _, CentralOffice, MetronetMap, MetronetLine) {
    var _this = this;

    this.elines = [];
    this.paths = [];
    this.map;

    $rootScope.$on('metronet.redrawConnections', function (evt, map) {
      _this.cleanElines(map, _this.paths);
      _this.renderElines(map);
    });

    // draw Elines on map
    this.renderElines = function () {
      var map = arguments.length <= 0 || arguments[0] === undefined ? _this.map : arguments[0];
      var elines = arguments.length <= 1 || arguments[1] === undefined ? _this.elines : arguments[1];

      _this.elines = elines;
      _this.map = map;
      _.forEach(elines, function (eline) {
        _this.drawEline(eline, map);
      });
    };

    this.drawEline = function (eline) {
      var map = arguments.length <= 1 || arguments[1] === undefined ? _this.map : arguments[1];

      var start = _this.findPortMarker(eline.uni1);
      var end = _this.findPortMarker(eline.uni2);
      var path = MetronetMap.drawLine(map, { color: MetronetLine['eline'], setMap: true }, eline, start, end);
      _this.paths.push(path);
    };

    this.cleanElines = function (map, paths) {
      _.forEach(paths, function (p) {
        p.setMap(null);
      });
    };

    this.removeElineById = function (id) {
      var path = _.find(_this.paths, function (p) {
        return p.connection.id === id;
      });
      _.remove(_this.elines, { id: id });
      _this.cleanElines(_this.map, [path]);
    };

    // if the port is shown use port,
    // else use central office
    this.findPortMarker = function (uni) {
      var port = _.find(CentralOffice.ports, function (port) {
        return port.uni.id === uni.id;
      });
      if (port.isShown) {
        return port;
      } else {
        return port.co;
      }
    };
  });
})();