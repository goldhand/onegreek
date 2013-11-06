'use strict';

/* Controllers */

myApp.controller('AccordionDemoCtrl', ['$scope', 'group', 'item', function($scope, group, item) {
        $scope.oneAtATime = true;

        $scope.$on( 'items.update', function( event ) {
            $scope.items = item.items;
        });

        $scope.items = item.items;
        $scope.groups = group.groups;
        $scope.addItem = function() {
            item.addItem('item');
        };

    }]);
