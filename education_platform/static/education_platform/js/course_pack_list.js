$(document).ready(function () {
    // Функция для отслеживания высоты прокрутки, чтобы отобразить кнопку "вверх"
    function handleScroll() {
        const crollY = window.scrollY;
        const buttonUpToStartPage = $('#buttonMoveToStartPage');

        if (scrollY > 700) {
            $(buttonUpToStartPage).fadeIn(300);
        } else {
            $(buttonUpToStartPage).fadeOut(300);
        }
    }

    // Отслеживание прокрутки и запуск функции handleScroll
    window.addEventListener('scroll', handleScroll);

    // Отслеживание нажатия кнопки "вверх"
    $("#buttonMoveToStartPage").click(function (e) {
        window.scrollTo({
            top: 0,
            left: 0,
            behavior: 'smooth'
        });
    });


    // Отслеживание кнопки compactFiltersMenuButton для открытия меню фильтров в windh < 756px
    $('#compactFiltersMenuButton').click(function (e) {
        var filtersсCol = $('.filters-сol')
        var filterFilters = $('.filters-сol .filters')

        filtersсCol.removeClass('d-none');
        filtersсCol.addClass('filters-сol-open-with-compact');
        filterFilters.addClass('container');

    });

    // Отслеживание закрытия компактного меню фильтров
    $('#applyCompactFiltersButton').click(function (e) {
        $('.filters-сol').addClass('d-none');
        $('.filters-сol').removeClass('filters-сol-open-with-compact');
        $('.filters-сol .filters').removeClass('container')
    });

    // Отслеживание закрытия компактного меню фильтров кнопкой btn-close
    $('.compact-filter-menu-close .btn-close').click(function (e) {
        $('.filters-сol').addClass('d-none');
        $('.filters-сol').removeClass('filters-сol-open-with-compact');
        $('.filters-сol .filters').removeClass('container')
    });

    /* ------------------------- Filters -------------------------- */
    // Заполняем поля формы с примененными фильтрами, если такие есть в url строке
    restoreFilterValues()

    // Функция обновления полей форм, если в URL строке есть какте-то параметры фильтрации
    function restoreFilterValues() {
        const urlParams = new URLSearchParams(window.location.search);

        // Восстанавливаем значение поля "Цена от"
        if (urlParams.has('price_from')) {
            $('#price_from').val(urlParams.get('price_from'));
        }

        // Восстанавливаем значение поля "Цена до"
        if (urlParams.has('price_to')) {
            $('#price_to').val(urlParams.get('price_to'));
        }
    }


    // Таймер для задержки перед отправкой запроса
    let delayTimer;

    // Функция обновления активных фильтров
    function updateActiveFilters() {
        let filters = '';

        let priceFrom = $('#price_from').val();
        let priceTo = $('#price_to').val();

        // Добавляем активные фильтры в виде плашек
        if (priceFrom) {
            filters += `<div class="selected-filter-item mt-1 me-2 mb-2" data-filter="price_from"><span>от: ${priceFrom}</span><button type="button" class="btn-close ms-1 pt-0"></button></div>`;
        }
        if (priceTo) {
            filters += `<div class="selected-filter-item mt-1 me-2 mb-2" data-filter="price_to"><span>до: ${priceTo}</span><button type="button" class="btn-close ms-1 pt-0"></button></div>`;
        }

        // Вставляем фильтры в div
        $('.selected-filters-list').html(filters);
    }

    // Функция обновления URL с учетом примененных фильтров
    function updateURLWithFilters() {
        const form = $('#filterForm');
        const url = new URL(window.location.href);
        const formData = form.serializeArray();

        formData.forEach(item => {
            if (item.value) {
                url.searchParams.set(item.name, item.value);
            } else {
                url.searchParams.delete(item.name);
            }
        });

        // Добавляем текущую страницу в URL, если она есть
        const pageParam = $('#pagination').find('.active').text();  // Текущая страница из пагинации
        if (pageParam) {
            url.searchParams.set('page', pageParam);
        }

        history.pushState(null, '', url.toString());
    }

    // Функция обновления списка карточек с пакетами курсов
    function updateCoursePackList(timout) {
        clearTimeout(delayTimer);

        $('.all-course-list-row').fadeOut(100);
        $('.image-loader').fadeIn(300);

        delayTimer = setTimeout(function () {
            $.ajax({
                url: $('#filterForm').attr('action'),
                data: $('#filterForm').serialize(),
                success: function (data) {
                    $('.all-course-list-row').html($(data).find('.all-course-list-row').html());
                    $('#pagination').html($(data).find('#pagination').html());

                    // Обновляем активированные фильры (плашки)
                    updateActiveFilters()

                    // Обновляем URL с примененными фильтрами
                    updateURLWithFilters()

                    // Обновляем ссылки пагинации с текущими фильтрами
                    const queryParams = new URLSearchParams($('#filterForm').serialize());
                    $('#pagination a').each(function () {
                        const pageURL = new URL($(this).attr('href'), window.location.href);
                        queryParams.forEach((value, key) => {
                            pageURL.searchParams.set(key, value);  // Объединяем параметры фильтрации с пагинацией
                        });
                        $(this).attr('href', `${pageURL.pathname}?${pageURL.searchParams.toString()}`);
                    });
                },
                complete: function () {
                    $('.all-course-list-row').fadeIn(300)
                    $('.image-loader').fadeOut(100)
                }
            });
        }, timout)
    }

    // Отслеживаем изменения в форме с фильтрами
    $('#filterForm input').on('input', function () {
        updateCoursePackList(1000);
    })

    // Удаление активного фильтра
    $('.selected-filters-list').on('click', '.btn-close', function () {
        let filterName = $(this).parent().data('filter');  // Получаем название фильтра
        $(`#${filterName}`).val('');  // Очищаем значение соответствующего поля

        // Обновляем список курсов и активные фильтры
        updateCoursePackList(300);
    });

    // Инициализация при загрузке страницы
    updateActiveFilters()

    // Логика сброса фильтров
    // Используем document, так как одна из кнопок resetFiltersButton рендерится динамически
    $(document).on('click', '.resetFiltersButton', function () {

        // Очищаем все поля формы
        $('#filterForm').trigger('reset');

        // Удаляем параметры фильтров из URL
        const url = new URL(window.location.href);
        url.searchParams.delete('price_from');
        url.searchParams.delete('price_to');
        url.searchParams.delete('easy_level');
        url.searchParams.delete('normal_level');
        url.searchParams.delete('hard_level');
        url.searchParams.delete('free');
        url.searchParams.delete('page');  // Удаляем параметр пагинации, если есть

        // Обновляем URL без фильтров
        history.pushState(null, '', url.toString());

        // Обновляем список курсов без фильтров
        updateCoursePackList(300);
    });

    // Инициализация при загрузке страницы
    updateActiveFilters()

    // Логика сброса фильтров
    $('#resetFiltersButton').click(function () {
        // Очищаем все поля формы
        $('#filterForm').trigger('reset');

        // Удаляем параметры фильтров из URL
        const url = new URL(window.location.href);
        url.searchParams.delete('price_from');
        url.searchParams.delete('price_to');
        url.searchParams.delete('page');  // Удаляем параметр пагинации, если есть

        // Обновляем URL без фильтров
        history.pushState(null, '', url.toString());

        // Обновляем список курсов без фильтров
        updateCoursePackList(300);
    });
});