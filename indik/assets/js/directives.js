'use strict';


/* Directives */
var directives = angular.module('indikApp.directives', []);


directives.directive('appVersion', ['version', function(version) {
  return function(scope, elm, attrs) {
    elm.text(version);
  };
}]);



directives.directive("indicatorQuery", ['$rootScope', 'indicatorsService', function($rootScope,indicatorsService){

    return {
        replace : false,
        restrict : 'A',
        templateUrl : createDjangoPath('templates/indicator_query.html'),
        link : function(scope, element, attrs){
            
            
        }
    };

}]);


directives.directive("indicatorsTable", ['$rootScope', 'indicatorsService', function($rootScope,indicatorsService){

    return {
        replace : false,
        restrict : 'A',
        templateUrl : createDjangoPath('templates/indicators_table.html'),
        link : function(scope, element, attrs){
            
            
        }
    };

}]);

directives.directive("indicatorDataTable", ['$rootScope', 'indicatorsService', function($rootScope,indicatorsService){

    return {
        replace : false,
        restrict : 'A',
        templateUrl : createDjangoPath('templates/indicator_data_table.html'),
        link : function(scope, element, attrs){
            
            
        }
    };
}]);


directives.directive("indicatorViz", ['$rootScope', 'indicatorsService', function($rootScope,indicatorsService){

    return {
        replace : false,
        restrict : 'A',
        templateUrl : createDjangoPath('templates/indicator_viz.html'),
        link : function(scope, element, attrs){
            
            
        }
    };

}]);



//DOES NOT WORK
directives.directive('selectpicker', function () {
    return {
      restrict: 'A',
      replace: false,
      link: function postLink(scope, element, attrs) {
            
          //element.selectpicker();
      }
    };
});