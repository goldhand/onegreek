'use strict';

/* Services */

usersApp.service('User', ['$rootScope', '$resource', function( $rootScope, $resource ) {
    return $resource('/api/users/:userId/', {}, {
        query: {method: 'GET', params:{ userId:'users'}, isArray:true}
    });

}]);


