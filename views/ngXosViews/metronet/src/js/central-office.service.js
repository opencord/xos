(function () {
  'use strict';

  const latLng2Point = (latLng, map) => {
    var topRight = map.getProjection().fromLatLngToPoint(map.getBounds().getNorthEast());
    var bottomLeft = map.getProjection().fromLatLngToPoint(map.getBounds().getSouthWest());
    var scale = Math.pow(2, map.getZoom());
    var worldPoint = map.getProjection().fromLatLngToPoint(latLng);
    return new google.maps.Point((worldPoint.x - bottomLeft.x) * scale, (worldPoint.y - topRight.y) * scale);
  };

  const point2LatLng = (point, map) => {
    var topRight = map.getProjection().fromLatLngToPoint(map.getBounds().getNorthEast());
    var bottomLeft = map.getProjection().fromLatLngToPoint(map.getBounds().getSouthWest());
    var scale = Math.pow(2, map.getZoom());
    var worldPoint = new google.maps.Point(point.x / scale + bottomLeft.x, point.y / scale + topRight.y);
    return map.getProjection().fromPointToLatLng(worldPoint);
  };

  angular.module('xos.metronet')
  .service('CentralOffice', function (_, MetronetCo, MetronetPort, MetronetMap, $rootScope) {
    const self = this;
    this.ports = [];

    this.unisToCo = (unis) => {
      let tmp = _.groupBy(unis, 'latlng');
      return _.reduce(tmp, (cos, unis) => {
        let [lng, lat] = JSON.parse(unis[0].latlng);
        cos.push({
          latlng: {lat: lat, lng: lng},
          unis: unis,
          name: unis[0].name,
          location: unis[0].location,
          markers: [] // to store child marker
        });
        return cos;
      }, [])
    };

    this.addCoToMap = (co, map) => {
      const latlng = new google.maps.LatLng(co.latlng.lat, co.latlng.lng);
      const marker = new google.maps.Marker({
        position: latlng,
        map: this.map,
        icon: MetronetCo,
        title: co.name,
        optimized: false,
        unis: co.unis,
        markers: co.markers,
        portConnections: []
      });
      MetronetMap.extendBounds(latlng);
      marker.setMap(map);

      self.addPortsToCo(marker, map);

      // add event listener
      google.maps.event.addListener(marker, 'click', function() {
        if(this.portShown !== true){
          // draw ports
          self.showPortsFromCo(this, map);
        }
        else {
          // hide ports
          self.hidePortsFromCo(this, map);
        }

        // NOTE emitting an event to avoid circular dependency
        $rootScope.$emit('metronet.redrawConnections', map);
      });
    };

    this.getPortPosition = (n, i, x, y, r = 5) => {
      return [
        x + r * Math.cos(2 * Math.PI * i / n),
        y + r * Math.sin(2 * Math.PI * i / n)
      ];
    };

    this.addPortsToCo = (co, map) => {
      _.forEach(co.unis, (uni, i) => {

        // TODO fin a common scale, we need to set the child marker in the same position whatever the zoom is

        // moving the uni marker in the correct position
        const position = latLng2Point(co.position, map);
        let [x, y] = this.getPortPosition(co.unis.length, i, position.x, position.y);
        position.x = x;
        position.y = y;
        const latlng = point2LatLng(position, map);

        // add markers
        const marker = new google.maps.Marker({
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

        // draw line from marker to parent
        co.portConnections.push(MetronetMap.drawLine(map, {}, co, marker));

        this.ports.push(marker);
      });

    };

    this.showPortsFromCo = (co, map) => {
      _.forEach(co.markers, marker => {
        marker.isShown = true;
        marker.setMap(map);
      });

      _.forEach(co.portConnections, poly => {
        poly.setMap(map);
      });

      co.portShown = true;
    };

    this.hidePortsFromCo = (co, map) => {
      _.forEach(co.markers, marker => {
        marker.isShown = false;
        marker.setMap(null);
      });

      _.forEach(co.portConnections, poly => {
        poly.setMap(null);
      });

      co.portShown = false;
    }
  });

}());