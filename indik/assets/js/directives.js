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

directives.directive("indicatorChart", ['$rootScope', 'indicatorsService', function($rootScope,indicatorsService){

    return {
        replace : false,
        restrict : 'A',
        scope : {
            valueAttr:"=",
            labelAttr:"=",
            data:"="

        },
        templateUrl : createDjangoPath('templates/indicator_chart.html'),
        link : function(scope, element, attrs){


            
            var chart;
            var updateChart = function(){

                if(!chart){ console.log("www");return };
             

                console.log(1);
                chart = chart
                    .y(function(d) { return d[scope.valueAttr] })
                    .x(function(d) { return d[scope.labelAttr] });
                
                
                
                var svg = $('svg', element)[0];
                
                var data = [{key:"ss", values : scope.data }];
                
                d3.select(svg)
                    .datum(data)
                    .transition().duration(500)
                    .call(chart);

            };

            nv.addGraph(function() {
                chart = nv.models.discreteBarChart()
                    //.staggerLabels(true)
                    .tooltips(false)
                    .showValues(true)

                
                  nv.utils.windowResize(chart.update); 

                  return chart;
            });


            
            

            scope.$watch('data', function(){
                console.log("data changed")
                console.log(scope.valueAttr, scope.labelAttr);
                updateChart();

            })

            scope.$watch('valueAttr', function(){
               console.log(scope.valueAttr, scope.labelAttr);
               
               

            })

            

            
            
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