'use strict';

/* Directives */

var userDirectives = angular.module('userDirectives', []);

userDirectives.directive('dragUser', ['$document', function ($document) {
    return function (scope, element, attr) {

        element.css({
            position: 'relative',
            cursor: 'pointer'
        });
        var startX = element.pageX, startY = element.pageY, x = 0, y = 0;

        element.on('mousedown', function (event) {
            // Prevent default dragging of selected content
            event.preventDefault();
            startX = event.pageX - x;
            startY = event.pageY - y;
            $document.on('mousemove', mousemove);
            $document.on('mouseup', mouseup);
        });

        function mousemove(event) {
            y = event.pageY - startY;
            x = event.pageX - startX;
            element.css({
                top: y + 'px',
                left: x + 'px'
            });
        }

        function mouseup() {
            $document.unbind('mousemove', mousemove);
            $document.unbind('mouseup', mouseup);
        }
    }
}]);
