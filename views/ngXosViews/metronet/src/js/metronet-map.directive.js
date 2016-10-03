(function () {
  'use strict';



  angular.module('xos.metronet')
    .component('metronetMap', {
      controllerAs: 'vm',
      template: `
        <ng-map zoom="7" center="0, 0">
          <marker 
            ng-repeat="m in vm.markers"
            position="{{m.lat}}, {{m.lng}}"></marker>
          <shape name="polyline"
            id="eline-{{$index}}"
            ng-repeat="path in vm.elinesPath"
            path="{{path}}"
            stroke-color="#FF0000"
            stroke-opacity="1.0"
            stroke-weight="3"></shape>
          <shape name="polyline"
            id="etree-{{$index}}"
            ng-repeat="path in vm.etreesPath"
            path="{{path}}"
            stroke-color="#0000FF"
            stroke-opacity="1.0"
            stroke-weight="3"></shape>
          <shape name="polyline"
            id="elan-{{$index}}"
            ng-repeat="path in vm.elansPath"
            path="{{path}}"
            stroke-color="#FF00FF"
            stroke-opacity="1.0"
            stroke-weight="3"></shape>
        </ng-map>
      `,
      controller: function($q, _, Eline, ELan, ETree, NgMap) {
        this.markers = [];
        this.elinesPath = [];
        this.etreesPath = [];
        this.elansPath = [];

        this.bounds = new google.maps.LatLngBounds();

        $q.all([
          Eline.query().$promise,
          ELan.query().$promise,
          ETree.query().$promise,
          NgMap.getMap()
        ])
        .then(res => {
          [this.elines, this.elans, this.etrees, this.map] = res;
          // TODO
          // [ ] if no result send to creation form

          // render info on the map
          this.renderElines(this.elines, this.map);
          this.renderEtrees(this.etrees, this.map);
          this.renderElans(this.elans, this.map);

          // center the map
          this.map.setCenter(this.bounds.getCenter());
          this.map.fitBounds(this.bounds);
        })
        .catch(e => {
          throw new Error(e);
        });
        this.user = {name: 'world'};

        // draw Elines on map
        this.renderElines = (elines, map) => {
          _.forEach(elines, eline => {
            this.addMarker(eline.uni1);
            this.addMarker(eline.uni2);
            this.addPath('eline', eline.uni1, eline.uni2);
          });
        };

        // draw Etrees on map
        this.renderEtrees = (etrees, map) => {
          _.forEach(etrees, etree => {
            this.addMarker(etree.root);
            _.forEach(etree.eps, (uni) => {
              this.addMarker(uni);
            });

            let unis = _.reduce(etree.eps, (unis, uni) => {
              unis.push(uni);
              return unis;
            }, [etree.root]);

            this.addPath('etree', ...unis);
          });
        };

        this.renderElans = (elans, map) => {
          _.forEach(elans, elan => {
            console.log(elan);
            _.forEach(elan.eps, (uni) => {
              this.addMarker(uni);
            });
            // NOTE should we close the line?
            const unis = angular.copy(elan.eps);
            unis.push(elan.eps[0]);
            this.addPath('elan', ...unis);
          });
        };

        this.addMarker = (uni) => {
          let [lng, lat] = JSON.parse(uni.latlng);
          angular.extend(uni, {lat: lat, lng: lng});
          this.markers.push(uni);

          // extend maps bounds
          const latlng = new google.maps.LatLng(lat, lng);
          this.bounds.extend(latlng);
        };

        this.addPath = (type, ...unis) => {
          // create a path that connect all unis we receive and add it to the right collection
          let path = _.reduce(unis, (path, uni) => {
            path.push([uni.lat, uni.lng]);
            return path;
          }, []);
          this[`${type}sPath`].push(path);
        };
      }
    });

}());