var modules = ['angular.filter', 'ngRoute', 'djng.urls', 'daterangepicker'].filter(function (module) {
    try {
        return !!angular.module(module);
    } catch (e) {
        console.log(module  + " No se pudo cargar");
    }
});


var app = angular.module('app', modules);


app.run(['$rootScope', '$route', '$templateCache',
         function($rootScope, $route, $templateCache) {
    $rootScope.$on('$routeChangeSuccess', function() {
        document.title = $route.current.title;
        elems = angular.element('li.active');
        angular.forEach(elems, function(el) { el.classList.remove('active'); });
        document.getElementById($route.current.currenttab).className = 'active';
    });
}]);

app.config(function($routeProvider, $httpProvider, $locationProvider) {
    $routeProvider.when('/uf/list', {
        title      : 'Historico valor de UF',
        templateUrl: '/static/frontend/uf/list.html',
        controller : 'ufvaluectrl',
        currenttab : 'uflist'
    }).when('/uf/price', {
        title      : 'Detalle de precio por fecha',
        templateUrl: '/static/frontend/uf/price.html',
        controller : 'ufvaluectrl',
        currenttab : 'ufprice'
    }).otherwise({
        redirectTo: '/uf/list'
    });
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $locationProvider.html5Mode(true);
});