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