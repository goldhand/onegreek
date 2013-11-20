'use strict';

/* Controllers */

var chapterControllers = angular.module('chapterControllers', []);

chapterControllers.controller('ChapterGlobalCtrl', [
    '$scope', '$rootScope', '$location', '$timeout', 'GlobalService',
    function ($scope, $rootScope, $location, $timeout, GlobalService) {

        $scope.globals = GlobalService;
        $scope.globals.chapters = undefined;
        var failureCb = function (status) {
            console.log(status);
        };
        $scope.initialize = function (is_authenticated, user_id, chapter_id, host) {
            $scope.globals.is_authenticated = is_authenticated;
            $scope.globals.chapter_id = user_id;
            $scope.globals.chapter_id = chapter_id;
            $scope.globals.host = host;
            console.log(host);
        };

}]);


chapterControllers.controller('ChapterListCtrl', [
    '$scope',
    '$http',
    'filterFilter',
    'ChapterService',
    'GlobalService',
    'chapters',
    function (
        $scope,
        $http,
        filterFilter,
        ChapterService,
        GlobalService,
        chapters
        ) {

        $scope.chapter = {};
        $scope.chapters = chapters;
        $scope.globals = GlobalService;


        if($scope.globals.chapters == undefined) {
            $scope.globals.chapters = chapters;
        }
        if($scope.globals.chapter == undefined) {
            $scope.globals.chapter = filterFilter($scope.globals.chapters, {id: $scope.globals.chapter_id})[0];
        }

        $scope.Search = undefined;

        $scope.submitChapter = function() {
            ChapterService.save($scope.chapter).then(function(data) {
                $scope.chapter = data;
                $scope.chapters.push(data);
            }, function(status) {
                console.log(status);
            });
        };



    }]);

chapterControllers.controller('ChapterDetailCtrl', ['$scope', '$http', '$routeParams', 'chapter', function ($scope, $http, $routeParams, chapter) {
    $scope.chapter = chapter;
    $scope.chapter.rush = {
        title: 'Rush ' + $scope.chapter.fraternity_title,
        hide: false,
        message: {
            hide: true,
            text: ''
        }
    };


    $scope.submit = function() {
        $http.post('/api/chapters/' + $routeParams.chapterId + '/', $scope.chapter).success(function(chapter_data) {
            $scope.chapters.push(chapter_data);
        });
    };
    $http.get($scope.chapter.rush_url).success(function(data) {
        $scope.chapter.rush.title = data.title;
        $scope.chapter.rush.message.hide = true;
    });
    $scope.rushSubmit = function() {
        $http.post($scope.chapter.rush_url).success(function(data) {
            //$scope.chapter.rush.hide = true;
            $scope.chapter.rush.title = data.title;
            $scope.chapter.rush.message.text = data.message;
            $scope.chapter.rush.message.hide = false;
        });
    };

}]);

