'use strict';

/* Controllers */

var controllersModule = angular.module('indikApp.controllers', []);

controllersModule
  .controller('MainCtrl', [ '$scope', 'indicatorsService', function($scope, indicatorsService) {
    
    $scope.indicators = [];

    indicatorsService.getIndicators().then(function(data){
        $scope.indicators = data;
    });

  }]);





controllersModule
  .controller('IndicatorCtlr', [ '$scope', '$routeParams', 'indicatorsService', function($scope, $routeParams, indicatorsService) {
    
    
    $scope.indicatorCode = $routeParams.indicatorCode;
    $scope.filterOperators = [
        {'name': 'uguale a', 'value' : ''},
        {'name': 'maggiore di ', 'value' : '__gt'},
        {'name': 'minore di', 'value' : '__lt'},
    ];

    $scope.aggregationOperators = [
        {'name': 'Nessuna aggregazione', 'value' : ''},
        {'name': 'Somma', 'value' : 'sum'},
        {'name': 'Media', 'value' : 'avg'},
        {'name': 'Min', 'value' : 'min'},
        {'name': 'Max', 'value' : 'max'},
    ];


    $scope.currentData = [];
    $scope.currentIndicator = null;
    $scope.currentClasses = {};


    $scope.queryModel = {
        aggregation: '',
        groupBy : [],
        filters : []
    };


    $scope.state = { 
        loading:false,
        querySync : false
    };


    $scope.currentParams = {};

    $scope.buildQueryParams = function(){

        //var out = { 'resolve_classes' : false };
        var out = { };

        //filters
        var filtersParams = [];
        var filters = $scope.queryModel.filters;
        for(var i=0,n=filters.length;i<n;i++){
            var flt = filters[i];
            if(flt.field && flt.value) {
                var param = flt.field+flt.operator + ":" + flt.value;
                filtersParams.push(param);
            }

        }
        out['filter'] = filtersParams;
        
        //aggregations
        if($scope.queryModel.aggregation){
            out['aggregation'] = $scope.queryModel.aggregation;

            //filters
            var groupByPieces = [];
            var groupBy = $scope.queryModel.groupBy;
            for(var i=0,n=groupBy.length;i<n;i++){
                var gb = groupBy[i];
                if(gb.name) {
                    groupByPieces.push(gb.name);
                }

            }
            out['group_by'] = groupByPieces.join(":");


        } 


        return out;

    }

    $scope.getIndicator = function(){
        indicatorsService.getIndicator($scope.indicatorCode ).then(function(data){
            $scope.currentIndicator = data[0];
        });
    };

    $scope.getIndicatorClasses = function(){
        indicatorsService.getIndicatorClasses($scope.indicatorCode ).then(function(data){
            $scope.currentClasses = data[0];
        });
    };

    $scope.getData = function(){
        $scope.state.loading = true;
        var queryParams = $scope.buildQueryParams();
        indicatorsService.getIndicatorData($scope.indicatorCode, queryParams ).then(function(data){
            $scope.currentData = data;
            $scope.state.loading = false;
            $scope.state.querySync = true;

        });
    };


    

    $scope.addFilter = function(){
        var flt = {'field' : '', 'operator' : '',  'value': '' };
        $scope.queryModel.filters.push(flt);

    };

    $scope.removeFilter = function(index){
        $scope.queryModel.filters.splice(index, 1);

    };

    $scope.addGroupBy = function(){
        var gb = {name:''};
        $scope.queryModel.groupBy.push(gb);

    };

    $scope.removeGroupBy = function(index){
        $scope.queryModel.groupBy.splice(index, 1);
    };

    $scope.isClass = function(fieldName){

        return ($scope.currentClasses[fieldName] !== undefined)

    }


    $scope.$watch('queryModel', function(nv){
            var newParams = $scope.buildQueryParams();
            if(newParams != $scope.currentParams) $scope.currentParams = newParams;
        }, 
        true);

    $scope.$watch('currentParams', function(nv){
            $scope.state.querySync = false;
        }, 
        true);

    
    $scope.getIndicatorClasses();
    $scope.getIndicator();


    /*
    $scope.currentIndicator = null;
    


    $scope.currentIndicator = indicator;
    
    */



  }]);