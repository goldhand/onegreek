'use strict';

/* Directives */

var userDirectives = angular.module('userDirectives', []);

userDirectives.directive('groupDisplay', [function () {
    //Cuts the chapter_X prefix from group names
    return {
        templateUrl: 'group-display.html',
        restrict: 'E',
        link: function link(scope, element, attrs) {
                var re = /^\w+?\d+?\s/;
                scope.groupName = scope.group.name.split(re)[1];
            }
    }

}]);
