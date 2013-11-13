'use strict';

/* Controllers */

var userControllers = angular.module('userControllers', []);

userControllers.controller('UserGlobalCtrl', [
    '$scope', '$rootScope', '$location', '$timeout', 'GlobalService',
    function ($scope, $rootScope, $location, $timeout, GlobalService) {
    var failureCb = function (status) {
        console.log(status);
    };
    $scope.globals = GlobalService;
    $scope.globals.users = undefined;

    $scope.initialize = function (is_authenticated) {
        $scope.globals.is_authenticated = is_authenticated;
    };

}]);


userControllers.controller('UserListCtrl', [
    '$scope',
    '$http',
    'filterFilter',
    'UserService',
    //'GroupService',
    'GlobalService',
    'users',
    'groups',
    function (
        $scope,
        $http,
        filterFilter,
        UserService,
        GlobalService,
        //GroupService,
        users,
        groups
        ) {

        $scope.user = {};
        $scope.users = users;
        $scope.globals = GlobalService;
        $scope.groups = groups;

        if($scope.globals.users == undefined) {
            $scope.globals.users = users;
        }

        $scope.Search = undefined;

        //$scope.filterForGroup = function(group) {
        //    return filterFilter($scope.globals.users, {groups: group.url});
            //$scope.users = filterFilter($scope.globals.users, {groups: group.url});
            //UserService.filter('group', group.id).then(function(data) {
            //    $scope.users = data;
            //});
        //};
        //angular.forEach($scope.groups, function(group){
        //    var user_set = $scope.filterForGroup(group);
        //    group.user_set = user_set;
        //});

        $scope.submitUser = function() {
            UserService.save($scope.user).then(function(data) {
                $scope.user = data;
                $scope.users.push(data);
            }, function(status) {
                console.log(status);
            });
        };



    }]);

userControllers.controller('UserDetailCtrl', ['$scope', '$http', '$routeParams', 'user', function ($scope, $http, $routeParams, user) {
    $scope.user = user;
    $scope.submit = function() {
        $http.post('/api/users/' + $routeParams.userId + '/', $scope.user).success(function(user_data) {
            $scope.users.push(user_data);
        });
    };
}]);


userControllers.controller('GroupListCtrl', [
    '$scope',
    '$http',
    'GroupService',
    'GlobalService',
    function (
        $scope,
        $http,
        GlobalService,
        GroupService
        ) {

        $scope.submitGroup = function(group) {
            GroupService.update(group).then(function(data) {
                console.log(data);
            }, function(status) {
                console.log(status);
            });
        };
        $scope.submitGroup2 = function(group) {
            var user_set = [];
            angular.forEach(group.user_set, function(user) {
                this.push(user.url.toString());
            }, user_set);
            group.user_set = user_set;
            console.log(group);
            $http.put(group.url, group).success(function(data) {
                console.log(data);
            });
        };



    }]);


