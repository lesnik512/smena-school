$(function () {

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


// Количество выбранных порций обеда

    $('.round-button').click(function () {
        var curCount = parseInt($(this).parents('.lunch').find('.lunch__control-count').text());
        var countText = $(this).parents('.lunch').find('.lunch__control-count');
        if ($(this).hasClass('minus')) {
            if (curCount == 0) {

            }
            else {
                curCount--;
                $(countText).text(curCount)
            }


        }
        else {
            curCount++;
            $(countText).text(curCount)
        }
    })


// Маска для телефона
    $(".input__this-phone").mask("+7(999) 999-9999", {
        completed: function () {
            $(this).parents('.input__cont').addClass('complete');
        }
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

//История заказов(ссылка  по клику на строке)

    $(".clickable-row").click(function () {
        var curHref= document.location.host
        var goHref='http://' + curHref + $(this).data("href");
        window.location.href = goHref;
    });


//Пагинация
    $('table.paginated').each(function () {
        var currentPage = 0;
        var numPerPage = 10;
        var $table = $(this);
        var countRow = $($table).find('tbody tr').length;
        var countPage = Math.ceil(countRow / numPerPage);
        $($table).parent('div').height($(this).find('tbody tr').height() * numPerPage + $(this).find('thead tr').height())
        $table.bind('repaginate', function () {
            $table.find('tbody tr').hide().slice(currentPage * numPerPage, (currentPage + 1) * numPerPage).show();
        });
        $table.trigger('repaginate');
        var numRows = $table.find('tbody tr').length;
        var numPages = Math.ceil(numRows / numPerPage);
        var $pager = $('<div class="pager">' +
            '<a class="page__control page__first"></a>' +
            '<a class=" page__control page__prev"></a>' +
            '<a class=" page__control page__next"></a>' +
            '<a class=" page__control page__last"></a>' +
            '</div>');
        var $pagerBox = $('<div class="pager__box"></div>').appendTo($pager);
        for (var page = 0; page < numPages; page++) {
            $('<span class="page-number"></span>').text(page + 1).bind('click', {
                newPage: page
            }, function (event) {
                currentPage = event.data['newPage'];
                $table.trigger('repaginate');
                $(this).addClass('active').siblings().removeClass('active');
            }).appendTo($pagerBox).addClass('clickable');
        }
        $pager.insertAfter($($table).parent('div')).find('span.page-number:first').addClass('active');

        $('.page__first').click(function () {
            $('.page-number').removeClass('active');
            $('.page-number:first').addClass('active');
            currentPage = 0;
            $table.trigger('repaginate');
        })

        $('.page__last').click(function () {
            $('.page-number').removeClass('active');
            $('.page-number:last').addClass('active');
            currentPage = countPage - 1;
            $table.trigger('repaginate');
        })

        $('.page__prev').click(function () {
            $('.page-number').removeClass('active');
            currentPage--;
            $('.page-number').eq(currentPage).addClass('active');
            $table.trigger('repaginate');
        })

        $('.page__next').click(function () {
            $('.page-number').removeClass('active');
            currentPage++;
            $('.page-number').eq(currentPage).addClass('active');
            $table.trigger('repaginate');
        })
    });
})




