'use strict';


// Declare app level module which depends on filters, and services
var commentApp = angular.module('commentApp', [
    'ui.bootstrap',
    'ngCookies',
    'ngRoute',
    'ngDragDrop',
    'commentControllers',
    'commentServices',
    'commentDirectives',
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

commentApp.config(['$routeProvider', '$httpProvider', function($routeProvider, $httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $routeProvider.when('/comments', {
        templateUrl: 'list.html',
        controller: 'UserListCtrl',
        resolve: {
            comments: function(UserService) {
                return UserService.list();
            },
            groups: function(GroupService) {
                return GroupService.list();
            }
        }
    });
    $routeProvider.when('/comments/filter/:query/:queryId', {
        templateUrl: 'list.html',
        controller: 'UserListCtrl',
        resolve: {
            comments: function($route, UserService) {
                var q = $route.current.params.query;
                var qId = $route.current.params.queryId;
                return UserService.filter(q, qId);
            }
        }
    });
    $routeProvider.when('/comments/:commentId', {
        templateUrl: 'detail.html',
        controller: 'UserDetailCtrl',
        resolve: {
            comment: function($route, UserService) {
                var commentId = $route.current.params.commentId;
                return UserService.get(commentId);
            }
        }

    });
    $routeProvider.otherwise({redirectTo: '/comments'});
}]);
