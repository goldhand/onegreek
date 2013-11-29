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
        templateUrl: 'list.html',
        controller: 'EventListCtrl',
        resolve: {
            events: function(EventService) {
                return EventService.list();
            }
        }
    });
    $routeProvider.when('/events/calendar', {
        templateUrl: 'http://localhost:8000/events/calendar/2013/11/'
    });
    $routeProvider.when('/events/calendar/rsvp', {
        templateUrl: 'http://localhost:8000/events/calendar/2013/11/?rsvp=true'
    });
    $routeProvider.when('/events/:eventId', {
        templateUrl: 'detail.html',
        controller: 'EventDetailCtrl',
        resolve: {
            event: function($route, EventService) {
                var eventId = $route.current.params.eventId;
                return EventService.get(eventId);
                }
            }
    });
    $routeProvider.otherwise({redirectTo: '/events'});
}]);

