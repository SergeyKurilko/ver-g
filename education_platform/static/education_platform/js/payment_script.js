$(document).ready(function () {
    // Скрипт загружается вместе со страницей подтверждения платежа

    // Если, при загузке страницы платеж уже подтвержден
    if (payment_confirmed === 'True') {
        $('.payment-confirmed-container').removeClass('d-none')


    // Если платеж еще не подтвержден, то делаем запросы в yookassa 
    // для подтверждения платежа
    } else if (payment_confirmed === 'False') {
        $('.payment-not-confirmed').removeClass('d-none')

        let checkCounter = 0

        // Функция для ajax запроса к check_payment_status view
        function check_payment_status() {
            $.ajax({
                type: "GET",
                url: check_payment_url,
                dataType: "json",
                success: function (response) {
                    if (response.status === 'succeeded') {
                        window.location.reload();
                    } else {

                        // Вызывает саму себя, пока checkCounter < 5
                        if (checkCounter < 5) {
                            checkCounter += 1
                            setTimeout(check_payment_status, 2000);

                        } else {
                            var paymentErrorHtml = `
                            <div class="container-fluid container-md text-center payment-not-confirmed">
                            <h4 style="font-weight: 100; line-height: 2rem;">
                            Ошибка оплаты. Если вы уверенны, что оплата завершена, или есть другие вопросы, 
                            то напишите нам на <a href="mailto:help@ver-g.ru">help@ver-g.ru</a>
                            </h4>
                            <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-exclamation-square-fill" viewBox="0 0 16 16">
                            <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2zm6 4c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995A.905.905 0 0 1 8 4m.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2"/>
                            </svg>
                            </div>
                            `
                            $('.payment-confirm').html(paymentErrorHtml)
                        }
                    }
                }
            });
        }

        // Первый вызов функции для запуска цикла запросов
        check_payment_status()
    }
});