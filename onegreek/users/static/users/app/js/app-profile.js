'use strict';


// Declare app level module which depends on filters, and services
var userApp = angular.module('userApp', [
    'ui.bootstrap',
    'ngCookies',
    'ngRoute',
    'ngDragDrop',
    'userControllers',
    'userServices',
    'userDirectives'
    //'groupControllers',
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

userApp.config(['$routeProvider', '$httpProvider', function($routeProvider, $httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $routeProvider.when('/events/calendar/:year/:month/:day', {
            templateUrl: 'profile-calendar.html',
            controller: 'ProfileCalendarCtrl'
    });
    $routeProvider.when('/events/calendar/', {
        templateUrl: 'profile-calendar.html',
        controller: 'ProfileCalendarCtrl'
    });
    $routeProvider.when('/events/calendar/rsvp', {
        templateUrl: 'http://localhost:8000/events/calendar/2013/11/?rsvp=true&profile=true'
    });
    $routeProvider.when('/', {
        controller: 'ProfileImgCtrl'
    });
    $routeProvider.otherwise({redirectTo: '/'});
}]);


userApp.controller('ProfileImgCtrl', [
    '$scope',
    '$http',
    '$route',
    '$window',
    function(
        $scope,
        $http,
        $route,
        $window
        ) {
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
                $scope.user = user_data;
                $scope.user.albums = [];
                $window.location.href = '/chapters/';
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




