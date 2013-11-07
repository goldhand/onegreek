'use strict';

/* Services */

myApp.service('item', ['$rootScope', function( $rootScope ) {
    var service = {

        items: ['Item 1', 'Item 2', 'Item 3'],

        addItem: function ( item ) {
            service.items.push( item );
            $rootScope.$broadcast('items.update');
        }
    };
    return service;

}]);

