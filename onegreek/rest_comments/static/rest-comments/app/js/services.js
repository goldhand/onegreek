'use strict';

/* Services */

var commentServices = angular.module('commentServices', ['ngResource']);


commentServices.factory('GlobalService', function () {
    var vars = {
        is_authenticated: false
    }
    return vars;
});


commentServices.factory('UserService', function ($http, $q) {
    var api_url = "/api/comments/";
    return {
        get: function (comment_id) {
            var url = api_url + comment_id + "/";
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
        update: function (comment) {
            var url = api_url + comment.id + "/";
            var defer = $q.defer();
            $http({method: 'PUT',
                url: url,
                data: comment}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
        save: function (comment) {
            var url = api_url;
            var defer = $q.defer();
            $http({method: 'POST',
                url: url,
                data: comment}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        }
    }
});

