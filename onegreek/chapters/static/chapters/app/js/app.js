'use strict';


// Declare app level module which depends on filters, and services
var chapterApp = angular.module('chapterApp', [
    'ui.bootstrap',
    'ngCookies',
    'ngRoute',
    'ngAnimate',
    'chapterControllers',
    'leftContentControllers',
    'chapterServices',
    //'chapterDirectives'
],
    function($interpolateProvider) {
        $interpolateProvider.startSymbol("{[{");
        $interpolateProvider.endSymbol("}]}");
    }
);

chapterApp.config(['$routeProvider', '$httpProvider', function($routeProvider, $httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $routeProvider.when('/', {
        templateUrl: 'detail.html',
        controller: 'ChapterDetailCtrl',
    });
    $routeProvider.otherwise({redirectTo: '/'});
}]);
