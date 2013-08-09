'use strict';


// Declare app level module which depends on filters, and services
angular.module('indikApp', ['indikApp.filters', 'indikApp.services', 'indikApp.directives', 'indikApp.controllers', 'ngSanitize', 'ui.bootstrap']).

  
  config(['$routeProvider', function($routeProvider) {
    
    $routeProvider.when('/home', {templateUrl: createDjangoPath('templates/home.html') });
    $routeProvider.when('/indicator/:indicatorCode', {templateUrl: createDjangoPath('templates/indicator.html'), 
        controller: 'IndicatorCtlr'
    });
    //$routeProvider.when('/starred', {templateUrl: 'partials/starred.html', controller: 'ArtworksCtrl'});
    $routeProvider.otherwise({redirectTo: '/home'});
    
  
}]);
