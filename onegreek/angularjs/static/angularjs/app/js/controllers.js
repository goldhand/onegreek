'use strict';

/* Controllers */

myApp.controller('AccordionDemoCtrl', ['$scope', function($scope) {
        $scope.oneAtATime = true;

        $scope.groups = [
            {
                title: "Header 1",
                content: "Body 1"
            },
            {
                title: "Header 2",
                content: "Body 2"
            }
        ];

        $scope.items = ['Item 1', 'Item 2', 'Item 3'];

        $scope.addItem = function() {
            var newItemNo = $scope.items.length + 1;
            $scope.items.push('Item ' + newItemNo);
        };

    }]);
