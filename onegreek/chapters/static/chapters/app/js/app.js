'use strict';


// Declare app level module which depends on filters, and services
var chapterApp = angular.module('chapterApp', [
    'ui.bootstrap',
    'ngCookies',
    'ngRoute',
    //'ngDragDrop',
    'chapterControllers',
    'chapterServices',
    'userServices',
    'chapterDirectives'
    //'groupControllers',
    //'groupServices'
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

chapterApp.config(['$routeProvider', '$httpProvider', function($routeProvider, $httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $routeProvider.when('/chapters', {
        templateUrl: '/static/chapters/app/partials/list.html',
        controller: 'ChapterListCtrl',
        resolve: {
            chapters: function(ChapterService) {
                return ChapterService.list();
            }
        }
    });
    $routeProvider.when('/chapters/filter/:query/:queryId', {
        templateUrl: 'list.html',
        controller: 'ChapterListCtrl',
        resolve: {
            chapters: function($route, ChapterService) {
                var q = $route.current.params.query;
                var qId = $route.current.params.queryId;
                return ChapterService.filter(q, qId);
            }
        }
    });
    $routeProvider.when('/chapters/:chapterId', {
        templateUrl: '/static/chapters/app/partials/detail.html',
        controller: 'ChapterDetailCtrl',
        resolve: {
            chapter: function($route, ChapterService) {
                var chapterId = $route.current.params.chapterId;
                return ChapterService.get(chapterId);
            },
            users: function($route, UserService) {
                var q = 'chapter';
                var qId = $route.current.params.chapterId;
                return UserService.filter(q, qId);
            }
        }

    });
    $routeProvider.otherwise({redirectTo: '/chapters'});
}]);
