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
        $scope.globals.go = function ( path ) {
          $location.path( path );
        };

        $scope.globals.tabs = [
            {
                active: true,
                heading: 'All',
                status: '!rush',
                order : 0
            },
            {
                active: false,
                heading: 'Actives',
                status: 'active',
                order: 1
            },
            {
                active: false,
                heading: 'Pledge',
                status: 'pledge',
                order: 2
            },
            {
                active: false,
                heading: 'Rush',
                status: 'rush',
                order: 3
            }
        ];

        $scope.initialize = function (is_authenticated, user_id, chapter_id, rush_form_id, host) {
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
            $scope.globals.rush_form_id = rush_form_id;
            $scope.globals.host = host;
            console.log(host);
        };

}]);


userControllers.controller('UserListCtrl', [
    '$scope',
    '$http',
    '$modal',
    '$location',
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
        $location,
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
        $scope.globals.filterForUserStatus = function(status) {
            $scope.users = filterFilter($scope.globals.users, {status: status});
        };

        $scope.userStatusOrder = function(user) {
            var userStatusOrderKey = {
                active_pending: 1,
                admin: 2,
                active: 3,
                pledge: 4,
                rush: 5
            };
            if(user.is_chapter_admin) {
                return userStatusOrderKey['admin'];
            } else {
                return userStatusOrderKey[user.status];
            }
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
                            user.is_chapter_admin = data.action == 'add';
                        } else {

                            if(data.new_status == 'call') {
                                // Call list is special like admin
                                user.is_call = data.action == 'add';

                            } else {
                                if(data.action == 'add') {
                                    user.status = data.status;
                                } else {
                                    if(data.status == 'active_pending') {
                                        if(data.new_status == 'rush') {
                                            var index = $scope.users.indexOf(user);
                                            $scope.users.splice(index, 1);
                                        }
                                    }
                                    user.status = data.new_status;
                                }
                            }
                        }
                    }
            });
        };

        $scope.checkUserChapterGroup = function ( user, status ) {
            // Works better than goGroup for adding groups to tabs
            $http.get(
                    '/users/check/group/?check_user_id=' + user.id +
                        '&chapter_id=' + $scope.globals.chapter_id +
                        '&status=' + status
                ).success(function(data) {
                    console.log(data);
                    user.is_call = data.in_group;
                });
        };


        $scope.updateUsers = function(users) {
            angular.forEach(users, function(user) {
                user.status_order = $scope.userStatusOrder(user);
                if(user.status == 'rush') {
                    $scope.checkUserChapterGroup(user, 'call');
                }
            });
        };

        $scope.updateUsers($scope.users);
        console.log($scope.users);



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
                    call: false,
                    pending: false
                };
                var re = /^\w+?\d+?\s/;
                group.tab.display = group.name.split(re)[1];
                if(group.tab.display == "Rush") {
                    group.tab.rush = true;
                    $scope.globals.rushGroup = group;
                }
                if(group.tab.display == "Call List") {
                    group.tab.call = true;
                    $scope.globals.callGroup = group;
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

        $scope.goGroup = function ( path, query ) {
            var group = $scope.filterForGroupName(query);
            $location.path( path + group.id );
        };

        $scope.globals.goGroup = function ( path, query ) {
            var group = $scope.filterForGroupName(query);
            $location.path( path + group.id );
        };

        $scope.globals.getGroup = function ( path, query ) {
            // Works better than goGroup for adding groups to tabs
            var group = $scope.filterForGroupName(query);
            $http.get('/api/users/?group=' + group.id).success(function(data) {
                $scope.users = data;
            });
        };

        angular.forEach($scope.globals.tabs, function(tab) {
            tab.select = function() {
                $scope.filterForUserStatus(tab.status);
            };
            if (tab.active) {
                $scope.filterForUserStatus(tab.status);
            }
        });









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

        $scope.globals.openCarouselModal = function () {
            var group_name_prefix = 'chapter_' + $scope.globals.chapter_id;
            var call_group = $scope.filterForGroupName(group_name_prefix + ' Call List');
            var modalInstance = $modal.open({
                templateUrl: 'carousel-modal.html',
                controller: 'CarouselModalInstanceCtrl',
                windowClass: 'full-screen-modal rush-carousel',
                resolve: {
                    users: function () {
                        return $scope.users;
                    },
                    call_list: function () {
                        return call_group;
                    },
                    chapter_id: function () {
                        return $scope.globals.chapter_id
                    },
                    rush_form_id: function () {
                        return $scope.globals.rush_form_id
                    }
                }
            });

            modalInstance.result.then(function () {
                $scope.updateUsers($scope.users);
            }, function () {});
        };
    }]);

