'use strict';

/* Controllers */
usersApp.controller('UserListCtrl', ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
    $scope.user = {};
    $http.get('/api/users/').success(function(data) {
        $scope.users = data;
    });
    $scope.submit = function() {
        $http.post('/api/users/', $scope.user).success(function(user_data) {
            $scope.users.push(user_data);
        });
    };
    $scope.openStart = function() {
        $timeout(function() {
            $scope.openedStart = true;
        });
    };
    $scope.openEnd = function() {
        $timeout(function() {
            $scope.openedEnd = true;
        });
    };
    $scope.dateOptions = {
        'year-format': "'yyyy'",
        'month-format': "'mm'",
        'starting-day': 1
    };
    $scope.hstep = 1;
    $scope.mstep = 15;
    $scope.ismeridian = true;

    $scope.Search = undefined;

}]);

usersApp.controller('UserDetailCtrl', ['$scope', '$http', '$routeParams', function ($scope, $http, $routeParams) {
    $http.get('/api/users/' + $routeParams.userId + '/').success(function(data) {
        $scope.user = data;
    });
    $scope.submit = function() {
        $http.post('/api/users/' + $routeParams.userId + '/', $scope.user).success(function(user_data) {
            $scope.users.push(user_data);
        });
    };
}]);


usersApp.controller('MyFormCtrl', ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
    $scope.user = {};
    $scope.submit = function() {
        $http.post('/api/users/', $scope.user).success(function(user_data) {
            $scope.users.push(user_data);
        });
    };

    $scope.openStart = function() {
        $timeout(function() {
            $scope.openedStart = true;
        });
    };
    $scope.openEnd = function() {
        $timeout(function() {
            $scope.openedEnd = true;
        });
    };
    $scope.dateOptions = {
        'year-format': "'yyyy'",
        'month-format': "'mm'",
        'starting-day': 1
    };
    $scope.hstep = 1;
    $scope.mstep = 15;
    $scope.ismeridian = true;
}]);

