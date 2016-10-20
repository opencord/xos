'use strict';

var _slicedToArray = (function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i['return']) _i['return'](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError('Invalid attempt to destructure non-iterable instance'); } }; })();

(function () {
  'use strict';

  var latLng2Point = function latLng2Point(latLng, map) {
    var topRight = map.getProjection().fromLatLngToPoint(map.getBounds().getNorthEast());
    var bottomLeft = map.getProjection().fromLatLngToPoint(map.getBounds().getSouthWest());
    var scale = Math.pow(2, map.getZoom());
    var worldPoint = map.getProjection().fromLatLngToPoint(latLng);
    return new google.maps.Point((worldPoint.x - bottomLeft.x) * scale, (worldPoint.y - topRight.y) * scale);
  };

  var point2LatLng = function point2LatLng(point, map) {
    var topRight = map.getProjection().fromLatLngToPoint(map.getBounds().getNorthEast());
    var bottomLeft = map.getProjection().fromLatLngToPoint(map.getBounds().getSouthWest());
    var scale = Math.pow(2, map.getZoom());
    var worldPoint = new google.maps.Point(point.x / scale + bottomLeft.x, point.y / scale + topRight.y);
    return map.getProjection().fromPointToLatLng(worldPoint);
  };

  angular.module('xos.metronet').service('CentralOffice', function (_, MetronetCo, MetronetPort, MetronetMap, $rootScope, MetronetLineDrawer) {
    var _this = this;

    var self = this;
    this.ports = [];

    this.unisToCo = function (unis) {
      var tmp = _.groupBy(unis, 'latlng');
      return _.reduce(tmp, function (cos, unis) {
        var _JSON$parse = JSON.parse(unis[0].latlng);

        var _JSON$parse2 = _slicedToArray(_JSON$parse, 2);

        var lng = _JSON$parse2[0];
        var lat = _JSON$parse2[1];

        cos.push({
          latlng: { lat: lat, lng: lng },
          unis: unis,
          name: unis[0].name,
          location: unis[0].location,
          markers: [] // to store child marker
        });
        return cos;
      }, []);
    };

    this.addCoToMap = function (co, map) {
      var latlng = new google.maps.LatLng(co.latlng.lat, co.latlng.lng);
      var marker = new google.maps.Marker({
        position: latlng,
        map: _this.map,
        icon: MetronetCo,
        title: co.name,
        optimized: false,
        unis: co.unis,
        markers: co.markers,
        portConnections: []
      });
      MetronetMap.extendBounds(latlng);
      marker.setMap(map);

      google.maps.event.addListener(marker, 'mouseover', function () {
        if (MetronetLineDrawer.isDrawingEnabled()) {
          if (this.portShown !== true) {
            // draw ports
            self.showPortsFromCo(this, map);
            // NOTE emitting an event to avoid circular dependency
            $rootScope.$emit('metronet.redrawConnections', map);
          }
        }
      });

      self.addPortsToCo(marker, map);

      // add event listener
      google.maps.event.addListener(marker, 'click', function () {
        if (this.portShown !== true) {
          // draw ports
          self.showPortsFromCo(this, map);
        } else {
          // hide ports
          self.hidePortsFromCo(this, map);
        }

        // NOTE emitting an event to avoid circular dependency
        $rootScope.$emit('metronet.redrawConnections', map);
      });
    };

    this.addInfoWindow = function (marker) {
      var infowindow = new google.maps.InfoWindow({
        content: '\n              <h4>' + marker.uni.name + '</h4>\n              <strong>' + marker.uni.location + ' - ' + marker.uni.pid + '</strong>\n              <br/><br/>\n              <table class="table table-bordered">\n                <tr>\n                    <th><small>bwpCfgCbs</small></th>\n                    <td><small>' + marker.uni.bwpCfgCbs + '</small></td>\n                    <th><small>bwpCfgCir</small></th>\n                    <td><small>' + marker.uni.bwpCfgCir + '</small></td>\n                </tr>\n                <tr>\n                    <th><small>bwpCfgEbs</small></th>\n                    <td><small>' + marker.uni.bwpCfgEbs + '</small></td>\n                    <th><small>bwpCfgEir</small></th>\n                    <td><small>' + marker.uni.bwpCfgEir + '</small></td>\n                </tr>\n              </table>\n            '
      });

      marker.addListener('click', function () {
        infowindow.open(this.map, marker);
      });
    };

    this.getPortPosition = function (n, i, x, y) {
      var r = arguments.length <= 4 || arguments[4] === undefined ? 5 : arguments[4];

      return [x + r * Math.cos(2 * Math.PI * i / n), y + r * Math.sin(2 * Math.PI * i / n)];
    };

    this.addPortsToCo = function (co, map) {
      _.forEach(co.unis, function (uni, i) {

        // TODO fin a common scale, we need to set the child marker in the same position whatever the zoom is

        // moving the uni marker in the correct position
        var position = latLng2Point(co.position, map);

        var _getPortPosition = _this.getPortPosition(co.unis.length, i, position.x, position.y);

        var _getPortPosition2 = _slicedToArray(_getPortPosition, 2);

        var x = _getPortPosition2[0];
        var y = _getPortPosition2[1];

        position.x = x;
        position.y = y;
        var latlng = point2LatLng(position, map);

        // add markers
        var marker = new google.maps.Marker({
          position: latlng,
          icon: MetronetPort,
          title: uni.name,
          optimized: false,
          uni: uni,
          co: co,
          isShown: false
        });
        MetronetMap.extendBounds(latlng);

        // add marker to parent
        co.markers.push(marker);

        // add infowindow to co
        self.addInfoWindow(marker);

        // draw line from marker to parent
        co.portConnections.push(MetronetMap.drawLine(map, {}, null, co, marker));

        // add event listener
        google.maps.event.addListener(marker, 'mousedown', function () {
          if (MetronetLineDrawer.isDrawingEnabled()) {
            MetronetLineDrawer.setStartUni(this.uni);
          }
        });
        google.maps.event.addListener(marker, 'mouseup', function () {
          if (MetronetLineDrawer.isDrawingEnabled()) {
            MetronetLineDrawer.setEndUni(this.uni);
          }
        });

        _this.ports.push(marker);
      });
    };

    this.showPortsFromCo = function (co, map) {
      _.forEach(co.markers, function (marker) {
        marker.isShown = true;
        marker.setMap(map);
      });

      _.forEach(co.portConnections, function (poly) {
        poly.setMap(map);
      });

      co.portShown = true;
    };

    this.hidePortsFromCo = function (co, map) {
      _.forEach(co.markers, function (marker) {
        marker.isShown = false;
        marker.setMap(null);
      });

      _.forEach(co.portConnections, function (poly) {
        poly.setMap(null);
      });

      co.portShown = false;
    };
  });
})();