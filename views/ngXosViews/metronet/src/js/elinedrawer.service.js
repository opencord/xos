/**
 * © OpenCORD
 *
 * Visit http://guide.xosproject.org/devguide/addview/ for more information
 *
 * Created by teone on 10/18/16.
 */

(function () {
  'use strict';

  angular.module('xos.metronet')
  .service('MetronetELineDrawer', function($rootScope, CentralOffice){
    let startUni, endUni, poly;
    let listener, moveListener = null;
    const self = this;

    this.setStartUni = (uni) => {
      startUni = uni;
    };

    this.setEndUni = (uni) => {
      endUni = uni;
    };

    this.getStartUni = () => startUni;

    this.getEndUni = () => endUni;

    this.cleanLine = () => poly ? poly.setMap(null) : false;

    this.resetMouseEventData = () => {
      startUni = null;
      endUni = null;
    };

    this.detachDrawingEvents = () => {
      
      google.maps.event.removeListener(listener);
      google.maps.event.removeListener(moveListener);

      // if line is not connecting unis, clear
      if(!self.getStartUni() || !self.getEndUni() || startUni === endUni){
        self.cleanLine();
      }
      self.resetMouseEventData();
    };

    this.attachDrawingEvents = (map) => {

      const ports = CentralOffice.getPorts();

      // attach eline marker events to ports
      _.forEach(ports, (marker) => {

        // add event listener
        marker.addListener('mousedown', function() {
          self.setStartUni(this.uni);
        });
        marker.addListener('mouseup', function() {
          self.setEndUni(this.uni);
        });
      });

      listener = google.maps.event.addDomListener(map.getDiv(), 'mousedown', (e) => {

        // the polygon
        poly = new google.maps.Polyline({map: map, clickable: true});

        // move-listener
        moveListener = google.maps.event.addListener(map, 'mousemove', (e) => {
          if(poly.getPath().length === 2){
            poly.getPath().pop();
          }
          poly.getPath().push(e.latLng);
        });
        
        //mouseup-listener
        $(window).mouseup((e) => {

          // check if we have start and end UNI
          if(startUni && endUni && startUni !== endUni){
            console.log(`Create a connection from ${startUni.name} to ${endUni.name}`);
            $rootScope.$emit('connection.details', {
              uni1: startUni,
              uni2: endUni,
              kind: 'eline',
              type: 'direct'
            });
          }
        });
      });
    };
  });
})();

