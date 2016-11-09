(function () {
  'use strict';

  angular.module('xos.metronet')
  .service('MetronetEtree', function(
    $q,
    $rootScope,
    CentralOffice,
    MetronetMap,
    MetronetLine,
    ETree){

    this.paths = [];
    this.map;

    $rootScope.$on('metronet.redrawConnections', (evt, map) => {
      this.cleanEtrees(map, this.paths);
      this.renderEtrees(map);
    });

    // draw Etrees on map
    this.renderEtrees = (map = this.map) => {
      this.map = map;
      const d = $q.defer();
      ETree.query().$promise
      .then(etrees => {
        this.etrees = etrees;
        this.map = map;
        _.forEach(etrees, etree => {
          this.drawEtree(etree, map);
        });
        d.resolve(this.etrees);
      })
      .catch(err => {
        d.reject(err);
      });
      return d.promise;
    };

    this.drawEtree = (etree, map = this.map) => {
      const root = CentralOffice.findPortMarker(etree.root);
      const points = _.map(etree.eps, uni => {
        return CentralOffice.findPortMarker(uni);
      });

      // each Etree is composed by multiple path from root to each uni
      const paths = _.reduce(points, (list, uni) => {
        const path = MetronetMap.drawLine(map, {color: MetronetLine['etree'], setMap: true}, etree, root, uni);
        path.connection = etree;
        list.push(path);
        return list;
      }, []);
      this.paths.push(paths);
    };

    this.cleanEtrees = (map, paths) => {
      _.forEach(_.flatten(paths), p => {
        p.setMap(null);
      });
    };

    this.removeEtreeById = (id) => {
      let path = _.filter(_.flatten(this.paths), p => p.connection.id === id);
      _.remove(this.etrees, {id: id});
      this.cleanEtrees(this.map, path);
    };

  });
})();
