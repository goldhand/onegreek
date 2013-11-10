'use strict';

/* Controllers */

var eventsControllers = angular.module('eventsControllers', []);

eventsControllers.controller('AppController', function ($scope, $rootScope, $location, GlobalService) {
    var failureCb = function (status) {
        console.log(status);
    };
    $scope.globals = GlobalService;

    $scope.initialize = function (is_authenticated) {
        $scope.globals.is_authenticated = is_authenticated;
    };
});


eventsControllers.controller('EventListCtrl', [
    '$scope',
    '$http',
    '$timeout',
    'EventService',
    'GlobalService',
    'events',
    function (
        $scope,
        $http,
        $timeout,
        EventService,
        GlobalService,
        events
        ) {
        $scope.event = {};
        $scope.events = events;
        $scope.globals = GlobalService;
        $scope.globals.events = events;

        //$http.get('/api/events/').success(function(data) {
        //    $scope.events = data;
        //});
        $scope.submit = function() {
            EventService.save($scope.event).then(function(data) {
                $scope.event = data;
                $scope.events.push(data);
            }, function(status) {
                console.log(status);
            });
        //    $http.post('/api/events/', $scope.event).success(function(event_data) {
        //        $scope.events.push(event_data);
        //    });
        };
        $scope.openStart = function() {
            $timeout(function() {
                $scope.openedStart = true;
            });
        };
        $scope.openEnd = function() {
            $timeout(function() {
                $scope.openedEnd = true;
            });
        };
        $scope.dateOptions = {
            'year-format': "'yyyy'",
            'month-format': "'mm'",
            'starting-day': 1
        };
        $scope.hstep = 1;
        $scope.mstep = 15;
        $scope.ismeridian = true;

        $scope.Search = undefined;

}]);

eventsApp.controller('EventDetailCtrl', ['$scope', '$http', '$routeParams', function ($scope, $http, $routeParams) {
    $http.get('/api/events/' + $routeParams.eventId + '/').success(function(data) {
        $scope.event = data;
    });
    $scope.submit = function() {
        $http.post('/api/events/' + $routeParams.eventId + '/', $scope.event).success(function(event_data) {
            $scope.events.push(event_data);
        });
    };
}]);


eventsApp.controller('MyFormCtrl', ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
    $scope.event = {};
    $scope.submit = function() {
        $http.post('/api/events/', $scope.event).success(function(event_data) {
            $scope.events.push(event_data);
        });
    };

    $scope.openStart = function() {
        $timeout(function() {
            $scope.openedStart = true;
        });
    };
    $scope.openEnd = function() {
        $timeout(function() {
            $scope.openedEnd = true;
        });
    };
    $scope.dateOptions = {
        'year-format': "'yyyy'",
        'month-format': "'mm'",
        'starting-day': 1
    };
    $scope.hstep = 1;
    $scope.mstep = 15;
    $scope.ismeridian = true;
}]);

