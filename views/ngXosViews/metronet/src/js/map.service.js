/**
 * © OpenCORD
 *
 * Visit http://guide.xosproject.org/devguide/addview/ for more information
 *
 * Created by teone on 10/17/16.
 */

(function () {
  'use strict';

  angular.module('xos.metronet')
  .service('MetronetMap', function(NgMap){
    NgMap.getMap()
    .then(map => {
      this.map = map;
    })
    .catch(e => {
      throw new Error(e);
    });

    this.bounds = new google.maps.LatLngBounds();

    this.extendBounds = (latlng) => {
      this.bounds.extend(latlng);
    };

    this.getBounds = () => {
      return this.bounds;
    };

    this.drawLine = (map, cfg, ...points) => {
      const path = [];
      _.forEach(points, p => {
        path.push({
          lat: p.position.lat(),
          lng: p.position.lng()
        });
      });

      // create a new Line
      const poly = new google.maps.Polyline({
        path: path,
        clickable: cfg.clickable,
        strokeColor: cfg.color || `#000`,
        strokeOpacity: 1.0,
        strokeWeight: 2
      });

      if(cfg.setMap === true){
        poly.setMap(map);
      }

      return poly;
    };
  });
})();

