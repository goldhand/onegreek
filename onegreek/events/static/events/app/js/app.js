'use strict';


// Declare app level module which depends on filters, and services
var eventsApp = angular.module('eventsApp', [
    'ui.bootstrap',
    'ngCookies',
    'ngRoute',
    'eventsControllers',
    'eventServices'
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
    $routeProvider.when('/events', {
        templateUrl: '/static/events/app/partials/list.html',
        controller: 'EventListCtrl',
        resolve: {
            events: function(EventService) {
                return EventService.list();
            }
        }
    });
    $routeProvider.when('/events/:eventId', {
        templateUrl: 'detail.html',
        controller: 'EventDetailCtrl'
    });
    $routeProvider.otherwise({redirectTo: '/events'});
}]);

