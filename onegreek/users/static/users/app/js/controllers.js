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

        $scope.filterForGroup = function(group) {
            //return filterFilter($scope.globals.users, {groups: group.url});
            //$scope.users = filterFilter($scope.globals.users, {groups: group.url});
            UserService.filter('group', group.id).then(function(data) {
                $scope.users = data;
            });
        };

        $scope.startDragUser = function(user) {
            $scope.draggedUser = user;
            console.log(user);
        };

        $scope.acceptUserToGroup = function(event, ui, group) {
            if (filterFilter(group.user_set, {id: $scope.$eval(ui.draggable.ngattr('jqyoui-draggable')).index}) === 'undefined') {
                console.log(filterFilter(group.user_set, {id: $scope.$eval(ui.draggable.ngattr('jqyoui-draggable')).index}));
                return true;
            } else {
                console.log(filterFilter(group.user_set, {id: $scope.$eval(ui.draggable.ngattr('jqyoui-draggable')).index}));
                return false;
            }
        };

        $scope.addUsersToGroup = function(event, ui, group) {
            console.log(group.user_set);
            console.log(filterFilter(group.user_set, {id: $scope.$eval(ui.draggable.ngattr('jqyoui-draggable')).index}));
            console.log(ui.draggable.ngattr('ng-model'));
            console.log($scope.$eval(ui.draggable.ngattr('jqyoui-draggable')).index);
        };
        $scope.removeUserFromGroup = function(event, ui, group) {
            console.log('out');
            console.log(group);
            group.user_set.pop($scope.draggedUser);
        };

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
                if(user.url){
                    this.push(user.url.toString());
                } else {
                    this.push(user);
                }
            }, user_set);
            $http.put(group.url,
                {
                    'id': group.id,
                    'name': group.name,
                    'url': group.url,
                    'user_set':user_set
                }
            ).success(function(data) {
                console.log(data);
            });
        };



    }]);


