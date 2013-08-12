'use strict';

/* Services */
var services = angular.module('indikApp.services', []);

// Demonstrate how to register services
// In this case it is a simple value service.
services
  .value('version', '0.1');


services
  .factory('baseUrls', function(){
    return {
        indicatorsUrl : 'indicators/',
        indicatorBaseUrl : 'indicators/',
        
        
        getIndicatorDataUrl : function(code){
            return this.indicatorBaseUrl + code + "/data/";
        },

        getIndicatorUrl : function(code){
            return this.indicatorBaseUrl + code + "/";
        },

        getIndicatorClassesUrl : function(code){
            return this.indicatorBaseUrl + code + "/classes/";
        }
        
        
    };
});  


services
.factory('indicatorsService', ['$http', '$q','baseUrls', function($http, $q, baseUrls) {
  return {
    
    indicatorsCache : [],
    
    getIndicators : function(){
        var deferred = $q.defer();
        var self = this;
        $http.get(baseUrls.indicatorsUrl).success(function(data){
            deferred.resolve(data.data);
            self.indicatorsCache = data.data;
        }).error(function(){
            deferred.reject("An error occured while fetching indicators list");
        });
        return deferred.promise;
    },

    getIndicator : function(code){
        var deferred = $q.defer();
        var self = this;
        var url = baseUrls.getIndicatorUrl(code);
        $http.get(url).success(function(data){
            deferred.resolve(data.data);
        }).error(function(){
            deferred.reject("An error occured while fetching indicators list");
        });
        return deferred.promise;
    },

    getIndicatorClasses : function(code){
        var deferred = $q.defer();
        var self = this;
        var url = baseUrls.getIndicatorClassesUrl(code);
        $http.get(url).success(function(data){
            deferred.resolve(data.data);
        }).error(function(){
            deferred.reject("An error occured while fetching indicators list");
        });
        return deferred.promise;
    },

    getIndicatorData : function(code, params){

        var params = params || {};
        var config = { params : params };

        var deferred = $q.defer();
        var self = this;
        var url = baseUrls.getIndicatorDataUrl(code);
        $http.get(url, config).success(function(data){
            deferred.resolve(data.data);
        }).error(function(){
            deferred.reject("An error occured while fetching indicators list");
        });
        return deferred.promise;
    },


    buildQueryParams : function(queryModel){

        //var out = { 'resolve_classes' : false };
        var out = { };
        if(queryModel.resolveClasses){
            out['resolve_classes'] = true;
        }

        //filters
        var filtersParams = [];
        var filters = queryModel.filters;
        for(var i=0,n=filters.length;i<n;i++){
            var flt = filters[i];
            if(flt.field && flt.value) {
                var param = flt.field+flt.operator + ":" + flt.value;
                filtersParams.push(param);
            }

        }
        out['filter'] = filtersParams;
        
        //aggregations
        if(queryModel.aggregation){
            out['aggregation'] = queryModel.aggregation;

            //filters
            var groupByPieces = [];
            var groupBy = queryModel.groupBy;
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
    
    
  }
}]);

