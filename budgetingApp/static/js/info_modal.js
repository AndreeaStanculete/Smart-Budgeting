function updateInformation(id, type) {
    var financeData = ["type", "amount", "currency", "periodical", "date"];
    var modalId = "#" + type + "Information";

    financeData.forEach(function(dataType) {
        var infoLabelName = modalId + " #" + dataType + "Show";
        var dataHolderName = "#" + dataType + "_" + id;
        var actualValue = $(dataHolderName).val();

        $(infoLabelName).val(actualValue);
    });

    console.log(modalId + " #updateId");
    $(modalId + " #updateId").val( id );
}

$(document).ready(function() {
    $(".deleteToggler").click(function(){
        $(".deleteText").toggle();
    });

    $(".showIncome").click(function(){
        var id = $(this).data('id');
        updateInformation(id, 'Income');
    
        $("#IncomeInformation").modal('show');
    });

    $(".showExpense").click(function(){
        var id = $(this).data('id');
        updateInformation(id, 'Expense');
    
        $("#ExpenseInformation").modal('show');
    });

    $(".edit").click(function(){
        $(".infoDisplay").prop('disabled', (i, v) => !v);

        $("#editShow").toggle();
        $("#editClose").toggle();
    });
});
