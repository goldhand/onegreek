'use strict';


// Declare app level module which depends on filters, and services
var groupApp = angular.module('groupApp', [
    'ui.bootstrap',
    'ngCookies',
    'ngRoute',
    'groupControllers',
    'groupervices'
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

groupsApp.config(['$routeProvider', '$httpProvider', function($routeProvider, $httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $routeProvider.when('/groups', {
        templateUrl: 'list.html',
        controller: 'GroupListCtrl',
        resolve: {
            groups: function(GroupService) {
                return GroupService.list();
            }
        }
    });
    $routeProvider.when('/groups/filter/:query/:queryId', {
        templateUrl: 'list.html',
        controller: 'GroupListCtrl',
        resolve: {
            groups: function($route, GroupService) {
                var q = $route.current.params.query;
                var qId = $route.current.params.queryId;
                return GroupService.filter(q, qId);
            }
        }
    });
    $routeProvider.when('/groups/:groupId', {
        templateUrl: 'detail.html',
        controller: 'GroupDetailCtrl',
        resolve: {
            group: function($route, GroupService) {
                var groupId = $route.current.params.groupId;
                return GroupService.get(groupId);
            }
        }

    });
    $routeProvider.otherwise({redirectTo: '/groups'});
}]);
