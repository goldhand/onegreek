'use strict';

/* Controllers */

var commentControllers = angular.module('commentControllers', []);

commentControllers.controller('UserGlobalCtrl', [
    '$scope', '$rootScope', '$location', '$timeout', 'GlobalService',
    function ($scope, $rootScope, $location, $timeout, GlobalService) {

        $scope.globals = GlobalService;
        $scope.globals.comments = undefined;
        var failureCb = function (status) {
            console.log(status);
        };
        $scope.initialize = function (is_authenticated, comment_id, chapter_id, host) {
            $scope.globals.is_authenticated = is_authenticated;
            $scope.globals.comment_id = comment_id;
            $scope.globals.chapter_id = chapter_id;
            $scope.globals.host = host;
            console.log(host);
        };

}]);


commentControllers.controller('UserListCtrl', [
    '$scope',
    '$http',
    'filterFilter',
    'UserService',
    //'GroupService',
    'GlobalService',
    'comments',
    'groups',
    function (
        $scope,
        $http,
        filterFilter,
        UserService,
        GlobalService,
        //GroupService,
        comments,
        groups
        ) {

        $scope.comment = {};
        $scope.comments = comments;
        $scope.globals = GlobalService;
        $scope.groups = groups;

        angular.forEach($scope.groups, function(group) {
            group.tab = {
                active: false,
                disabled: false
            };
        });
        $scope.groups[0].tab.active = true;

        if($scope.globals.comments == undefined) {
            $scope.globals.comments = comments;
        }
        if($scope.globals.groups == undefined) {
            $scope.globals.groups = groups;
        }
        if($scope.globals.comment == undefined) {
            $scope.globals.comment = filterFilter($scope.globals.comments, {id: $scope.globals.comment_id})[0];
        }

        $scope.Search = undefined;

        //$scope.filterForGroup = function(group) {
        //    return filterFilter($scope.globals.comments, {groups: group.url});
            //$scope.comments = filterFilter($scope.globals.comments, {groups: group.url});
            //UserService.filter('group', group.id).then(function(data) {
            //    $scope.comments = data;
            //});
        //};
        //angular.forEach($scope.groups, function(group) {
        //    group.comment_set = $scope.filterForGroup(group);
        //});

        $scope.startDragUser = function(comment) {
            $scope.draggedUser = comment;
            console.log(comment);
        };

        $scope.acceptUserToGroup = function(event, ui, group) {
            if (filterFilter(group.comment_set, {id: $scope.$eval(ui.draggable.ngattr('jqyoui-draggable')).index}) === 'undefined') {
                console.log(filterFilter(group.comment_set, {id: $scope.$eval(ui.draggable.ngattr('jqyoui-draggable')).index}));
                return true;
            } else {
                console.log(filterFilter(group.comment_set, {id: $scope.$eval(ui.draggable.ngattr('jqyoui-draggable')).index}));
                return false;
            }
        };

        $scope.addUsersToGroup = function(event, ui, group) {
            console.log(group.comment_set);
            console.log(filterFilter(group.comment_set, {id: $scope.$eval(ui.draggable.ngattr('jqyoui-draggable')).index}));
            console.log(ui.draggable.ngattr('ng-model'));
            console.log($scope.$eval(ui.draggable.ngattr('jqyoui-draggable')).index);
        };
        $scope.removeUserFromGroup = function(event, ui, group) {
            console.log('out');
            console.log(group);
            group.comment_set.pop($scope.draggedUser);
        };

        $scope.submitUser = function() {
            UserService.save($scope.comment).then(function(data) {
                $scope.comment = data;
                $scope.comments.push(data);
            }, function(status) {
                console.log(status);
            });
        };



    }]);

commentControllers.controller('UserDetailCtrl', ['$scope', '$http', '$routeParams', 'comment', function ($scope, $http, $routeParams, comment) {
    $scope.comment = comment;
    $scope.submit = function() {
        $http.post('/api/comments/' + $routeParams.commentId + '/', $scope.comment).success(function(comment_data) {
            $scope.comments.push(comment_data);
        });
    };
}]);


commentControllers.controller('GroupListCtrl', [
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
            var comment_set = [];
            // convert comment objects into urls for server
            angular.forEach(group.comment_set, function(comment) {
                if(comment.url){
                    this.push(comment.url.toString());
                }
            }, comment_set);
            $http.put(group.url,
                {
                    'id': group.id,
                    'name': group.name,
                    'url': group.url,
                    'comment_set':comment_set
                }
            ).success(function(data) {
                console.log(data);
            });
        };



    }]);

commentControllers.controller('MyFormCtrl', [
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
               data.comment_set = [
                    $scope.globals.comment.url
                ];
                $scope.submitGroup(data);

            }, function(status) {
                console.log(status);
            });
        };
        $scope.submitGroup = function(group) {
            GroupService.update(group).then(function(data) {
                $scope.group = data;
                $scope.group.comment_set = [
                    $scope.globals.comment
                ];
                $scope.group.tab = { active: true, disabled: false};
                $scope.globals.groups.push(data);
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



commentControllers.controller('ModalInstanceCtrl', [
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




