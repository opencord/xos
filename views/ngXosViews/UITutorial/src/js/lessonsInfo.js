(function () {
  'use strict';
  angular.module('xos.UITutorial')
  .service('LessonInfo', function($injector, ResponseHandler, ErrorHandler){

    this.lessonCatalogue = (id) => {
      let lessonData = [{
        id: 1,
        text: 'lesson 1 info',
        solution: 'Hello World'
      },
      {
        id: 2,
        text: 'lesson 2 info',
        solution: 'Hello World'
      },
      {
        id: 3,
        text: 'lesson 3 info',
        solution: 'Hello World'
      },
      {
        id: 4,
        text: 'lesson 4 info',
        solution: 'Hello World  '
      },
      {
       id: 5,
       text: 'lesson 5 info',
       solution: 'Hello World'

    }];

    console.log(lessonData[id]);
    return lessonData[id];
    }

  });
})();