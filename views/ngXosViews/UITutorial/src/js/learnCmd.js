(function () {
  'use strict';
  angular.module('xos.UITutorial')
  .service('LearnCmd', function(LessonInfo, $cookies){


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

    this.getLessonIdFromCookie = ()=>{
      let lessonId = $cookies.get('lessonId') ? $cookies.get('lessonId') : {};
      return lessonId;
    };

    this.getNextLesson = (cmd,arg,done)=>{
      let lessonId = this.getLessonIdFromCookie();
      if(_.isEmpty(lessonId))
      {
        done(this.getCurrentLesson(0));
      }
      else{
        done(this.getCurrentLesson(parseInt(lessonId)+1));
      }
    };

    this.getPreviousLesson = (cmd,arg,done)=>{
      let lessonId = this.getLessonIdFromCookie();
      if(lessonId!==0) {
        done(this.getCurrentLesson(parseInt(lessonId) - 1));
      }
      else{
        done('This is the first Lesson');
      }
    };

    this.setup = (shell) => {
      this.shell = shell;
      this.nextLesson(shell);
      this.prevLesson(shell);
    };

  });
})();