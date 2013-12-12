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
    $routeProvider.otherwise({redirectTo: '/events/calendar'});
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




