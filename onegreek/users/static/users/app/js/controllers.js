'use strict';

/* Controllers */

var userControllers = angular.module('userControllers', []);

userControllers.controller('UserGlobalCtrl', function ($scope, $rootScope, $location, GlobalService) {
    var failureCb = function (status) {
        console.log(status);
    };
    $scope.globals = GlobalService;
    $scope.globals.users = undefined;

    $scope.initialize = function (is_authenticated) {
        $scope.globals.is_authenticated = is_authenticated;
    };
});


userControllers.controller('UserListCtrl', [
    '$scope',
    '$http',
    'UserService',
    //'GroupService',
    'GlobalService',
    'users',
    'groups',
    function (
        $scope,
        $http,
        UserService,
        GlobalService,
        //GroupService,
        users,
        groups
        ) {
        $scope.user = {};
        $scope.users = users;
        $scope.groups = groups;

        $scope.globals = GlobalService;
        if($scope.globals.users == undefined) {
            $scope.globals.users = users;
        }

        $scope.submit = function() {
            UserService.save($scope.user).then(function(data) {
                $scope.user = data;
                $scope.users.push(data);
            }, function(status) {
                console.log(status);
            });
        };

        $scope.Search = undefined;

    }]);

userControllers.controller('UserDetailCtrl', ['$scope', '$http', '$routeParams', 'user', function ($scope, $http, $routeParams, user) {
    $scope.user = user;
    $scope.submit = function() {
        $http.post('/api/users/' + $routeParams.userId + '/', $scope.user).success(function(user_data) {
            $scope.users.push(user_data);
        });
    };
}]);

