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
  .service('MetronetListeners', function($rootScope, MetronetELineDrawer){

    this.begin = (map) => {
      // hold shift to enable draw eline
      // hold ctrl to draw etree
      // hold option/alt to draw e lan
      
      // TODO move all eline logic inside ElineDrawerService
      window.onkeyup = (e) => {
        if(e.key === 'Shift'){
          map.setOptions({draggable: true});
          // if line is not connecting unis, clear
          if(!MetronetELineDrawer.getStartUni() || !MetronetELineDrawer.getEndUni()){
            MetronetELineDrawer.cleanLine();
          }
          MetronetELineDrawer.resetMouseEventData();
          MetronetELineDrawer.detachDrawingEvents();
        };
      };
      window.onkeydown = (e) => {
        if(e.key === 'Shift'){
          MetronetELineDrawer.attachDrawingEvents(map);
          map.setOptions({draggable: false});
        };
      };
    }
  })
  .service('MetronetELineDrawer', function($rootScope, CentralOffice){
    let drawingEnabled = false;
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

    this.isDrawingEnabled = () => drawingEnabled;

    this.enableDrawing = () => drawingEnabled = true;

    this.disableDrawing = () => drawingEnabled = false;

    this.resetMouseEventData = () => {
      drawingEnabled = false;
      startUni = null;
      endUni = null;
    };

    this.detachDrawingEvents = () => {
      this.disableDrawing();
      google.maps.event.removeListener(listener);
      google.maps.event.removeListener(moveListener);

      const ports = CentralOffice.getPorts();

      _.forEach(ports, (marker) => {
        CentralOffice.addInfoWindowListener(marker);
      });
    };

    this.attachDrawingEvents = (map) => {
      this.enableDrawing();

      const ports = CentralOffice.getPorts();
      const cos = CentralOffice.getCos();

      // attach eline marker events to ports
      _.forEach(ports, (marker) => {

        // clear existing listener
        google.maps.event.clearInstanceListeners(marker);

        // add event listener
        marker.addListener('mousedown', function() {
          // for Elines
          if(self.isDrawingEnabled()){
            self.setStartUni(this.uni);
          }
        });
        marker.addListener('mouseup', function() {
          // for Elines
          if(self.isDrawingEnabled()){
            self.setEndUni(this.uni);
          }
        });
      });

      // attach eline marker events to COs
      _.forEach(cos, (marker) => {
        marker.addListener('mouseover', function() {
          if(self.isDrawingEnabled()){
            if(this.portShown !== true){
              // draw ports
              CentralOffice.showPortsFromCo(this, map);
              // NOTE emitting an event to avoid circular dependency
              $rootScope.$emit('metronet.redrawConnections', map);
            }
          }
        });
      });

      listener = google.maps.event.addDomListener(map.getDiv(), 'mousedown', (e) => {
        console.log('Eline Mouse Down');
        // do it with shift pressed only

        // the polygon
        poly = new google.maps.Polyline({map: map, clickable: true, info: 'test'});

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
          if(startUni && endUni){
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

