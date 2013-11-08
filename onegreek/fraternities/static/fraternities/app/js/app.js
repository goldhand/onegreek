'use strict';


// Declare app level module which depends on filters, and services
var eventsApp = angular.module('eventsApp', [
    'ui.bootstrap',
    'ngCookies',
    'ngRoute'
    //'myApp.filters',
    //'myApp.services',
    //'myApp.directives',
    //'myApp.controllers'
    ],
    function($interpolateProvider) {
        $interpolateProvider.startSymbol("{[{");
        $interpolateProvider.endSymbol("}]}");
    }
);

eventsApp.config(['$routeProvider', '$httpProvider', function($routeProvider, $httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $routeProvider.when('/', {templateUrl: 'static/events/app/partials/demo.html'});
    $routeProvider.otherwise({redirectTo: '/'});
}]);

