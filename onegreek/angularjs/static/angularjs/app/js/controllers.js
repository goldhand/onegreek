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

myApp.controller('AlertDemoCtrl', ['$scope', 'alert', function ($scope, alert) {

    $scope.$on( 'alerts.update', function( event ) {
        $scope.alerts = alert.alerts;
    });
    $scope.alerts = alert.alerts;

    $scope.addAlert = function() {
        alert.addAlert(
            { type: 'error', msg: 'Oh snap! Change a few things up and try submitting again.' }
        );
    };
    $scope.closeAlert = function( index ) {
        alert.closeAlert(index);
    };

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

myApp.controller('TabsDemoCtrl', ['$scope', function ($scope) {
  $scope.tabs = [
    { title:"Dynamic Title 1", content:"Dynamic content 1" },
    { title:"Dynamic Title 2", content:"Dynamic content 2", disabled: true }
  ];

  $scope.alertMe = function() {
    setTimeout(function() {
      alert("You've selected the alert tab!");
    });
  };

  $scope.navType = 'pills';
}]);


myApp.controller('TimepickerDemoCtrl', ['$scope', function ($scope) {
  $scope.mytime = new Date();

  $scope.hstep = 1;
  $scope.mstep = 15;

  $scope.options = {
    hstep: [1, 2, 3],
    mstep: [1, 5, 10, 15, 25, 30]
  };

  $scope.ismeridian = true;
  $scope.toggleMode = function() {
    $scope.ismeridian = ! $scope.ismeridian;
  };

  $scope.update = function() {
    var d = new Date();
    d.setHours( 14 );
    d.setMinutes( 0 );
    $scope.mytime = d;
  };

  $scope.changed = function () {
    console.log('Time changed to: ' + $scope.mytime);
  };

  $scope.clear = function() {
    $scope.mytime = null;
  };
}]);

myApp.controller('TooltipDemoCtrl', ['$scope', function ($scope) {
  $scope.dynamicTooltip = "Hello, World!";
  $scope.dynamicTooltipText = "dynamic";
  $scope.htmlTooltip = "I've been made <b>bold</b>!";
}]);

myApp.controller('TypeaheadCtrl', ['$scope', function($scope) {

  $scope.selected = undefined;
  $scope.states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Dakota', 'North Carolina', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'];
}]);


myApp.controller('PopoverDemoCtrl', ['$scope', function ($scope) {
  $scope.dynamicPopover = "Hello, World!";
  $scope.dynamicPopoverText = "dynamic";
  $scope.dynamicPopoverTitle = "Title";
}]);



myApp.controller('DatepickerDemoCtrl', ['$scope', '$timeout', function ($scope, $timeout) {
  $scope.today = function() {
    $scope.dt = new Date();
  };
  $scope.today();

  $scope.showWeeks = true;
  $scope.toggleWeeks = function () {
    $scope.showWeeks = ! $scope.showWeeks;
  };

  $scope.clear = function () {
    $scope.dt = null;
  };

  // Disable weekend selection
  $scope.disabled = function(date, mode) {
    return ( mode === 'day' && ( date.getDay() === 0 || date.getDay() === 6 ) );
  };

  $scope.toggleMin = function() {
    $scope.minDate = ( $scope.minDate ) ? null : new Date();
  };
  $scope.toggleMin();

  $scope.open = function() {
    $timeout(function() {
      $scope.opened = true;
    });
  };

  $scope.dateOptions = {
    'year-format': "'yyyy'",
    'month-format': "'mm'",
    'starting-day': 1
  };
}]);

myApp.controller('MyFormCtrl', ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
    $scope.submit = function() {
        $http.post('/api/events/', $scope.events).success(function(out_data) {
            // do something
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
