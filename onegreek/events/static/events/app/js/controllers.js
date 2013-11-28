'use strict';

/* Controllers */

var eventsControllers = angular.module('eventsControllers', []);

eventsControllers.controller('EventGlobalCtrl', function ($scope, $rootScope, $location, $http, GlobalService) {
    var failureCb = function (status) {
        console.log(status);
    };
    $scope.globals = GlobalService;

    $scope.initialize = function (is_authenticated, user_id, host) {
        if(is_authenticated) {
            var api_url = "/api/users/";
            var url = api_url + user_id + "/";
            $http.get('/api/users/' + user_id + '/').success(function(user_data) {
                $scope.globals.user = user_data;
                console.log(user_data);
                console.log($scope.globals.user.status);
            });
        }
        else {
            $scope.globals.user = {
                id: false,
                chapter_id: false,
                status: false
            }
        }

        $scope.globals.is_authenticated = is_authenticated;
        $scope.globals.host = host;
    };
});


eventsControllers.controller('EventListCtrl', [
    '$scope',
    '$http',
    '$modal',
    'filterFilter',
    'EventService',
    'GlobalService',
    'events',
    function (
        $scope,
        $http,
        $modal,
        filterFilter,
        EventService,
        GlobalService,
        events
        ) {
        $scope.event = {};
        $scope.events = events;
        $scope.globals = GlobalService;
        $scope.globals.events = events;

        $scope.filterForGroup = function(status) {
            if(status=="all"){
                $scope.events = $scope.globals.events;
            } else {
                $scope.events = filterFilter($scope.globals.events, {status: status});
            }
        };
        $scope.tabs = [
            {
                title:"All",
                content:"All Chapter Events",
                status: "all",
                disabled: false,
                active: $scope.globals.user.status != "rush",
                hidden: false
            },
            {
                title:"Active",
                content:"Active Member Events",
                status: "active",
                disabled: $scope.globals.user.status != "active",
                active: false,
                hidden: $scope.globals.user.status != "active"
            },
            {
                title:"Pledge",
                content:"Pledge Events",
                status: "pledge",
                //disabled: $scope.globals.user.status != "pledge",
                disabled: false,
                active: false,
                hidden: $scope.globals.user.status == "rush"
            },
            {
                title:"Rush",
                content:"Rush Events",
                status: "rush",
                disabled: false,
                //disabled: $scope.globals.user.status != "rush",
                active: $scope.globals.user.status == "rush",
                hidden: false
            }
        ];


        $scope.Search = undefined;

        $scope.submit = function() {
            EventService.save($scope.event).then(function(data) {
                $scope.globals.events.push(data);
                $scope.event = {};
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

eventsApp.controller('EventDetailCtrl', [
    '$scope', '$http', '$modal', '$routeParams', 'EventService', 'GlobalService', 'event',
    function ($scope, $http, $modal, $routeParams, EventService, GlobalService, event) {

        $scope.globals = GlobalService;
        $scope.event = event;
        $scope.event.guest_list = {
            attendees: [],
            rsvps: [],
            display: false
        };

        $scope.getAttendees = function() {
            $http.get('/api/events/' + event.id + '/?nest=true').success(function(data) {
                console.log(data);
                $scope.event.guest_list = {
                    attendees: data.get_attendees,
                    rsvps: data.get_rsvps_not_attendees,
                    display: true
                };
            });
        };


        if ($scope.globals.user.is_chapter_admin) {
        } else {
            $scope.submit = function () {};
        }

        $scope.getRsvp = function() {
            $http.get($scope.event.rsvp_url).success(function(data) {
                $scope.event.rsvp = data;
                console.log(data);
            });
        };
        $scope.getRsvp();

        $scope.postRsvp = function() {
            $http.post($scope.event.rsvp_url, {}).success(function(data) {
                    $scope.event.rsvp = data;
                    console.log(data);
                });
        };
        $scope.postAttend = function(attendee) {
            $http.post($scope.event.attend_url + '?attendee=' + attendee.id, {}).success(function(data) {
                console.log(data);
                if (data.attend) {
                    $scope.event.guest_list.attendees.push(attendee);
                    var index = $scope.event.guest_list.rsvps.indexOf(attendee);
                    $scope.event.guest_list.rsvps.splice(index, 1);
                } else {
                    $scope.event.guest_list.rsvps.push(attendee);
                    index = $scope.event.guest_list.attendees.indexOf(attendee);
                    $scope.event.guest_list.attendees.splice(index, 1);
                }
            });
        };

        $scope.submit = function() {
            EventService.update($scope.event).then(function(data) {
                $scope.event = data;
                $scope.getRsvp();
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
                $scope.globals.events.push(data);
                $scope.event = {};
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