userControllers.controller('UserDetailCtrl', ['$scope', '$http', '$routeParams', 'GlobalService', 'user',
    function ($scope, $http, $routeParams, GlobalService, user) {
        $scope.user = user;
        $scope.globals = GlobalService;

    angular.forEach($scope.globals.tabs, function(tab) {
        tab.active = false;
        tab.select = function() {
            $scope.globals.go('#/users');
        }
    });

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

userControllers.controller('UserQueryCtrl', [
    '$scope',
    '$http',
    '$modal',
    '$location',
    'filterFilter',
    'UserService',
    'GlobalService',
    'users',
    function (
        $scope,
        $http,
        $modal,
        $location,
        filterFilter,
        UserService,
        GlobalService,
        users
        ) {

        $scope.users = users;
        $scope.globals = GlobalService;

        angular.forEach($scope.globals.tabs, function(tab) {
            tab.active = false;
            tab.select = function() {
                $scope.globals.go('#/users');
            }
        });


        $scope.globals.openCarouselModal = function () {
            var group_name_prefix = 'chapter_' + $scope.globals.chapter_id;
            var call_group = $scope.globals.callGroup;
            var modalInstance = $modal.open({
                templateUrl: 'carousel-modal.html',
                controller: 'CarouselModalInstanceCtrl',
                windowClass: 'full-screen-modal',
                resolve: {
                    users: function () {
                        return $scope.users;
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


userControllers.controller('CarouselModalInstanceCtrl', [
    '$scope',
    '$timeout',
    '$modalInstance',
    '$http',
    'filterFilter',
    'users',
    'call_list',
    'rush_form_id',
    'chapter_id',
    function (
        $scope,
        $timeout,
        $modalInstance,
        $http,
        filterFilter,
        users,
        call_list,
        rush_form_id,
        chapter_id
        ) {

        $scope.users = users;
        $scope.call_list = call_list;
        $scope.events = [];
        $scope.rush_form_id = rush_form_id;
        $scope.chapter_id = chapter_id;

        $scope.getRushEvents = function() {
            $http.get('/api/events/?rush_week=true&nest=true').success(function(data) {
                $scope.events = data;
            });
        };
        $scope.getRushEvents();

        $scope.getRushForm = function() {
            $http.get('/rush/forms/' + $scope.rush_form_id + '/').success(function(data) {
                console.log('\n\n\n++++++++++++++++++Rush Form ++++++++++++++++++++\n\n\n');
                console.log(data);
                angular.forEach(data.fields, function(field) {
                    field.value = '';
                });
                $scope.rushForm = data;
                console.log($scope.rushForm);
            });
        };
        $scope.getRushForm();


        $scope.getEventRsvpForUser = function(user, event) {
            var rsvp_query_set = filterFilter(event.get_rsvps, {id: user.id});
            var rsvp = false;
            if (rsvp_query_set.length > 0) {
                rsvp = true;
            }

            return rsvp
        };
        $scope.getEventAttendForUser = function(user, event) {
            var attendee_query_set = filterFilter(event.get_attendees, {id: user.id});
            var attendee = false;
            if (attendee_query_set.length > 0) {
                attendee = true;
            }
            return attendee
        };
        $scope.getEntryForUser = function(user) {
            var entry_url = '/rush/forms/' + $scope.rush_form_id + '/' + user.id + '/';

            $http.get(entry_url).success(function(data) {
                console.log('\n\n\n++++++++++++++++++Entry For User ' + user.get_full_name + ' ++++++++++++++++++++\n\n\n');
                console.log(data);
                console.log('\n\n\n++++++++++++++++++Users ++++++++++++++++++++\n\n\n');
                console.log($scope.users);
                user.fields = data.entry.fields;
                //return data;
            });
        };
        $scope.getEntriesForUsers = function() {
            angular.forEach($scope.users, function(user) {
                $scope.getEntryForUser(user);
                console.log(user);
            });
        };
        $scope.getEntriesForUsers();


        $scope.modUser = function(user, action, status, new_status) {
            $http.post('/users/mod/', {
                user_id: user.id,
                chapter_id: $scope.chapter_id,
                action: action,
                status: status,
                new_status: new_status
            }).success(function(data) {
                    console.log(data);
                    if(data.success) {
                        if(data.status == 'admin') {
                            user.is_chapter_admin = data.action == 'add';
                        } else {

                            if(data.new_status == 'call') {
                                // Call list is special like admin
                                user.is_call = data.action == 'add';

                            } else {
                                if(data.action == 'add') {
                                    user.status = data.status;
                                } else {
                                    if(data.status == 'active_pending') {
                                        if(data.new_status == 'rush') {
                                            var index = $scope.users.indexOf(user);
                                            $scope.users.splice(index, 1);
                                        }
                                    }
                                    user.status = data.new_status;
                                }
                            }
                        }
                    }
                });
        };

        $scope.checkUserChapterGroup = function ( user, status ) {
            // Works better than goGroup for adding groups to tabs
            $http.get(
                    '/users/check/group/?check_user_id=' + user.id +
                        '&chapter_id=' + $scope.chapter_id +
                        '&status=' + status
                ).success(function(data) {
                    console.log(data);
                    user.is_call = data.in_group;
                });
        };



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









//*******************************************



userControllers.controller('ModalInstanceCtrl', [
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
            console.log('myModalInstance.ok');
            console.log($scope.user);
            $modalInstance.close($scope.user);
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
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
