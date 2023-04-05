$(document).ready(function() {
	if($(".result-text").text() == "") {
		$('.result-file').css('display', 'none');
		$('.clear-btn').css('display', 'none');
        $('.copy-btn').css('display', 'none');
	}
    if($(".text").text() == "") {
        $('.text-delete-btn').css('display', 'none');
	}
    $('.text').on('input', function() {
        if ($(this).val().length > 0) {
            $('.text-delete-btn').show();
        } else {
            $('.text-delete-btn').hide();
        }
    });


	if ($('#id_action_0').is(':checked')) {
		$('#id_action_0').parent().addClass('action-active');
	}
	if ($('#id_action_1').is(':checked')) {
		$('#id_action_1').parent().addClass('action-active');
	}
    $(document).on("change",".action",function() {
		if ($('#id_action_0').is(':checked')) {
			$('#id_action_0').parent().addClass('action-active');
		} else if ($('#id_action_0').is(':checked') == false) {
			$('#id_action_0').parent().removeClass('action-active');
		}
		if ($('#id_action_1').is(':checked')) {
			$('#id_action_1').parent().addClass('action-active');
		} else if ($('#id_action_1').is(':checked') == false) {
			$('#id_action_1').parent().removeClass('action-active');
		}
	});


	$('.input-file input[type=file]').on('change', function(){
		let file = this.files[0];
		$(this).next().html(file.name);
	});


	$('.algorithm').each(function() {
        const _this = $(this),
            selectOption = _this.find('option'),
            selectOptionLength = selectOption.length,
            duration = 450;

        _this.hide();
        _this.wrap('<div class="algorithm"></div>');
        $('<div>', {
            class: 'new-select',
            text: _this.children('option:selected').text()
        }).insertAfter(_this);

        const selectHead = _this.next('.new-select');
        $('<div>', {
            class: 'new-select__list'
        }).insertAfter(selectHead);

        const selectList = selectHead.next('.new-select__list');
        for (let i = 0; i < selectOptionLength; i++) {
            $('<div>', {
                class: 'new-select__item',
                html: $('<span>', {
                    text: selectOption.eq(i).text()
                })
            })
            .attr('data-value', selectOption.eq(i).val())
            .appendTo(selectList);
        }

        const selectItem = selectList.find('.new-select__item');
        selectList.slideUp(0);
        selectHead.on('click', function() {
            if ( !$(this).hasClass('on') ) {
                $(this).addClass('on');
                selectList.slideDown(duration);

                selectItem.on('click', function() {

                    let chooseItem = $(this).data('value');

                    $(`.algorithm option`).attr('selected', false);
                    $(`option[value='${chooseItem}']`).attr('selected', true);

                    selectHead.text( $(this).find('span').text() );

                    selectList.slideUp(duration);
                    selectHead.removeClass('on');

                });

            } else {
                $(this).removeClass('on');
                selectList.slideUp(duration);
            }
        });
    });


    $('.text-delete-btn').on('click', function() {
        $('.text').val('');
        $(this).hide();
    });


    $(document).on("click",".copy-btn",function() {
    var el = '.result-text'
        var $tmp = $("<textarea>");
        $("body").append($tmp);
        $tmp.val($(el).text()).select();
        document.execCommand("copy");
        $tmp.remove();
    })


    function matchWidth() {
        var inputFileWidth = $('.input-file label').outerWidth();
        $('.generate-btn').outerWidth(inputFileWidth);
    }
    matchWidth();
    $(window).on('resize', function() {
        matchWidth();
    });
    $('.input-file input[type=file]').on('change', function(){
        matchWidth();
	});


    function handleAlgorithmChange() {
        var textarea = $('.text');
        var hiddenText = textarea.data('hidden-text');
        var algorithm = $('.algorithm option:selected').val();

        $('.generate-rsa-area, .generate-diffie_hellman-area').hide();
        $('.submit-post').attr('disabled', false);
        textarea.attr("readonly", false).attr('placeholder', 'Текст или файл');

        if (hiddenText) {
            textarea.val(hiddenText);
            textarea.removeData('hidden-text');
        }

        if (algorithm === 'gamming') {
            textarea.attr("readonly", true);
            textarea.data('hidden-text', textarea.val());
            textarea.val('');
            textarea.attr('placeholder', 'Только файл');

        } else if (algorithm === 'RSA') {
            $('.generate-rsa-area').show();
            $('.key').attr("placeholder", "🔑PEM");

        } else if (algorithm === 'Diffie-Hellman') {
            $('.generate-diffie_hellman-area').show();
            $('.submit-post').attr('disabled', true);
            textarea.attr('readonly', true);
            textarea.data('hidden-text', textarea.val());
            textarea.val('');
            textarea.attr('placeholder', 'Только генерация ключа');
        } else {
            $('.key').attr("placeholder", "🔑");
        }
    }

    handleAlgorithmChange();
    $(document).on('click', '.new-select__item', function() {
        setTimeout(handleAlgorithmChange, 225);
    });

});