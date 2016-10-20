/**
 * Collection of helpers for xos tests
 */

/* exported clickElement */
/* eslint-disable angular/ng_document_service */

const clickElement = function (el){
  const ev = document.createEvent('MouseEvent');
  ev.initMouseEvent(
    'click',
    true /* bubble */, true /* cancelable */,
    window, null,
    0, 0, 0, 0, /* coordinates */
    false, false, false, false, /* modifier keys */
    0 /*left*/, null
  );
  el.dispatchEvent(ev);
};

describe('Matchers inclusion', () => {
  beforeEach(function(){
    jasmine.addMatchers({
      toBeInstanceOf: function() {

        return {
          compare: (actual, expected) => {
            // const actual = actual;
            const result = {};
            result.pass = actual instanceof expected.constructor;

            result.message = 'Expected ' + actual + ' to be instance of ' + expected;

            return result;
          },
          negativeCompare: (actual, expected) => {
            // const actual = actual;
            const result = {};
            result.pass = actual instanceof expected.constructor === false;

            result.message = 'Expected ' + actual + ' to be instance of ' + expected;

            return result;
          }
        }
      }
    });
  });
});
console.log('---------------------- Test Helpers Loaded!! -----------------------');
