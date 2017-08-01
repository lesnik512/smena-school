$(function () {
    var address_info = [];
    $("#id_address").suggestions({
        token: "b6f7b487c9c0ba5220d9c3d31cc26184a5174432",
        type: "ADDRESS",
        count: 5,
        /* Вызывается, когда пользователь выбирает одну из подсказок */
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
            console.log(address_info);
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
            success: function(data) {
                if (data.status) window.location = data.url
            }
        });
        return false
    });

    $('.lunch__control-cont').on('submit', function (e) {
        var $form = $(this);
        var fdata = $form.serialize();
        var $btn = $form.find("button[type=submit]:focus");
        fdata += '&amount=' + $btn.attr('value');
        $.ajax({
           type: "POST",
           url: $form.attr('action'),
           data: fdata,
           success: function(data) {
               if (data.status) {
                   $form.find('.lunch__control-count').text(data.amount);
                   $('.cart__count').text(data.basket_amount);
                   $('.cart__cost').text(data.basket_sum);
               }
           }
        });
        return false
    });
//скроллы

//скролл до меню
    $('.hero__bottom-text').click(function () {
        var scroll_elem = $('.menu');
        $('html, body').animate({scrollTop: $(scroll_elem).offset().top}, 500);
    });

//скролл до форм внизу

    $('.cart').click(function () {
        var scroll_elem = $('.order');
        $('html, body').animate({scrollTop: $(scroll_elem).offset().top}, 500);
    });

    $('.button-login').click(function () {
        var scroll_elem = $('.order');
        $('html, body').animate({scrollTop: $(scroll_elem).offset().top}, 500);
    });

// Маска для телефона
    $(".input__this-phone").on('focus',function () {
        $(this).mask("+7(999) 999-9999", {
            completed: function () {
                $(this).parents('.input__cont').addClass('complete');
            }
        });
    });



//Placeholder - событие по фокусу

    $('.input__this').focus(function () {
        $('.input__cont').removeClass('focused');
        $(this).parents('.input__cont').addClass('focused');
    })

    $('.input__this').focusout(function () {
        $('.input__cont').removeClass('focused');
    })


    $(".input__this").keyup(function () {
            if ($(this).hasClass('input__this-phone')) {

            } else {
                if ($(this).val().length > 0) {
                    $(this).parents('.input__cont').addClass('complete');
                }
                else {
                    $(this).parents('.input__cont').removeClass('complete');
                }
            }

        }
    )

// Переключение табов
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

    })


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

})




