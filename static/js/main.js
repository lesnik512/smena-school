$(function () {
    var address_info = [];
    $("#id_address").suggestions({
        token: "b6f7b487c9c0ba5220d9c3d31cc26184a5174432",
        type: "ADDRESS",
        count: 5,
        onSelect: function (suggestion) {
            address_info = [
                {
                    'name': 'address_geo_lat',
                    'value': suggestion.data.geo_lat
                },
                {
                    'name': 'address_geo_lon',
                    'value': suggestion.data.geo_lon
                }
            ];
        }
    });

    $('.order_address form').on('submit', function () {
        $('.order_address').slideUp();
        $('.order_time').slideDown();
        return false;
    });

    $('.order_time form').on('submit', function () {
        var $forms = $('.order form');
        var data = $forms.serializeArray();
        if (address_info.length) data = data.concat(address_info);
        $.ajax({
            type: "POST",
            url: $forms.attr('action'),
            data: data,
            dataType: 'json',
            success: function (data) {
                if (data.status) window.location = data.url
            }
        });
        return false
    });

    //lunch amount changing
    $('.lunch__control-cont').on('submit', function (e) {
        var $form = $(this);
        var fdata = $form.serialize();
        var $btn = $form.find("button[type=submit]:focus");
        fdata += '&amount=' + $btn.attr('value');
        $.ajax({
            type: "POST",
            url: $form.attr('action'),
            data: fdata,
            success: function (data) {
                if (data.status) {
                    $form.find('.lunch__control-count').text(data.amount);
                    $('.cart__count').text(data.basket_amount);
                    $('.cart__cost').text(data.basket_sum);
                }
            }
        });
        return false
    });

    //registration
    $('.js-reg-form').on('submit', function (e) {
        var $form = $(this);
        var fdata = $form.serialize();
        var $btn = $form.find("button[type=submit]:focus");
        if ($btn.attr('name') === 'action') {
            fdata += '&' + $btn.attr('name') + '=' + $btn.attr('value');
        }
        $.ajax({
            type: "POST",
            url: $form.attr('action'),
            data: fdata,
            success: function (data) {
                if (data.success) {
                    if (data.is_sms) {
                        $btn.prop('disabled', true);
                    }
                    else {
                        setTimeout(function() {location.reload();}, 2000)
                    }
                }
                $.each(data.messages, function (index, value) {
                    if (value.extra_tags === 'success') {
                        iziToast.success({
                            position: 'bottomCenter',
                            message: value.message
                        });
                    }
                    else {
                        iziToast.warning({
                            position: 'bottomCenter',
                            message: value.message
                        });
                    }
                });
            }
        });
        return false
    });

    //authorization
    $('.js-login-form').on('submit', function (e) {
        var $form = $(this);
        var fdata = $form.serialize();
        $.ajax({
            type: "POST",
            url: $form.attr('action'),
            data: fdata,
            success: function (data) {
                if (data.success) {
                    setTimeout(function() {location.reload();}, 2000)
                }
                $.each(data.messages, function (index, value) {
                    if (value.extra_tags === 'success') {
                        iziToast.success({
                            position: 'bottomCenter',
                            message: value.message
                        });
                    }
                    else {
                        iziToast.warning({
                            position: 'bottomCenter',
                            message: value.message
                        });
                    }
                });
            }
        });
        return false
    });

    //scrolls
    $('a[href*=\\#]').on('click', function(event){
        if (this.hash && $(this.hash).length && !$(this).hasClass('js-noscroll')) {
            jQuery('html,body').animate({scrollTop:jQuery(this.hash).offset().top}, 500);
            return false;
        }
    });

    //phone mask
    $(".input__this-phone").on('focusin', function () {
        $(this).mask("+7(999) 999-9999", {
            completed: function () {
                $(this).parents('.input__cont').addClass('complete');
            }
        });
    });


    //placeholders
    $('.input__this').on('focusin', function () {
        $('.input__cont').removeClass('focused');
        $(this).parents('.input__cont').addClass('focused');
    }).on('focusout', function () {
        $('.input__cont').removeClass('focused');
    }).on('keyup', function () {
        if ($(this).hasClass('input__this-phone')) {}
        else {
            if ($(this).val().length > 0) {
                $(this).parents('.input__cont').addClass('complete');
            }
            else {
                $(this).parents('.input__cont').removeClass('complete');
            }
        }
    });

    //tabs
    $('.form__tab-item').click(function () {
        if ($(this).hasClass('active')) {

        } else {
            var curEl = $(this);
            var clickAttr = $(this).attr('data-tab');
            $('.form__item').each(function () {
                if ($(this).attr('data-tab') == clickAttr) {
                    $('.form__tab-item').removeClass('active');
                    $('.form__item').removeClass('active');
                    $(this).addClass('active');
                    $(curEl).addClass('active');
                }
            })
        }

    });

    //карточка обедов(группировка по 2 обеда для недельного меню)
    $('.weekly__item').each(function () {
        var curLunch = $(this).find('.lunch');
        var cardIndex = 0;
        var stepIndex = 0;
        var lunchNum = 1;
        var endLine = $(curLunch).find('.lunch__item').last().index()
        $(curLunch).find('.lunch__item').each(function () {
            if (stepIndex == endLine) {
                $(this).addClass('look-like');
                $('.look-like').wrapAll("<div class='lunch__group'></div>");
                $('.lunch__item').removeClass('look-like');
            }
            else if (cardIndex < lunchNum) {
                $(this).addClass('look-like');
                cardIndex = cardIndex + 1;
                stepIndex++;
            }
            else {
                cardIndex = 0;
                $(this).addClass('look-like');
                $('.look-like').wrapAll("<div class='lunch__group'></div>");
                $('.lunch__item').removeClass('look-like');
                stepIndex++;
            }
        })
    })
});




