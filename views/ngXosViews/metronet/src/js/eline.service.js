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
  .service('MetronetEline', function(
    $q,
    $rootScope,
    _,
    Eline,
    CentralOffice,
    MetronetMap,
    MetronetLine) {

    this.elines = [];
    this.paths = [];
    this.map;

    $rootScope.$on('metronet.redrawConnections', (evt, map) => {
      this.cleanElines(map, this.paths);
      this.renderElines(map);
    });

    // draw Elines on map
    this.renderElines = (map = this.map) => {
      const d = $q.defer();
      Eline.query().$promise
      .then(elines => {
        this.elines = elines;
        this.map = map;
        _.forEach(elines, eline => {
          this.drawEline(eline, map);
        });
        d.resolve(this.elines);
      })
      .catch(err => {
        d.reject(err);
      });
      return d.promise;
    };

    this.drawEline = (eline, map = this.map) => {
      const start = CentralOffice.findPortMarker(eline.uni1);
      const end = CentralOffice.findPortMarker(eline.uni2);
      const path = MetronetMap.drawLine(map, {color: MetronetLine['eline'], setMap: true}, eline, start, end);
      this.paths.push(path);
    };

    this.cleanElines = (map, paths) => {
      _.forEach(paths, p => {
        p.setMap(null);
      })
    };

    this.removeElineById = (id) => {
      let path = _.find(this.paths, p => p.connection.id === id);
      _.remove(this.elines, {id: id});
      this.cleanElines(this.map, [path]);
    };

  });
})();

