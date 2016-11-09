(function () {
  'use strict';

  angular.module('xos.metronet')
  .service('MetronetEtreeDrawer', function(
    $rootScope,
    CentralOffice,
    MetronetPort,
    MetronetPortSelected){

    const self = this;

    let rootUni, endUni, rootUniMarker, listener;

    let paths = [], moveListeners = [], eps = [];

    this.resetMouseEventData = () => {
      rootUni = null;
      rootUniMarker = null;
    }

    this.setRootUni = (marker) => {
      marker.setIcon(MetronetPortSelected)

      rootUniMarker = marker;
      rootUni = marker.uni;
    };

    this.cleanLine = () => {
      _.forEach(paths, p => {
        p.setMap(null);
      })
    };

    this.resetRootMarker = () => {
      if(rootUniMarker){
        rootUniMarker.setIcon(MetronetPort);
      }
      // NOTE works, but it is not the right place to call this method
      this.resetMouseEventData();
    }

    this.detachDrawingEvents = () => {
      if(!rootUni || eps.length === 0){
        this.cleanLine();
        this.resetRootMarker();
      }
      if(rootUni && eps.length > 0){
        $rootScope.$emit('connection.details', {
          root: rootUni,
          eps: eps,
          kind: 'etree',
          type: 'ethernet'
        });
      }
    };

    this.attachDrawingEvents = (map) => {
      const ports = CentralOffice.getPorts();

      // attach etree marker events to ports
      _.forEach(ports, (marker) => {

        // add event listener
        marker.addListener('mousedown', function() {
          if(!rootUni){
            self.setRootUni(this);
          }
        });

        marker.addListener('mouseup', function() {
          eps.push(this.uni)
        });
      });

      // line drawer
      listener = google.maps.event.addDomListener(map.getDiv(), 'mousedown', (e) => {
        let poly = new google.maps.Polyline({map: map, clickable: true});
        paths.push(poly);

        // move-listener
        let moveListener = google.maps.event.addListener(map, 'mousemove', (e) => {
          if(poly.getPath().length === 2){
            poly.getPath().pop();
          }
          poly.getPath().push(e.latLng);
        });
        moveListeners.push(moveListener);

        //mouseup-listener
        $(window).mouseup((e) => {
          console.log('remove moveListener');
          google.maps.event.removeListener(moveListener);
        });
      });
    }
  });
})();