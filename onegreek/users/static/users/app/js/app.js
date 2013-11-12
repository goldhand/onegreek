'use strict';


// Declare app level module which depends on filters, and services
var userApp = angular.module('userApp', [
    'ui.bootstrap',
    'ngCookies',
    'ngRoute',
    'userControllers',
    'userServices',
    //'groupControllers',
    'groupServices'
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
    $routeProvider.when('/users', {
        templateUrl: 'list.html',
        controller: 'UserListCtrl',
        resolve: {
            users: function(UserService) {
                return UserService.list();
            },
            groups: function(GroupService) {
                return GroupService.list();
            }
        }
    });
    $routeProvider.when('/users/filter/:query/:queryId', {
        templateUrl: 'list.html',
        controller: 'UserListCtrl',
        resolve: {
            users: function($route, UserService) {
                var q = $route.current.params.query;
                var qId = $route.current.params.queryId;
                return UserService.filter(q, qId);
            }
        }
    });
    $routeProvider.when('/users/:userId', {
        templateUrl: 'detail.html',
        controller: 'UserDetailCtrl',
        resolve: {
            user: function($route, UserService) {
                var userId = $route.current.params.userId;
                return UserService.get(userId);
            }
        }

    });
    $routeProvider.otherwise({redirectTo: '/users'});
}]);
