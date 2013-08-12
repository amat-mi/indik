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
        filters : [],
        resolveClasses : false
    };


    $scope.state = { 
        loading:false,
        querySync : false
        
    };


    $scope.currentParams = {};

    

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
        var queryParams = $scope.currentParams;
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

    $scope.allowSimpleChart = function(){
        if ($scope.queryModel.groupBy.length !== 1) return false;
        if (!$scope.queryModel.groupBy[0].name) return false;
        return true;

    }    


    $scope.$watch('queryModel', function(nv){
            var newParams = indicatorsService.buildQueryParams($scope.queryModel);
            if(newParams != $scope.currentParams) $scope.currentParams = newParams;
        }, 
        true);

    $scope.$watch('currentParams', function(nv){
            $scope.state.querySync = false;
        }, 
        true);

    
    $scope.getIndicatorClasses();
    $scope.getIndicator();


  }]);