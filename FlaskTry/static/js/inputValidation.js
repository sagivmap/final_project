$("#NodeName").on("invalid", function (event) {
    event.target.setCustomValidity('Invalid Name')
}).bind('blur', function (event) {
    event.target.setCustomValidity('');
});

$("#CF").on("invalid", function (event) {
    event.target.setCustomValidity('Enter in format \\d+ or [(\\d+,)*\\d+]')
}).bind('blur', function (event) {
    event.target.setCustomValidity('');
});

$("#FD").on("invalid", function (event) {
    event.target.setCustomValidity('Enter in format \\d+ or [(\\d+,)*\\d+]')
}).bind('blur', function (event) {
    event.target.setCustomValidity('');
});

$("#MF").on("invalid", function (event) {
    event.target.setCustomValidity('Enter in format \\d+ or [(\\d+,)*\\d+]')
}).bind('blur', function (event) {
    event.target.setCustomValidity('');
});


function checkInputValidation() {
    name_ans = $('#NodeName')[0].reportValidity();
    tf_ans = $('#TF')[0].reportValidity();
    aua_ans = $('#AUA')[0].reportValidity();
    cf_ans = $('#CF')[0].reportValidity();
    fd_ans = $('#FD')[0].reportValidity();
    mf_ans = $('#MF')[0].reportValidity();

    return name_ans && tf_ans && aua_ans && cf_ans && fd_ans && mf_ans
}