'use strict';

/* Controllers */
eventsApp.controller('EventListCtrl', ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
    $scope.event = {};
    $http.get('/api/events/').success(function(data) {
        $scope.events = data;
    });
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

