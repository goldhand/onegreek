'use strict';

/* Services */

var eventServices = angular.module('eventServices', ['ngResource']);


eventServices.factory('Event', ['$resource', function( $resource ) {
    return $resource('/api/events/:eventId/', {}, {
        query: {method: 'GET', params:{ eventId:''}, isArray:true}
    });
}]);


eventServices.factory('EventService', function ($http, $q) {
    var api_url = "/api/events/";
    return {
        get: function (event_id) {
            var url = api_url + event_id + "/";
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
        update: function (event) {
            var url = api_url + event.id + "/";
            var defer = $q.defer();
            $http({method: 'PUT',
                url: url,
                data: event}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
        save: function (event) {
            var url = api_url;
            var defer = $q.defer();
            $http({method: 'POST',
                url: url,
                data: event}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        }
    }
});
