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
    '$window',
    'filterFilter',
    'EventService',
    'GlobalService',
    'events',
    function (
        $scope,
        $http,
        $modal,
        $window,
        filterFilter,
        EventService,
        GlobalService,
        events
        ) {
        $scope.event = {};
        $scope.events = events;
        $scope.globals = GlobalService;
        $scope.globals.events = events;

        $scope.globals.getEvents = function() {
            $http.get('/api/events').success(function(data) {
                $scope.events = data;
            });
        };


        $scope.formatCalendarEvents = function(events) {
            angular.forEach(events, function(event) {
                event.start = new Date(event.start);
                event.end = new Date(event.end);
                event.url = '#events/' + event.id;
            });
        };
        $scope.formatCalendarEvents($scope.events);

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
                hidden: false,
                calendar: "allCalendar"
            },
            {
                title:"Active",
                content:"Active Member Events",
                status: "active",
                disabled: $scope.globals.user.status != "active",
                active: false,
                hidden: $scope.globals.user.status != "active",
                calendar: "activeCalendar"
            },
            {
                title:"Pledge",
                content:"Pledge Events",
                status: "pledge",
                //disabled: $scope.globals.user.status != "pledge",
                disabled: $scope.globals.user.status == "active_pending",
                active: false,
                hidden: $scope.globals.user.status == "rush",
                calendar: "pledgeCalendar"
            },
            {
                title:"Rush",
                content:"Rush Events",
                status: "rush",
                disabled: $scope.globals.user.status == "active_pending",
                //disabled: $scope.globals.user.status != "rush",
                active: $scope.globals.user.status == "rush",
                hidden: false,
                calendar: "rushCalendar"
            }
        ];


        $scope.Search = undefined;

        $scope.submit = function() {
            EventService.save($scope.event).then(function(data) {
                $scope.globals.events.push(data);
                console.log();
                if($scope.event.redirect) {
                    console.log($scope.event);
                    var target = '/gallery/upload/' + data.ctype_id + '/' + data.id + '/';
                    $window.location.href = target;
                }
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
                console.log(newEvent);
                $scope.submit();
            }, function () {});
        };

        $scope.openEventModal = function (event) {
            var modalInstance = $modal.open({
                templateUrl: 'detail.html',
                controller: 'EventDetailCtrl',
                windowClass: 'full-screen-modal',
                resolve: {
                    event: function () {
                        return event;
                    }
                }
            });

            modalInstance.result.then(function (newEvent) {
                $scope.event = newEvent;
                console.log(newEvent);
                $scope.submit();
            }, function () {});
        };




        var date = new Date();
        var d = date.getDate();
        var m = date.getMonth();
        var y = date.getFullYear();
        /* event source that pulls from google.com */
        $scope.eventSource = {
            url: "http://www.google.com/calendar/feeds/usa__en%40holiday.calendar.google.com/public/basic",
            className: 'gcal-event',           // an option!
            currentTimezone: 'America/Chicago' // an option!
        };

        /* event source that calls a function on every view switch */
        $scope.eventsF = function (start, end, callback) {
            var s = new Date(start).getTime() / 1000;
            var e = new Date(end).getTime() / 1000;
            var m = new Date(start).getMonth();
            var events = [{title: 'Feed Me ' + m,start: s + (50000),end: s + (100000),allDay: false, className: ['customFeed']}];
            callback(events);
        };

        $scope.calEventsExt = {
            color: '#f00',
            textColor: 'yellow',
            events: [
                {type:'party',title: 'Lunch',start: new Date(y, m, d, 12, 0),end: new Date(y, m, d, 14, 0),allDay: false},
                {type:'party',title: 'Lunch 2',start: new Date(y, m, d, 12, 0),end: new Date(y, m, d, 14, 0),allDay: false},
                {type:'party',title: 'Click for Google',start: new Date(y, m, 28),end: new Date(y, m, 29),url: 'http://google.com/'}
            ]
        };
        /* alert on eventClick */
        $scope.alertEventOnClick = function( event, jsEvent, view ){
            $scope.$apply(function(){
                jsEvent.preventDefault();
                console.log('event clicked');
                $scope.alertMessage = ('Day Clicked ' + date);
            });
        };
        /* alert on Drop */
        $scope.alertOnDrop = function(event, dayDelta, minuteDelta, allDay, revertFunc, jsEvent, ui, view){
            $scope.$apply(function(){
                $scope.alertMessage = ('Event Droped to make dayDelta ' + dayDelta);
            });
        };
        /* alert on Resize */
        $scope.alertOnResize = function(event, dayDelta, minuteDelta, revertFunc, jsEvent, ui, view ){
            $scope.$apply(function(){
                $scope.alertMessage = ('Event Resized to make dayDelta ' + minuteDelta);
            });
        };
        /* add and removes an event source of choice */
        $scope.addRemoveEventSource = function(sources,source) {
            var canAdd = 0;
            angular.forEach(sources,function(value, key){
                if(sources[key] === source){
                    sources.splice(key,1);
                    canAdd = 1;
                }
            });
            if(canAdd === 0){
                sources.push(source);
            }
        };
        /* add custom event*/
        $scope.addEvent = function() {
            $scope.events.push({
                title: 'Open Sesame',
                start: new Date(y, m, 28),
                end: new Date(y, m, 29),
                className: ['openSesame']
            });
        };
        /* remove event */
        $scope.remove = function(index) {
            $scope.events.splice(index,1);
        };
        /* Change View */
        $scope.changeView = function(view,calendar) {
            calendar.fullCalendar('changeView',view);
        };
        /* Change View */
        $scope.renderCalendar = function(calendar) {
            calendar.fullCalendar('render');
        };
        $scope.rerenderCalendar = function(calendar) {
            calendar.fullCalendar('renderEvents');
        };


        /* event sources array*/
        $scope.eventSources = [$scope.events];


        /* config object */
        $scope.uiConfig = {
            calendar:{
                height: 450,
                editable: true,
                header:{
                    left: 'title',
                    center: '',
                    right: 'month agendaWeek agendaDay today prev,next'
                },
                dayClick: $scope.alertEventOnClick,
                eventDrop: $scope.alertOnDrop,
                eventResize: $scope.alertOnResize,
                defaultView: 'agendaWeek'
            }
        };




}]);






