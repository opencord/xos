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
  .service('MetronetEline', function($rootScope, _, CentralOffice, MetronetMap, MetronetLine) {

    this.elines = [];
    this.paths = [];

    $rootScope.$on('metronet.redrawConnections', (evt, map) => {
      this.cleanElines(map, this.paths);
      this.renderElines(map);
    });

    // draw Elines on map
    this.renderElines = (map, elines = this.elines) => {
      this.elines = elines;
      _.forEach(elines, eline => {
        this.drawEline(eline, map);
      });
    };

    this.drawEline = (eline, map) => {
      const start = this.findPortMarker(eline.uni1);
      const end = this.findPortMarker(eline.uni2);
      const path = MetronetMap.drawLine(map, {color: MetronetLine['eline'], setMap: true}, eline, start, end);
      this.paths.push(path);
    };

    this.cleanElines = (map, paths) => {
      _.forEach(paths, p => {
        p.setMap(null);
      })
    };

    // if the port is shown use port,
    // else use central office
    this.findPortMarker = (uni) => {
      const port = _.find(CentralOffice.ports, port => {
        return port.uni.id === uni.id;
      });
      if(port.isShown){
        return port;
      }
      else {
        return port.co;
      }
    };

  });
})();

