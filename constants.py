URL_OZON_FBS = "https://api-seller.ozon.ru/v3/posting/fbs/list"

URL_OZON_FBO = "https://api-seller.ozon.ru/v2/posting/fbo/list"

LIMIT = 1000

OFFSET = 0

DATEPARSER_SETTINGS = {'DATE_ORDER': 'YMD'}

FOREIGN_COUNTRIES_SHIPMENT = {
    'Армения': {'Армения'},
    'Беларусь': {'Брест', 'Витебск', 'Гомель', 'Гродно', 'Минск', 'Могилев', 'Беларусь', 'Брестская', 'Витебская', 'Гомельская', 'Гродненская', 'Минская', 'Могилевская',},
    'Киргизия': {'Киргизия', 'Кыргызстан'},
    'Казахстан': {'Актау', 'Актобе', 'Алма-Ата', 'Алматы', 'Астана', 'Атырау', 'Караганда', 'Караганды',
                  'Костанай', 'Кызылорда', 'Павлодар', 'Петропавловск', 'Петропавл', 'Тараз',
                  'Туркестан', 'Уральск', 'Орал', 'Усть-Каменогорск', 'Казахстан'},
}

STATUS_CATALOGUE = {
    'awaiting_registration': 'Ожидает регистрации',
    'acceptance_in_progress': 'Идёт приёмка',
    'awaiting_approve': 'Ожидает подтверждения',
    'awaiting_packaging': 'Ожидает упаковки',
    'awaiting_deliver': 'Ожидает отгрузки',
    'arbitration': 'Арбитраж',
    'client_arbitration': 'Клиентский арбитраж доставки',
    'delivering': 'Доставляется',
    'driver_pickup': 'У водителя',
    'delivered': 'Доставлено',
    'cancelled': 'Отменено',
    'not_accepted': 'Не принято на сортировочном центре',
    'sent_by_seller': 'Отправлено продавцом',
}

LIST_ERROR_CURRENCY = {
    101: 'Ошибка ключа доступа. Ведите корректый ключ.',
    102: 'Учетная запись пользователя не активна. Необходимо связаться со службой поддержки.',
    103: 'Пользователь запросил несуществующую функцию API.',
    104: 'Достигнут или превышен месячный лимит API-запросов, установленный для тарифного плана.',
    105: 'Текущий абонентский план пользователя не поддерживает запрашиваемую функцию API.',
    106: 'Запрос пользователя не дал никаких результатов',
    201: 'Указана недопустимая валюта конвертации.',
    202: 'Пользователь ввел один или несколько недопустимых кодов валют.',
    301: 'Пользователь не указал дату.',
    302: 'Пользователь ввел недопустимую дату.',
    404: 'Пользователь запросил несуществующий ресурс.',
    700: 'Ошибка получения данных валюты. Обратитесь в службу поддержки бота.',
    800: 'Ошибка получения валюты. Обратитесь в службу поддержки бота.',
    808: 'Ошибка подключения к базе данных. Попробуйте повторить запрос позже.',
}

NAME_FILE_WITH_ERROR = 'error.txt'

LOCATE_FILE_WITH_ERROR = f'C:\project\Ozon_EAEU_script\{NAME_FILE_WITH_ERROR}'
