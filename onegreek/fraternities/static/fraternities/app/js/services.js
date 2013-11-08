'use strict';

/* Services */

eventsApp.service('Event', ['$rootScope', '$resource', function( $rootScope, $resource ) {
    return $resource('/api/events/:eventId/', {}, {
        query: {method: 'GET', params:{ eventId:'events'}, isArray:true}
    });

}]);

eventsApp.service('')

