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
    'EventService',
    'GlobalService',
    'events',
    function (
        $scope,
        $http,
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


eventsControllers.controller('MyFormCtrl', [
    '$scope',
    '$http',
    '$modal',
    'GlobalService',
    'EventService',
    function (
        $scope,
        $http,
        $modal,
        GlobalService,
        EventService
        ) {
    $scope.event = {};
    $scope.globals = GlobalService;
    $scope.submit = function() {
        EventService.save($scope.event).then(function(data) {
            $scope.event = data;
            $scope.globals.events.push(data);
        }, function(status) {
            console.log(status);
        });
    };

        $scope.openModal = function () {
            var modalInstance = $modal.open({
                templateUrl: 'newEventModal.html',
                controller: 'ModalInstanceCtrl',
                windowClass: 'full-screen-modal',
                resolve: {
                    event: function () {
                        return $scope.event;
                    }
                }
            });

            modalInstance.result.then(function (newEvent) {
                $scope.event = newEvent;
                $scope.submit();
            }, function () {});
        };
}]);

eventsControllers.controller('ModalInstanceCtrl', [
    '$scope',
    '$timeout',
    '$modalInstance',
    'event',
    function (
        $scope,
        $timeout,
        $modalInstance,
        event
        ) {
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
        $scope.mstep = 1;
        $scope.ismeridian = true;

        $scope.event = event;

            $scope.ok = function () {
                $modalInstance.close($scope.event);
            };

            $scope.cancel = function () {
                $modalInstance.dismiss('cancel');
            };
    }]);
