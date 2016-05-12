$(document).ready(function(){
    $(".ui-monthpicker").datepicker({
        dateFormat: 'MM yy',
        changeMonth: true,
        changeYear: true,
        showButtonPanel: true,
        beforeShow: function(input, inst) {
            inst.dpDiv.addClass('month_year_datepicker');

            var date_str = $(this).val();

            if (date_str.length > 0) {
                var date = new Date(Date.parse(date_str));
                $(this).datepicker('option', 'defaultDate', date);
                $(this).datepicker('setDate', date)
            }
        },
        onClose: function() {
            var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
            var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
            $(this).datepicker('setDate', new Date(year, month, 1)).trigger('change');
        }
    });
});