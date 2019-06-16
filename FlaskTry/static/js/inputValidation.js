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

function check_MF_and_FD(TF_AUA, MF_FD) {
    var i;
    for (i=0; i < MF_FD.length; i++) {
        if (MF_FD[i] > TF_AUA) {
            return false;
        }
    }
    return true;
}

function checkPatterns() {
    name_ans = $('#NodeName')[0].reportValidity();
    tf_ans = $('#TF')[0].reportValidity();
    aua_ans = $('#AUA')[0].reportValidity();
    cf_ans = $('#CF')[0].reportValidity();
    fd_ans = $('#FD')[0].reportValidity();
    mf_ans = $('#MF')[0].reportValidity();
    return name_ans && tf_ans && aua_ans && cf_ans && fd_ans && mf_ans
}

function checkCfMfFdLengths(cf, mf, fd) {
    if (!(cf.length === mf.length && cf.length === fd.length)) {
        window.alert('CF, MF and FD lengths should be the same');
        return false;
    }
    return true;
}

function checkCorelateInput(tf,mf,aua,fd) {
    if (!check_MF_and_FD(tf, mf)) {
        if (mf.length == 1) {
            window.alert("MF should be less then TF");
        } else {
            window.alert("All MF should be less then TF");
        }
        return false;
    }
    if (!check_MF_and_FD(aua, fd)) {
        if (mf.length == 1) {
            window.alert("FD should be less then AUA");
        } else {
            window.alert("All FD should be less then AUA");
        }
        return false;
    }
    return true;
}

function checkDuplicateCF(cf) {
    var arrLen = cf.length;
    var setCf = new Set(cf);
    if (arrLen > setCf.size) {
        window.alert("There duplicate CF.");
        return false;
    }
    return true;
}

function checkInputValidation() {

    if (checkPatterns()){
        var name = document.getElementById("NodeName").value,
            tf = parseInt(document.getElementById("TF").value),
            aua = parseInt(document.getElementById("AUA").value),
            cf = document.getElementById("CF").value.split(",").map(function (num) { return parseInt(num, 10); }),
            mf = document.getElementById("MF").value.split(",").map(function (num) { return parseInt(num, 10); }),
            fd = document.getElementById("FD").value.split(",").map(function (num) { return parseInt(num, 10); });

        if (checkDuplicateCF(cf)) {
            if (checkCfMfFdLengths(cf, mf, fd)) {
                if (checkCorelateInput(tf, mf, aua, fd, cf)) {
                    return true;
                }
            }
        }
    }

    return false;
}