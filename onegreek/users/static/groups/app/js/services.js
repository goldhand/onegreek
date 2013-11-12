'use strict';

/* Services */

var groupServices = angular.module('groupServices', ['ngResource']);


groupServices.factory('GroupService', function ($http, $q) {
    var api_url = "/api/groups/";
    return {
        get: function (group_id) {
            var url = api_url + group_id + "/";
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
            $http({method: 'GET', url: api_url, isArray:true}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                    console.log(data);
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
                    console.log(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
        update: function (group) {
            var url = api_url + group.id + "/";
            var defer = $q.defer();
            $http({method: 'PUT',
                url: url,
                data: group}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
        save: function (group) {
            var url = api_url;
            var defer = $q.defer();
            $http({method: 'POST',
                url: url,
                data: group}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        }
    }
});

