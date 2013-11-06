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
