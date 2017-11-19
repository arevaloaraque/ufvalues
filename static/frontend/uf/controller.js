'user strict';

// extend initial module
var app = angular.module(['app']);
var localSettingsBlockUI = {
    message: '<img src="/static/img/loading.gif" /> ' + 'Cargando, espere por favor...',
    css: {
        border: 'none',
        padding: '15px',
        backgroundColor: '#000',
        '-webkit-border-radius': '10px',
        '-moz-border-radius': '10px',
        opacity: '.5',
        color: '#fff'
    }
};
var notify = {};

app.controller('ufvaluectrl', ['$scope','djangoUrl', '$http', '$filter', '$location', 
               function($scope, djangoUrl, $http, $filter, $location){
    $scope.options       = [];
    $scope.days          = [];
    $scope.monthLabels   = [
        'Enero',
        'Febrero',
        'Marzo',
        'Abril',
        'Mayo',
        'Junio',
        'Julio',
        'Agosto',
        'Septiembre',
        'Octubre',
        'Noviembre',
        'Diciembre',
    ];
    $scope.selected_year = (new Date).getFullYear();
    $scope.historical    = [];
    $scope.ufvalues      = [];
    $scope.date;
    $scope.value;
    $scope.selected;
    $scope.total;
    /**
     * Create options for select years and days
     **/
    for (var x=1977; x<=(new Date()).getFullYear();x++) { $scope.options.push(x); }
    for (var x=1; x<=31;x++) { $scope.days.push(x); }


    /**
     * Load data by year
     **/
    $scope.loadData = function(_date){
        $.blockUI(localSettingsBlockUI);
        $http({
            method : 'GET',
            url    : djangoUrl.reverse('uf:uf-list'),
            params : {'year': _date},
            headers: { 'Content-Type': 'application/json; charset=UTF-8' },
        }).then(function(response) {
            $scope.historical = response.data;
            $scope.groupBy();
            $.unblockUI();
        }, function(err){
            $.unblockUI();
            if (typeof(notify.close) != 'undefined') { notify.close(); }
            notify = $.notify({
                'message' : '<b>Ocurrio un error inesperado</b>',
                'icon'    : 'glyphicon glyphicon-alert',
            },{
                'newest_on_top': true,
                'type'         : 'danger',
            });
        });
    };
    if ($location.path() == '/uf/list') {
        if (typeof($scope.$parent.initialdata) != 'undefined') {
            delete $scope.$parent.initialdata;
        }
        $scope.date     = '';
        $scope.value    = '';
        $scope.selected = '';
        $scope.total    = '';
        $scope.loadData($scope.selected_year);
    }
    

    /**
     * Sort and group date by day to display in table.
     **/
    $scope.groupBy = function(){
        var groups = [
            [], [], [], [], [], [], [], [], [], [],
            [], [], [], [], [], [], [], [], [], [],
            [], [], [], [], [], [], [], [], [], [], [],
        ], itemGroupedByDays = [];
        var items = $scope.historical;
        for (var i = 0; i < items.length; i++) {
            var index = items[i]['key'].substring(0, 2);
            groups[index-1].push(items[i]);
            if (i == (items.length-1)) {
                for (var z = 0; z < groups.length; z++) {
                    if (groups[z].length) {
                        itemGroupedByDays.push({
                            day  : z+1,
                            items: groups[z]
                        });
                        if (z == (groups.length-1)) {
                            $scope.ufvalues = itemGroupedByDays;
                        }
                    }
                }
            }
        }
    };


    /**
     * Verify day or autocomplete with blank space
     **/
    $scope.verifyDay = function(index, date, day, items){
        if (typeof(date) != 'undefined' && (parseInt(index)+1) === parseInt(date.key.substring(2, 4))) {
            return $filter('number')(date.value, 2);
        } else {
            var newindex = (('0' + day).slice(-2).toString() + (('0' + (index+1)).slice(-2).toString())).toString();
            var filter   = {'key': newindex+$scope.selected_year}
            var filtered = $filter('filter')(items, filter, true);
            if (filtered.length>0) {
                return $filter('number')(filtered[0].value, 2);
            } else {
                return '';
            }
        }
    };


    /**
     * Initial settings for calendar
     **/
    $scope.datePicker        = {};
    $scope.datePicker.date   = '';
    $scope.datepickerOptions = {
        singleDatePicker: true,
        locale          : {
            separator : ' - ',
            format    : "DD/MM/YYYY",
            monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                         'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        },
    };


    /**
     * Verify initial data
     **/
    if (typeof($scope.$parent.initialdata) != 'undefined') {
        angular.forEach($scope.$parent.initialdata, function(value, index) {
            if (index == 'date') {
                $scope.datePicker.date = moment(value, "YYYYMMDD");
            } else {
                $scope[index] = value;
            }
        }, this);
    }


    /**
     * Observable method for update scope with data by index
     **/
    $scope.$watch('datePicker.date', function(old_value, new_value){
        var selected_date = moment($scope.datePicker.date).format('YYYYMMDD');
        if (selected_date == 'Invalid date') {
            $scope.date = '';
        } else {
            $scope.date = selected_date;
        }
    }, true);
    $scope.$watch('selected', function(old_value, new_value){
        if ($scope.selected != undefined) {
            $scope.total = parseFloat($scope.value) / parseFloat($scope.selected);
        }
    }, true);
}]);