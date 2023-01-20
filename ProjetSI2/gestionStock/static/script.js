$(function () {
    $(document).ready(function () {
        $('#search').DataTable();
    });
});

$(function () {
    $(document).ready(function () {
        $('#noSearch').DataTable({
            "searching":false,
        });
    });
});



$(function () {
    $(document).ready(function () {
        $('#dernier').DataTable({
            columnDefs: [
                { "searchable": false, "targets":-1},
            ]
        });
    });
});

$(function () {
    $(document).ready(function () {
        $('#deuxF').DataTable({
            columnDefs: [
                { "searchable": false, "targets":[2,3,4,5]},
            ]
        });
    });
});