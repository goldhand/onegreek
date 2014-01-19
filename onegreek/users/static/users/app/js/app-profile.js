'use strict';


// Declare app level module which depends on filters, and services
var userApp = angular.module('userApp', [
    'ui.bootstrap',
    'ngCookies',
    'ngRoute',
    'userControllers',
    'leftContentControllers',
    'userServices'
    //'userDirectives'
    //'groupControllers',
],
    function($interpolateProvider) {
        $interpolateProvider.startSymbol("{[{");
        $interpolateProvider.endSymbol("}]}");
    }
);

userApp.config(['$routeProvider', '$httpProvider', function($routeProvider, $httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $routeProvider.when('/', {});
    $routeProvider.when('/events/calendar/', {
            templateUrl: 'list.html',
            controller: 'EventListCtrl'
    });
    $routeProvider.when('/img/', {
        controller: 'ProfileImgCtrl'
    });
    $routeProvider.otherwise({redirectTo: '/'});
}]);


userApp.controller('ProfileImgCtrl', [
    '$scope',
    '$http',
    '$route',
    '$window',
    'GlobalService',
    function(
        $scope,
        $http,
        $route,
        $window,
        GlobalService
        ) {
        $scope.globals = GlobalService;
        $scope.showProfileImgPreview = false;

        $scope.getUser = function(user_id) {
            $http.get('/api/users/' + user_id + '/').success(function(data) {
                $scope.user = data;
                $scope.user.photos = [];
                console.log($scope.user);
                $scope.setUserImg = function(select) {
                    console.log(select);
                    $scope.user.profile_img_select = select;
                };
            });
        };


        $scope.submit = function() {
            $http.put('/api/users/' + $scope.user.id + '/', $scope.user).success(function(user_data) {
                console.log(user_data);
                $scope.globals.addAlert("success", "Profile image updated. Refresh to see changes.");
            });
        };

        $scope.submitRedirect = function(target) {
            $http.put('/api/users/' + $scope.user.id + '/', $scope.user).success(function(user_data) {
                console.log(user_data);
                $scope.user = user_data;
                $scope.user.albums = [];
                $window.location.href = target;
            });
        };

        $scope.getFbAlbums = function() {
            $http.get($scope.user.fb_photos + '&access_token=' + $scope.user.fb_access_token).success(function(data) {
                $scope.user.albums = data.albums.data;
                angular.forEach($scope.user.albums, function(album) {
                    album.photos = [];
                    album.collapse = true;
                });
                console.log($scope.user);
            }).error(function(data) {
                $scope.globals.addAlert("error", "Please login again to use facebook photo albums");
               
            });
        };
        $scope.expandFbAlbum = function(user, album) {
            if(!(album.photos.length)) {

                $http.get('https://graph.facebook.com/' + album.id + '/photos?fields=id,picture,source&access_token=' + $scope.user.fb_access_token).success(function(data) {
                    console.log(data);
                    album.photos = data.data;
                    console.log($scope.user);
                });
            }
            album.collapse = !album.collapse;
        };

        $scope.saveProfileImg = function(user, img) {
            $http.get('https://graph.facebook.com/' + img.id + '?fields=picture,source,id&access_token=' + $scope.user.fb_access_token).success(function(data) {
                $scope.user.profile_img_id = data.id;
                $scope.user.profile_img_src = data.source;
                $scope.user.profile_img_pic = data.picture;
                $scope.showProfileImgPreview = true;
                console.log($scope.user);
            });
        };



    }]);

userApp.controller('AlertCtrl', [
    '$scope',
    'GlobalService',
    function(
        $scope,
        GlobalService
        ) {
        $scope.globals = GlobalService;
        $scope.globals.alerts = [];

        $scope.globals.closeAlert = function(index) {
            $scope.globals.alerts.splice(index, 1);

        };

        $scope.globals.addAlert = function(type, msg) {
            $scope.globals.alerts.push({type: type, msg: msg});
            if ($scope.globals.alerts.length >= 6) {
                $scope.globals.closeAlert(0);
            }
        };
    }]);

userApp.controller('ProfileCalendarCtrl', [
    '$scope',
    '$http',
    '$modal',
    '$sce',
    '$route',
    'filterFilter',
    'GlobalService',
    function (
        $scope,
        $http,
        $modal,
        $sce,
        $route,
        filterFilter,
        GlobalService
        ) {

        $scope.globals = GlobalService;
        //$scope.year = $route.current.params.year;
        //$scope.month = $route.current.params.month;
        //$scope.day = $route.current.params.day;
        //$scope.calendar.day = 10;

        $scope.getCal = function(year, month) {
            var cal_url = '/events/calendar/' + year + '/' + month + '/';   // + $scope.day + '/';
            $http.get(cal_url).success(function(data) {
                console.log(data);
                $scope.calendar = {
                    cal: data,
                    html: $sce.trustAsHtml(data.calendar),
                    year: year,
                    month: month
                };
                console.log($scope.calendar);
            });
        };

        $scope.cal = {
            year: 2013,
            month: 12
        };
        $scope.calMonthUp = function() {
            if($scope.cal.month < 12) {
                $scope.cal.month += 1;
            } else {
                $scope.cal.month = 1;
                $scope.cal.year += 1;
            }
            $scope.getCal($scope.cal.year, $scope.cal.month);
        };
        $scope.calMonthDown = function() {
            if($scope.cal.month > 2) {
                $scope.cal.month -= 1;
            } else {
                $scope.cal.month = 12;
                $scope.cal.year -= 1;
            }
            $scope.getCal($scope.cal.year, $scope.cal.month);
        };

        $scope.getCal($scope.cal.year, $scope.cal.month);

        console.log($scope.calendar);


    }]);


userApp.controller('EventListCtrl', [
    '$scope',
    '$http',
    '$modal',
    '$window',
    'filterFilter',
    'GlobalService',
    function (
        $scope,
        $http,
        $modal,
        $window,
        filterFilter,
        GlobalService
        ) {
        $scope.event = {};
        $scope.globals = GlobalService;
        $scope.getEvents = function() {
            $http.get('/api/events/').success(function(data) {
                $scope.formatCalendarEvents(data);
                $scope.events = data;
                $scope.globals.events = data;
            });
        };

        $scope.formatCalendarEvents = function(events) {
            angular.forEach(events, function(event) {
                event.start = new Date(event.start);
                event.end = new Date(event.end);
                event.url = '#events/' + event.id;
            });
        };


        $scope.Search = undefined;

        $http.get('/api/events/').success(function(data) {
            $scope.formatCalendarEvents(data);
            $scope.events = data;
            $scope.globals.events = data;
        });



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

        /* event sources array*/
        $scope.eventSources = [$scope.events, $scope.eventsF];


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
                eventResize: $scope.alertOnResize
            }
        };


    }]);





