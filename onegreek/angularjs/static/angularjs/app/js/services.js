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


myApp.service('group', [function() {

    return {
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

}]);

myApp.service('alert', ['$rootScope', function( $rootScope ) {
var service = {
        alerts: [
        { type: 'error', msg: 'Oh snap! Change a few things up and try submitting again.' },
        { type: 'success', msg: 'Well done! You successfully read this important alert message.' }
        ],

    addAlert: function( msg ) {
        service.alerts.push( msg );
        $rootScope.$broadcast( 'alerts.update' );
        },

    closeAlert: function(index) {
        service.alerts.splice(index, 1);
        $rootScope.$broadcast( 'alerts.destroy' );
        }
    };
    return service;
}]);
