'use strict';

/* Controllers */

var chapterControllers = angular.module('chapterControllers', []);

chapterControllers.controller('ChapterGlobalCtrl', [
    '$scope',
    '$rootScope',
    '$location',
    '$timeout',
    'GlobalService',
    function ($scope, $rootScope, $location, $timeout, GlobalService) {

        $scope.globals = GlobalService;
        $scope.globals.chapters = undefined;
        var failureCb = function (status) {
            console.log(status);
        };
        $scope.initialize = function (is_authenticated, user_id, user_chapter_id, chapter_id, host) {
            $scope.globals.is_authenticated = is_authenticated;
            $scope.globals.user_id = user_id;
            $scope.globals.user_chapter_id = user_chapter_id;
            $scope.globals.chapter_id = chapter_id;
            $scope.globals.host = host;
        };

}]);


chapterControllers.controller('ChapterListCtrl', [
    '$scope',
    '$http',
    'GlobalService',
    function (
        $scope,
        $http,
        GlobalService
        ) {

        $scope.globals = GlobalService;
        $scope.getChapters = function() {
            $http.get('/api/chapters/').success(function(data) {
                $scope.chapters = data;
            });
        };
        $scope.getChapters();

        $scope.Search = undefined;

    }]);

chapterControllers.controller('ChapterDetailCtrl', [
    '$scope',
    '$http',
    '$modal',
    '$routeParams',
    'GlobalService',
    function (
        $scope,
        $http,
        $modal,
        $routeParams,
        GlobalService
        ) {
        $scope.globals = GlobalService;

        $scope.getChapterRush = function(rush_url) {
            $http.get(rush_url).success(function(data) {
                console.log(data);
                $scope.chapter.rush = {
                    title: data.title,
                    hide: data.hide,
                    disabled: data.disabled,
                    message: { hide: true, text: data.message },
                    rushing: data.rushing
                };
            });
        };

        $scope.getChapter = function(chapter_id) {
            $http.get('/api/chapters/' + chapter_id + '/').success(function(data) {
                $scope.chapter = data;
                if(data.rush_url) {
                    $scope.getChapterRush(data.rush_url);
                }
                if(data.ctype_id) {
                    $scope.getComments(data.ctype_id, data.id);
                }
            });
        };

        $scope.getUsers = function(chapter_id) {
            $http.get('/api/users/?chapter=' + chapter_id).success(function(data) {
                $scope.users = data;
            });
        };

        $scope.getComments = function(ctype, obj) {
            $http.get('/api/comments/?ctype=' + ctype + '&obj=' + obj).success(function(data) {
                $scope.comments = data;
            });
        };

        $scope.rushSubmit = function() {
            $http.post($scope.chapter.rush_url).success(function(data) {
                $scope.chapter.rush.title = data.title;
                $scope.chapter.rush.message.text = data.message;
                $scope.chapter.rush.message.hide = false;
                $scope.chapter.rush.rushing = data.rushing;
            });
        };
        $scope.rushFormSubmit = function() {
            $http.post($scope.chapter.rush_form_url, $scope.rush_form).success(function(data) {
                console.log(data);
            });
        };
        $scope.commentSubmit = function() {

            $.ajax({
                url: "/api/comments/",
                type: "POST",
                data: $('#restcomment-form').serialize(),
                success: function(data) {
                    $scope.getComments($scope.chapter.ctype_id, $scope.chapter.id);

                }
            });
        };

        $scope.getChapter($scope.globals.chapter_id);
        $scope.getUsers($scope.globals.chapter_id);

        $scope.rush_form = {};

        $scope.openModal = function () {
            if(!($scope.chapter.rush.rushing)) {

                var modalInstance = $modal.open({
                    templateUrl: 'RushFormModal.html',
                    controller: 'ModalInstanceCtrl',
                    resolve: {
                        rush_form: function () {
                            return $scope.rush_form;
                        }
                    }
                });

                modalInstance.result.then(function (rush_form) {
                    $scope.rush_form = rush_form;
                    $scope.rushFormSubmit();
                    $scope.rushSubmit();
                }, function () {});
            } else {
                $scope.rushSubmit();
            }
        };
}]);


chapterControllers.controller('ModalInstanceCtrl', [
    '$scope',
    '$timeout',
    '$modalInstance',
    'rush_form',
    function (
        $scope,
        $timeout,
        $modalInstance,
        rush_form
        ) {
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
        $scope.rush_form = rush_form;

        $scope.ok = function () {
            console.log($scope.rush_form);
            $modalInstance.close($scope.rush_form);
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    }]);
