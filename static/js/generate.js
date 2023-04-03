$(document).ready(function () {

    function generate_RSA() {
        $.ajax({
            url: '/generate_rsa/',
            dataType: 'json',
            success: function (response) {
                var values = response.values;
                document.getElementById('values-textarea-public-key').value = values['public'];
                document.getElementById('values-textarea-private-key').value = values['private'];
            },
        });
    }

    function generate_Diffie_Hellman() {
        $.ajax({
            url: '/generate_diffie_hellman/',
            dataType: 'json',
            success: function (response) {
                var value = response.value;
                document.getElementById('value-textarea-diffie_hellman-key').value = value;
            },
        });
    }

    $('.generate-btn').click(generate);
    function generate() {
        if ($('.algorithm option:selected').val() === 'RSA') {
            generate_RSA()
        }
        else if ($('.algorithm option:selected').val() === 'Diffie-Hellman') {
            generate_Diffie_Hellman()
        }
    }
});
