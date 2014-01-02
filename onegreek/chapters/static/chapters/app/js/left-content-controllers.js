
var leftContentControllers = angular.module('leftContentControllers', []);

leftContentControllers.controller('LeftContentCtrl', [
    '$scope',
    '$http',
    function (
        $scope,
        $http
        ) {
        $http.get('/api/chapters/').success(function(data) {
            $scope.chapters = data;
            $http.get('/api/events/').success(function(data) {
                $scope.events = data;
                $scope.searchQuerySet = $scope.events.concat($scope.chapters);
                $http.get('/api/users/').success(function(data) {
                    $scope.users = data;
                    $scope.searchQuerySet = $scope.searchQuerySet.concat($scope.users);
                });

            });
        });

    }]);


