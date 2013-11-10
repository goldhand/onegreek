'use strict';


// Declare app level module which depends on filters, and services
var usersApp = angular.module('eventsApp', [
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

usersApp.config(['$routeProvider', '$httpProvider', function($routeProvider, $httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $routeProvider.when('/users', {templateUrl: '/static/users/app/partials/list.html'});
    $routeProvider.when('/users/:userId', {templateUrl: 'detail.html', controller: 'UserDetailCtrl'});
    $routeProvider.otherwise({redirectTo: '/users'});
}]);

