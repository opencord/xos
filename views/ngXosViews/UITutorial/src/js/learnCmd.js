(function () {
  'use strict';
  angular.module('xos.UITutorial')
  .service('LearnCmd', function($injector, ResponseHandler, ErrorHandler,LessonInfo,$cookies){


    this.getCurrentLesson = (id)=>{
      var details = LessonInfo.lessonCatalogue(id);
      $cookies.put('lessonId', id);
      return JSON.stringify(details);
    };

    this.nextLesson = (shell) => {
      this.shell = shell;
      shell.setCommandHandler('next', {
        exec: this.getNextLesson,
      });
    }

    this.prevLesson = (shell) => {
      this.shell = shell;
      shell.setCommandHandler('prev', {
        exec: this.getPreviousLesson,
      });
    }

    this.getNextLesson = (cmd,arg,done)=>{
      let lessonId = $cookies.get('lessonId') ? angular.fromJson($cookies.get('lessonId')) : {};
      if(!lessonId===undefined)
      {
        done(this.getCurrentLesson(0));
      }
      else{
        done(this.getCurrentLesson(lessonId+1));
      }
    };

    this.getPreviousLesson = (cmd,arg,done)=>{
      let lessonId = $cookies.get('lessonId') ? angular.fromJson($cookies.get('lessonId')) : {};
      if(lessonId!==0) {
        done(this.getCurrentLesson(lessonId - 1));
      }
      else{
        done('This is the first Lesson');
      }
    };

    this.setup = (shell,done) => {
      this.shell = shell;
      this.nextLesson(shell);
      this.prevLesson(shell);
    };

  });
})();