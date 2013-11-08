'use strict';

/* Controllers */

eventsApp.controller('MyFormCtrl', ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
    $http.get('/api/events/').success(function(data) {
      $scope.events = data;
    });
    $scope.submit = function() {
        $http.post('/api/events/', $scope.newEvent).success(function(event_data) {
            $scope.events.push(event_data);
        });
    };

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
    $scope.dateOptions = {
        'year-format': "'yyyy'",
        'month-format': "'mm'",
        'starting-day': 1
    };
    $scope.hstep = 1;
    $scope.mstep = 15;
    $scope.ismeridian = true;
}]);

myApp.controller('ModalDemoCtrl', ['$scope', '$modal', '$log', function ($scope, $modal, $log) {

    $scope.items = ['item1', 'item2', 'item3'];

    $scope.open = function () {

        var modalInstance = $modal.open({
            templateUrl: 'myModalContent.html',
            controller: 'ModalInstanceCtrl',
            resolve: {
                items: function () {
                    return $scope.items;
                }
            }
        });

        modalInstance.result.then(function (selectedItem) {
            $scope.selected = selectedItem;
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };
}]);

myApp.controller('ModalInstanceCtrl', ['$scope', '$modalInstance', 'items', function ($scope, $modalInstance, items) {

    $scope.items = items;
    $scope.selected = {
        item: $scope.items[0]
    };

    $scope.ok = function () {
        $modalInstance.close($scope.selected.item);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}]);
