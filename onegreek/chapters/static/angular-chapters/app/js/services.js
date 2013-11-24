'use strict';

/* Services */

var chapterServices = angular.module('chapterServices', ['ngResource']);


chapterServices.factory('GlobalService', function () {
    var vars = {
        is_authenticated: false
    }
    return vars;
});


chapterServices.factory('ChapterService', function ($http, $q) {
    var api_url = "/api/chapters/";
    return {
        get: function (chapter_id) {
            var url = api_url + chapter_id + "/";
            var defer = $q.defer();
            $http({method: 'GET', url: url}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                })
                .error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
        list: function () {
            var defer = $q.defer();
            $http({method: 'GET', url: api_url}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
        filter: function (query, query_id) {
            var defer = $q.defer();
            var url = api_url + '?' + query + '=' + query_id;
            $http({method: 'GET', url: url, isArray:true}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
        update: function (chapter) {
            var url = api_url + chapter.id + "/";
            var defer = $q.defer();
            $http({method: 'PUT',
                url: url,
                data: chapter}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
        save: function (chapter) {
            var url = api_url;
            var defer = $q.defer();
            $http({method: 'POST',
                url: url,
                data: chapter}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        }
    }
});

