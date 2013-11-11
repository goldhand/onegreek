'use strict';

/* Controllers */

var groupControllers = angular.module('groupControllers', []);

groupControllers.controller('AppController', function ($scope, $rootScope, $location, GlobalService) {
    var failureCb = function (status) {
        console.log(status);
    };
    $scope.globals = GlobalService;

    $scope.initialize = function (is_authenticated) {
        $scope.globals.is_authenticated = is_authenticated;
    };
});


groupControllers.controller('GroupListCtrl', [
    '$scope',
    '$http',
    'GroupService',
    'GlobalService',
    'groups',
    function (
        $scope,
        $http,
        GroupService,
        GlobalService,
        groups
        ) {
        $scope.group = {};
        $scope.groups = groups;
        $scope.globals = GlobalService;
        $scope.globals.groups = groups;

        $scope.submit = function() {
            GroupService.save($scope.group).then(function(data) {
                $scope.group = data;
                $scope.groups.push(data);
            }, function(status) {
                console.log(status);
            });
        };

        $scope.Search = undefined;

    }]);

groupControllers.controller('GroupDetailCtrl', ['$scope', '$http', '$routeParams', 'group', function ($scope, $http, $routeParams, group) {
    $scope.group = group;
    $scope.submit = function() {
        $http.post('/api/groups/' + $routeParams.groupId + '/', $scope.group).success(function(group_data) {
            $scope.groups.push(group_data);
        });
    };
}]);

