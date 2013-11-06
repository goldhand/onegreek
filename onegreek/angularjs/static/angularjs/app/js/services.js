'use strict';

/* Services */

myApp.service('item', ['$rootScope', function( $rootScope ) {
    var service = {

        items: ['Item 1', 'Item 2', 'Item 3'],

        addItem: function ( item ) {
            service.items.push( item );
            $rootScope.$broadcast('items.update');
        }
    }
    return service;

}]);


myApp.service('group', ['$rootScope', function( $rootScope ) {

    var service = {
        groups: [
            {
                title: "Header 1",
                content: "Body 1"
            },
            {
                title: "Header 2",
                content: "Body 2"
            }
        ]
    };
    return service;

}]);

