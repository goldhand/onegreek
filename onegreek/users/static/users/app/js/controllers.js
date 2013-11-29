'use strict';

/* Controllers */

var userControllers = angular.module('userControllers', []);

userControllers.controller('UserGlobalCtrl', [
    '$scope', '$rootScope', '$location', '$timeout', 'GlobalService',
    function ($scope, $rootScope, $location, $timeout, GlobalService) {

        $scope.globals = GlobalService;
        $scope.globals.users = undefined;
        var failureCb = function (status) {
            console.log(status);
        };
        $scope.initialize = function (is_authenticated, user_id, chapter_id, host) {
            $scope.globals.is_authenticated = is_authenticated;
            $scope.globals.user_id = user_id;
            $scope.globals.chapter_id = chapter_id;
            $scope.globals.host = host;
            console.log(host);
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

        angular.forEach($scope.groups, function(group) {
            group.tab = {
                active: false,
                disabled: false
            };
        });
        $scope.groups[0].tab.active = true;

        if($scope.globals.users == undefined) {
            $scope.globals.users = users;
        }
        if($scope.globals.groups == undefined) {
            $scope.globals.groups = groups;
        }
        if($scope.globals.user == undefined) {
            $scope.globals.user = filterFilter($scope.globals.users, {id: $scope.globals.user_id})[0];
        }

        $scope.Search = undefined;

        //$scope.filterForGroup = function(group) {
        //    return filterFilter($scope.globals.users, {groups: group.url});
            //$scope.users = filterFilter($scope.globals.users, {groups: group.url});
            //UserService.filter('group', group.id).then(function(data) {
            //    $scope.users = data;
            //});
        //};
        //angular.forEach($scope.groups, function(group) {
        //    group.user_set = $scope.filterForGroup(group);
        //});

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
    '$modal',
    'GroupService',
    'GlobalService',
    function (
        $scope,
        $http,
        $modal,
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
            // convert user objects into urls for server
            angular.forEach(group.user_set, function(user) {
                if(user.status)
                if(user.url){
                    this.push(user.url.toString());
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
        $scope.openCarouselModal = function (users) {
            var modalInstance = $modal.open({
                templateUrl: 'carousel-modal.html',
                controller: 'CarouselModalInstanceCtrl',
                windowClass: 'full-screen-modal',
                resolve: {
                    users: function () {
                        return users;
                    }
                }
            });

            modalInstance.result.then(function () {

            }, function () {});
        };



    }]);

userControllers.controller('MyFormCtrl', [
    '$scope',
    '$http',
    '$modal',
    'GlobalService',
    'GroupService',
    function (
        $scope,
        $http,
        $modal,
        GlobalService,
        GroupService
        ) {
        $scope.group = {};
        $scope.globals = GlobalService;
        $scope.submit = function() {
            GroupService.save($scope.group).then(function(data) {
                $scope.group.tab = { active: true, disabled: false};
                $scope.globals.groups.push(data);

            }, function(status) {
                console.log(status);
            });
        };
        $scope.submitGroup = function(group) {
            GroupService.update(group).then(function(data) {
                $scope.group = data;
                $scope.group.tab = { active: true, disabled: false};
                $scope.globals.groups.push(data);
                $scope.group = {}
            }, function(status) {
                console.log(status);
            });
        };

        $scope.openModal = function () {
            var modalInstance = $modal.open({
                templateUrl: 'newGroupModal.html',
                controller: 'ModalInstanceCtrl',
                resolve: {
                    group: function () {
                        $scope.group = {};
                        console.log('myformctrl.openModal');
                        return $scope.group;
                    }
                }
            });

            modalInstance.result.then(function (newGroup) {
                $scope.group = newGroup;
                console.log('myformctrl.openModal.result');
                console.log($scope.group);
                $scope.group.name = 'chapter_' + $scope.globals.chapter_id + ' ' + newGroup.name;
                $scope.submit();
            }, function () {});
        };
    }]);



userControllers.controller('ModalInstanceCtrl', [
    '$scope',
    '$timeout',
    '$modalInstance',
    'group',
    function (
        $scope,
        $timeout,
        $modalInstance,
        group
        ) {

        $scope.group = group;

        $scope.ok = function () {
            console.log('myModalInstance.ok');
            console.log($scope.group);
            $modalInstance.close($scope.group);
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    }]);


userControllers.controller('CarouselModalInstanceCtrl', [
    '$scope',
    '$timeout',
    '$modalInstance',
    'users',
    function (
        $scope,
        $timeout,
        $modalInstance,
        users
        ) {

        $scope.users = users;

        $scope.ok = function () {
            console.log('RushCarouselInstance.ok');
            $modalInstance.close();
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    }]);



