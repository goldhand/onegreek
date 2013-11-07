'use strict';


// Declare app level module which depends on filters, and services
var myApp = angular.module('myApp', [
    'ui.bootstrap',
    'ngCookies',
    'ngRoute'
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

//myApp.run([function ($rootScope, $log, $http, $cookies) {
//    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
//}]);

myApp.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/demo', {templateUrl: 'static/angularjs/app/partials/demo.html'});
    //$routeProvider.when('/view1', {templateUrl: 'partials/partial1.html', controller: 'MyCtrl1'});
    //$routeProvider.when('/view2', {templateUrl: 'partials/partial2.html', controller: 'MyCtrl2'});
    $routeProvider.otherwise({redirectTo: '/demo'});
}]);


