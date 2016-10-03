(function () {
  'use strict';

  // https://snazzymaps.com/explore
  // const mapStyles = [{"featureType":"water","elementType":"geometry","stylers":[{"color":"#e9e9e9"},{"lightness":17}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":20}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#ffffff"},{"lightness":17}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#ffffff"},{"lightness":29},{"weight":0.2}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":18}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":16}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":21}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#dedede"},{"lightness":21}]},{"elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#ffffff"},{"lightness":16}]},{"elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#333333"},{"lightness":40}]},{"elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#f2f2f2"},{"lightness":19}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#fefefe"},{"lightness":20}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#fefefe"},{"lightness":17},{"weight":1.2}]}];
  const mapStyles = [{"featureType":"administrative","elementType":"labels.text.fill","stylers":[{"color":"#444444"}]},{"featureType":"landscape","elementType":"all","stylers":[{"color":"#f2f2f2"}]},{"featureType":"poi","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"road","elementType":"all","stylers":[{"saturation":-100},{"lightness":45}]},{"featureType":"road.highway","elementType":"all","stylers":[{"visibility":"simplified"}]},{"featureType":"road.arterial","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"water","elementType":"all","stylers":[{"color":"#46bcec"},{"visibility":"on"}]}];

  angular.module('xos.metronet')
    .component('metronetMap', {
      controllerAs: 'vm',
      template: `
        <ng-map zoom="7" center="0, 0" styles="{{vm.mapStyles}}"></ng-map>
        <metronet-side-panel></metronet-side-panel>
      `,
      controller: function($q, $rootScope, _, Eline, ELan, ETree, Uni, NgMap, CentralOffice, MetronetMap, MetronetEline, MetronetListeners) {
        this.mapStyles = mapStyles;
        this.markers = [];
        this.elinesPath = [];
        this.etreesPath = [];
        this.elansPath = [];

        let startUni, endUni;

        this.bounds = new google.maps.LatLngBounds();

        $q.all([
          Uni.query().$promise,
          Eline.query().$promise,
          ELan.query().$promise,
          ETree.query().$promise,
          NgMap.getMap()
        ])
        .then(res => {
          [this.unis, this.elines, this.elans, this.etrees, this.map] = res;

          this.cos = CentralOffice.unisToCo(this.unis);

          _.forEach(this.cos, co => {
            CentralOffice.addCoToMap(co, this.map);
          });

          // TODO
          // [ ] if no result send to creation form

          // render info on the map
          MetronetEline.renderElines(this.map, this.elines);
          // this.renderEtrees(this.etrees, this.map);
          // this.renderElans(this.elans, this.map);

          // center the map
          this.map.setCenter(MetronetMap.getBounds().getCenter());
          this.map.fitBounds(MetronetMap.getBounds());

          // listeing for events
          MetronetListeners.begin(this.map);

        })
        .catch(e => {
          throw new Error(e);
        });
        this.user = {name: 'world'};

        // draw Etrees on map
        this.renderEtrees = (etrees, map) => {
          _.forEach(etrees, etree => {

            // augment with info
            etree.connectionType = 'etree';

            this.addMarker(etree.root);
            _.forEach(etree.eps, (uni) => {
              this.addMarker(uni);
            });

            let unis = _.reduce(etree.eps, (unis, uni) => {
              unis.push(uni);
              return unis;
            }, [etree.root]);

            this.addPath(etree, ...unis);
          });
        };

        this.renderElans = (elans, map) => {
          _.forEach(elans, elan => {

            // augment with info
            elan.connectionType = 'elan';

            _.forEach(elan.eps, (uni) => {
              this.addMarker(uni);
            });
            // NOTE should we close the line?
            const unis = angular.copy(elan.eps);
            unis.push(elan.eps[0]);
            this.addPath(elan, ...unis);
          });
        };

        this.addMarker = (uni) => {
          let [lng, lat] = JSON.parse(uni.latlng);
          angular.extend(uni, {lat: lat, lng: lng});

          // add markers
          const latlng = new google.maps.LatLng(lat, lng);
          const marker = new google.maps.Marker({
            position: latlng,
            map: this.map,
            icon: markerIcon,
            title: uni.name,
            optimized: false,
            uni: uni
          });
          marker.setMap(this.map);



          // extend maps bounds
          this.bounds.extend(latlng);

          // add the info window
          this.addInfoWindow(marker);
        };

        this.addPath = (connection, ...unis) => {

          // create a new Line
          const poly = new google.maps.Polyline({
            map: this.map,
            clickable: true,
            connection: connection,
            strokeColor: lineColors[connection.connectionType]
          });

          // attach a click handler
          poly.addListener('click', function() {
            $rootScope.$emit('connection.details', connection);
          });

          // attach all the point to the line
          const latlng = (uni) => {
            return {
              lat: () => uni.lat,
              lng: () => uni.lng,
            };
          };
          _.forEach(unis, uni => poly.getPath().push(latlng(uni)))
        };

      }
    });

}());