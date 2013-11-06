'use strict';

/* Directives */


myApp.directive('nuAddItemButton', ['item', function( item ) {
    return {
        restrict: "A",
        link: function( scope, element, attrs ) {
            element.bind( "click", function() {
                item.addItem( 'newItem' );
                //var newItemNo = group.items.length + 1;
                //var newItem = ('Item ' + newItemNo);
        });
        }
    };
}]);

myApp.directive('contenteditable', function() {
    return {
        require: 'ngModel',
        link: function(scope, elm, attrs, ctrl) {
            // view -> model
            elm.on('blur', function() {
                scope.$apply(function() {
                    ctrl.$setViewValue(elm.html());
                });
            });

            // model -> view
            ctrl.$render = function() {
                elm.html(ctrl.$viewValue);
            };

            // load init value from DOM
            ctrl.$setViewValue(elm.html());
        }
    };
});
