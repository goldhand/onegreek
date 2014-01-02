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
    'filterFilter',
    'GlobalService',
    function (
        $scope,
        $http,
        filterFilter,
        GlobalService
        ) {

        $scope.globals = GlobalService;
        $scope.Search = undefined;

        $scope.getChapters = function() {
            $http.get('/api/chapters/').success(function(data) {
                $scope.chapters = data;
            });
        };
        $scope.getChapters();

        $scope.getEvents = function() {
            $http.get('/api/events/').success(function(data) {
                $scope.events = data;
                $scope.globals.events = data;
            });
        };
        $scope.getEvents();

        $scope.globals.filterForChapter = function(chapter) {
            if(!(chapter)){
                $scope.events = $scope.globals.events;
            } else {
                $scope.events = filterFilter($scope.globals.events, {chapter_id: chapter.id});
            }
        };


    }]);

chapterControllers.controller('ChapterDetailCtrl', [
    '$scope',
    '$http',
    '$modal',
    '$routeParams',
    'filterFilter',
    'GlobalService',
    function (
        $scope,
        $http,
        $modal,
        $routeParams,
        filterFilter,
        GlobalService
        ) {
        $scope.globals = GlobalService;
        $scope.globals.ogLoading = {
            chapter: false,
            rush: false,
            users: false,
            comments: false,
            images: false
        };
        $scope.globals.filterForChapter = function(chapter) {
            if(!(chapter)){
                $scope.events = $scope.globals.events;
            } else {
                $scope.events = filterFilter($scope.globals.events, {chapter_id: chapter.id});
            }
        };

        $scope.getChapterRush = function(rush_url) {
            $http.get(rush_url).success(function(data) {
                $scope.chapter.rush = {
                    title: data.title,
                    hide: data.hide,
                    disabled: data.disabled,
                    message: { hide: true, text: data.message },
                    rushing: data.rushing
                };
                $scope.globals.ogLoading.rush = true;
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
                    $scope.getImages(data.ctype_id, data.id);
                }
                // filters events for chapter
                $scope.globals.filterForChapter(data.id);
                // chapter loading done
                $scope.globals.ogLoading.chapter = true;
            });
        };

        $scope.getUsers = function(chapter_id) {
            $http.get('/api/users/?chapter=' + chapter_id).success(function(data) {
                $scope.users = data;
                $scope.globals.ogLoading.users = true;
            });
        };

        $scope.getComments = function(ctype, obj) {
            $http.get('/api/comments/?ctype=' + ctype + '&obj=' + obj).success(function(data) {
                $scope.comments = data;
                $scope.globals.ogLoading.comments = true;
            });
        };
        $scope.getImages = function(ctype, obj) {
            $http.get('/api/images/?ctype=' + ctype + '&obj=' + obj).success(function(data) {
                console.log(data);
                $scope.images = data;
                $scope.globals.ogLoading.images = true;
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
            if(!($scope.chapter.rush.disabled)) {
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