eventsApp.controller('EventDetailCtrl', [
    '$scope', '$http', '$modal', '$routeParams', '$location', 'EventService', 'GlobalService', 'event',
    function ($scope, $http, $modal, $routeParams, $location, EventService, GlobalService, event) {

        $scope.globals = GlobalService;
        $scope.event = event;
        $scope.event.guest_list = {
            attendees: [],
            rsvps: [],
            all: [],
            display: false
        };

        $scope.getAttendees = function() {
            $http.get('/api/events/' + event.id + '/?nest=true').success(function(data) {
                console.log(data);
                $scope.event.guest_list = {
                    attendees: data.get_attendees,
                    rsvps: data.get_rsvps_not_attendees,
                    all: data.get_rsvps,
                    display: true
                };
            });
        };

        $scope.getImages = function(ctype, obj) {
            $http.get('/api/images/?ctype=' + ctype + '&obj=' + obj).success(function(data) {
                $scope.event.images = data;
            });
        };


        $scope.getAttendees();
        $scope.getImages($scope.event.ctype_id, $scope.event.id);

        $scope.getRsvp = function() {
            $http.get($scope.event.rsvp_url).success(function(data) {
                $scope.event.rsvp = data;
            });
        };
        $scope.getRsvp();

        $scope.postRsvp = function() {
            $http.post($scope.event.rsvp_url, {}).success(function(data) {
                    $scope.event.rsvp = data;
                });
        };
        $scope.postAttend = function(attendee) {
            $http.post($scope.event.attend_url + '?attendee=' + attendee.id, {}).success(function(data) {
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
                $scope.getAttendees();
                $scope.getImages($scope.event.ctype_id, $scope.event.id);
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

            modalInstance.result.then(function (newEvent, redirect) {
                $scope.event = newEvent;
                $scope.submit(redirect);
            }, function () {});
        };
        $scope.deleteEvent = function () {
            $http.post('/events/' + $scope.event.id + '/delete/', '').success(function() {
                $scope.globals.getEvents();
                $location.path('/events');
            })
        }

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
                $scope.event.redirect = false;
                $modalInstance.close($scope.event);
            };
            $scope.addImages = function () {
                $scope.event.redirect = true;
                $modalInstance.close($scope.event);
            };

            $scope.cancel = function () {
                $modalInstance.dismiss('cancel');
            };
    }]);












//***************************************

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
        $scope.submit = function(redirect) {
            EventService.save($scope.event).then(function(data) {
                $scope.globals.events.push(data);
                $scope.event = {};
                if(redirect) {
                    console.log('redirect');
                    //var target = data.ctype_id + '/' + data.id + '/';
                    //$window.location.href = target;
                    //<a href="{% url 'imagestore:upload'  %}{[{ event.ctype_id }]}/{[{ event.id }]}/">Add Images</a>
                }


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
            }, function () {});
        };
    }]);

