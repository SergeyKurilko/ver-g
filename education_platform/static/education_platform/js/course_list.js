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
    // Таймер для задержки перед отправкой запроса
    let delayTimer;

    // При загрузке страницы заполняем поля формы с примененными фильтрами, если такие есть в url строке
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

        // Восстанавливаем состояние чекбоксов для уровня сложности
        if (urlParams.has('easy_level')) {
            $('#easy_level').prop('checked', true);
        }
        if (urlParams.has('normal_level')) {
            $('#normal_level').prop('checked', true);
        }
        if (urlParams.has('hard_level')) {
            $('#hard_level').prop('checked', true);
        }

        // Восстанавливаем состояние чекбокса для бесплатных курсов
        if (urlParams.has('free')) {
            $('#free_check').prop('checked', true);
        }

        updateActiveFilters()

        // Обновляем ссылки пагинации с текущими фильтрами
        const queryParams = new URLSearchParams($('#filterForm').serialize());
        $('#pagination a').each(function () {
            const pageURL = new URL($(this).attr('href'), window.location.href);
            queryParams.forEach((value, key) => {
                pageURL.searchParams.set(key, value);  // Объединяем параметры фильтрации с пагинацией
            });
            $(this).attr('href', `${pageURL.pathname}?${pageURL.searchParams.toString()}`);
        });
    }

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

        // Добавляем активные фильтры для уровней сложности
        if ($('#easy_level').is(':checked')) {
            filters += `<div class="selected-filter-item mt-1 me-2 mb-2" data-filter="easy_level"><span>Начальный уровень</span><button type="button" class="btn-close ms-1 pt-0"></button></div>`;
        }
        if ($('#normal_level').is(':checked')) {
            filters += `<div class="selected-filter-item mt-1 me-2 mb-2" data-filter="normal_level"><span>Средний уровень</span><button type="button" class="btn-close ms-1 pt-0"></button></div>`;
        }
        if ($('#hard_level').is(':checked')) {
            filters += `<div class="selected-filter-item mt-1 me-2 mb-2" data-filter="hard_level"><span>Высокий уровень</span><button type="button" class="btn-close ms-1 pt-0"></button></div>`;
        }

        // Добавляем активный фильтр для бесплатных курсов
        if ($('#free_check').is(':checked')) {
            filters += `<div class="selected-filter-item mt-1 me-2 mb-2" data-filter="free_check"><span>Бесплатные курсы</span><button type="button" class="btn-close ms-1 pt-0"></button></div>`;
        }

        // Вставляем фильтры в div
        $('.selected-filters-list').html(filters);
    }

    // Функция обновления URL с учетом примененных фильтров
    function updateURLWithFilters() {
        const form = $('#filterForm');
        const url = new URL(window.location.href);
        const formData = form.serializeArray();

        // Обработка текстовых и чиловых инпутов
        formData.forEach(item => {
            if (item.value) {
                url.searchParams.set(item.name, item.value);
            } else {
                url.searchParams.delete(item.name);
            }
        });

        // Отдельная обработка для чекбоксов (независимо от serializeArray)
        form.find('input[type="checkbox"]').each(function () {
            if (this.checked) {
                url.searchParams.set(this.name, 'on');
            } else {
                url.searchParams.delete(this.name);
            }
        });

        // Добавляем текущую страницу в URL, если она есть
        const pageParam = $('#pagination').find('.active').text();
        if (pageParam) {
            url.searchParams.set('page', pageParam);
        }

        history.pushState(null, '', url.toString());
    }

    // Функция обновления списка карточек с курсами
    function updateCourseList(timout) {
        clearTimeout(delayTimer);

        $('.all-course-list-row').fadeOut(100);
        $('.image-loader').fadeIn(300);

        // Явно проверяем состояние чекбоксов и добавляем их в данные запроса
        let form = $('#filterForm');
        let formData = form.serializeArray();

        // Проверка состояния каждого чекбокса перед отправкой данных
        form.find('input[type="checkbox"]').each(function () {
            if (this.checked) {
                formData.push({ name: this.name, value: 'on' });  // Если чекбокс активен, добавляем его в formData
            } else {
                formData.push({ name: this.name, value: '' });  // Если чекбокс не активен, добавляем пустое значение
            }
        });

        delayTimer = setTimeout(function () {
            $.ajax({
                url: form.attr('action'),
                data: $.param(formData),  // Сериализуем данные формы, включая чекбоксы,
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
    $('#filterForm input').on('input change', function () {
        updateCourseList(600);
    });

    // Удаление активного фильтра
    $('.selected-filters-list').on('click', '.btn-close', function () {

        let filterName = $(this).parent().data('filter');  // Получаем название фильтра

        $(`#${filterName}`).prop('checked', false);  // Очищаем значение соответствующего чекбокса, если это чекбокс
        $(`#${filterName}`).val('');  // Очищаем значение для текстовых полей


        // Обновляем список курсов и активные фильтры
        updateCourseList(300);

        // Обновляем URL удаляя отмененные фильтры
        updateURLWithFilters();

        // Обновляем состояние формы и активных фильтров после удаления плашки
        restoreFilterValues();  // Эта функция синхронизирует форму и активные фильтры с URL
    });

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
        updateCourseList(300);
    });

});