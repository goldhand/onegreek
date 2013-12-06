'use strict';

/* Controllers */

var userControllers = angular.module('userControllers', []);

userControllers.controller('UserGlobalCtrl', [
    '$scope', '$rootScope', '$location', '$http', '$timeout', 'GlobalService',
    function ($scope, $rootScope, $location, $http, $timeout, GlobalService) {

        $scope.globals = GlobalService;
        $scope.globals.users = undefined;
        var failureCb = function (status) {
            console.log(status);
        };
        $scope.initialize = function (is_authenticated, user_id, chapter_id, host) {
            $scope.globals.is_authenticated = is_authenticated;
            $scope.globals.user_id = user_id;
            if(is_authenticated) {
                var api_url = "/api/users/";
                var url = api_url + user_id + "/";
                $http.get('/api/users/' + user_id + '/').success(function(user_data) {
                    $scope.globals.user = user_data;
                    console.log(user_data);
                    console.log($scope.globals.user.status);
                });
            }
            $scope.globals.chapter_id = chapter_id;
            $scope.globals.host = host;
            console.log(host);
        };

}]);


userControllers.controller('UserListCtrl', [
    '$scope',
    '$http',
    '$modal',
    'filterFilter',
    'UserService',
    //'GroupService',
    'GlobalService',
    'users',
    'groups',
    function (
        $scope,
        $http,
        $modal,
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


        $scope.filterForUserStatus = function(status) {
            $scope.users = filterFilter($scope.globals.users, {status: status});
        };
        $scope.pendingActivesFirst = function(user) {
            return (user.status == 'active_pending');
        };

        $scope.modUser = function(user, action, status, new_status) {
            $http.post('/users/mod/', {
                user_id: user.id,
                chapter_id: $scope.globals.chapter_id,
                action: action,
                status: status,
                new_status: new_status
            }).success(function(data) {
                    console.log(data);
                    if(data.success) {
                        if(data.status == 'admin') {
                            if(data.action == 'add') {
                                user.is_chapter_admin = true;
                            } else {
                                user.is_chapter_admin = false;

                            }

                        } else {
                            if(data.action == 'add') {
                                user.status = data.status;
                            } else {
                                if(data.status == 'active_pending') {
                                    var index = $scope.users.indexOf(user);
                                    $scope.users.splice(index, 1);

                                }
                                user.status = data.new_status;
                            }
                        }
                    }
            });
        };


        $scope.filterForGroupName = function(group_name) {
            return filterFilter($scope.groups, {name: group_name})[0];
        };

        $scope.updateGroups = function(active_group_name) {
            angular.forEach($scope.groups, function(group) {
                group.tab = {
                    active: false,
                    disabled: false,
                    display: false,
                    rush: false,
                    pending: false
                };
                var re = /^\w+?\d+?\s/;
                group.tab.display = group.name.split(re)[1];
                if(group.tab.display == "Rush") {
                    group.tab.rush = true;
                    $scope.globals.rushGroup = group;
                }
                if(group.tab.display == "Pending") {
                    group.tab.pending = true;
                    $scope.globals.pendingGroup = group;
                }
                if(group.tab.display == active_group_name) {
                    group.tab.active = true;
                    $scope.globals.activeGroup = group;
                }
            });
            if(active_group_name == '') {
                $scope.groups[0].tab.active = true;
            }
        };
        $scope.updateGroups('');

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

        $scope.submitPending = function(group) {
            var drop_user_set = [];
            var unchanged_user_set = [];

            var group_name_prefix = 'chapter_' + $scope.globals.chapter_id;
            var active_group_name = group_name_prefix + ' Active';
            var active_group = $scope.filterForGroupName(active_group_name);

            // convert user objects into urls for server
            angular.forEach(group.user_set, function(user) {
                if(user.pending == "active") {
                    this.push(user);
                }
                else {
                    if(user.pending == "drop") {
                        drop_user_set.push(user.id);
                    }
                    else {
                        unchanged_user_set.push(user.url.toString())
                    }
                }
            }, active_group.user_set);
            $http.put(group.url,
                {
                    'id': group.id,
                    'name': group.name,
                    'url': group.url,
                    'user_set':unchanged_user_set
                }
            ).success(function(group_data) {

                    $http.post('/users/group/mod/',
                        {
                            'action': 'drop',
                            'group_id': group.id,
                            'chapter_id': $scope.globals.chapter_id,
                            'user_set': drop_user_set
                        }
                        ).success(function(data){
                        $scope.submitGroup(active_group);
                    });
                });
        };

        $scope.submitGroup = function(group) {
            var user_set = [];
            // convert user objects into urls for server
            angular.forEach(group.user_set, function(user) {
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
            ).success(function(group_data) {
                    $http.get('/api/groups/').success(function(data) {
                        $scope.groups = data;
                        $scope.updateGroups(group.tab.display);
                        $scope.globals.groups = $scope.groups;
                    });
                    UserService.list().then(function(data) {
                        $scope.globals.users = data;
                    });
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
        $scope.callList = function(user, action) {
            var group_name_prefix = 'chapter_' + $scope.globals.chapter_id;
            var call_group = $scope.filterForGroupName(group_name_prefix + ' Call List');

            $http.post('/users/group/call/', {
                    'user_id': user.id,
                    'group_id': call_group.id,
                    'action': action
            }
            ).success(function(data) {
                    if(action == 'add') {
                        user.call = true;
                    }
                    if(action == 'remove') {
                        user.call = false;
                    }
                console.log(data);
            });
        };

        $scope.openCarouselModal = function (users) {
            var group_name_prefix = 'chapter_' + $scope.globals.chapter_id;
            var call_group = $scope.filterForGroupName(group_name_prefix + ' Call List');
            var modalInstance = $modal.open({
                templateUrl: 'carousel-modal.html',
                controller: 'CarouselModalInstanceCtrl',
                windowClass: 'full-screen-modal',
                resolve: {
                    users: function () {
                        return users;
                    },
                    call_list: function () {
                        return call_group;
                    }
                }
            });

            modalInstance.result.then(function (call_list) {
                console.log(call_list);
                angular.forEach(call_list.add, function(user) {
                    call_group.user_set.push(user);
                });
                $scope.submitGroup(call_group);
            }, function () {});
        };
    }]);

userControllers.controller('UserDetailCtrl', ['$scope', '$http', '$routeParams', 'user', function ($scope, $http, $routeParams, user) {
    $scope.user = user;
    $scope.submit = function() {
        $http.post('/api/users/' + $routeParams.userId + '/', $scope.user).success(function(user_data) {
            $scope.users.push(user_data);
        });
    };
    $scope.callList = function(user, action, group_id) {

        $http.post('/users/group/call/', {
                'user_id': user.id,
                'group_id': group_id,
                'action': action
            }
        ).success(function(data) {
                console.log(data);
            });
    };
}]);


userControllers.controller('GroupListCtrl', [
    '$scope',
    '$http',
    '$modal',
    'filterFilter',
    'GroupService',
    'GlobalService',
    function (
        $scope,
        $http,
        $modal,
        filterFilter,
        GlobalService,
        GroupService
        ) {



        $scope.submitGroup2 = function(group) {
            var user_set = [];
            // convert user objects into urls for server
            angular.forEach(group.user_set, function(user) {
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
            ).success(function(group_data) {
                    console.log(group_data);
                    $http.get('/api/groups/').success(function(data) {
                        $scope.globals.groups = data;
                        angular.forEach($scope.globals.groups, function(group) {
                            group.tab = {
                                active: false,
                                disabled: false
                            };
                            if (group.name == group_data.name) {
                                group.tab.active = true;

                            };
                        });
                    });
                });
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
    'call_list',
    function (
        $scope,
        $timeout,
        $modalInstance,
        users,
        call_list
        ) {

        $scope.users = users;
        $scope.call_list = call_list;


        $scope.callList = function(user, action) {
            if(action == 'add') {
                $scope.call_list.user_set.push(user);
                user.call = true;
            }
            if(action == 'remove') {
                var add_index = $scope.call_list.user_set.indexOf(user);
                $scope.call_list.user_set.splice(add_index, 1);
                user.call = false;
            }

        };
        $scope.ok = function () {
            console.log('RushCarouselInstance.ok');
            $modalInstance.close($scope.call_list);
        };

        $scope.cancel = function () {
            $modalInstance.close($scope.call_list);
        };
    }]);



userControllers.controller('UserFormCtrl', [
    '$scope',
    '$http',
    'filterFilter',
    'GlobalService',
    function (
        $scope,
        $http,
        filterFilter,
        GlobalService
        //GroupService,
        ) {

        $scope.globals = GlobalService;
        $scope.userForm = {
            part2: false,
            next: '?next=/avatar/change/'
            };
        $scope.userForm.reveal = function(status) {
            console.log('userform');
            $scope.userForm.part2 = true;
            if(status == 'active') {
                $scope.userForm.next = '';
            } else {
                $scope.userForm.next = '?next=/avatar/change/';
            }
        };

    }]);
