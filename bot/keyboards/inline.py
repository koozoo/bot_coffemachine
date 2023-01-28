from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

close = InlineKeyboardButton(text="❌", callback_data='BACK_CLOSE')


def service_auth(access, data: dict, user_access=None):
    kb = InlineKeyboardMarkup(row_width=2)
    match access:
        case '1':
            for k, v in data['all_ltd'].items():
                btn = InlineKeyboardButton(text=f'{v["title"]}',
                                           callback_data=f'NAV_LTD_{data["company_id"]}:{v["ltd_id"]}')
                kb.add(btn)
            kb.row(close)

        case '2':
            if user_access is not None:
                for k, v in data['all_address'].items():
                    btn = InlineKeyboardButton(text=f'{v["title"]}',
                                               callback_data=f'NAV_ADDRESS_{data["company_id"]}:{data["ltd_id"]}:{v["address_id"]}')
                    kb.add(btn)
                back = InlineKeyboardButton(text='⤴️', callback_data=f"BACK_BACK_{data['company_id']}")
                kb.row(back, close)
            else:
                for k, v in data['all_address'].items():
                    btn = InlineKeyboardButton(text=f'{v["title"]}',
                                               callback_data=f'NAV_ADDRESS_{data["company_id"]}:{data["ltd_id"]}:{v["address_id"]}')
                    kb.add(btn)
                kb.row(close)

        case '3':
            if user_access is not None:
                for k, v in data['all_device'].items():
                    btn = InlineKeyboardButton(text=f'{v["model"]}', callback_data=f'NAV_DEVICE_{data["company_id"]}:'
                                                                                   f'{data["ltd_id"]}:{data["address_id"]}:{v["device_id"]}')
                    kb.add(btn)
                back = InlineKeyboardButton(text='⤴️', callback_data=f"BACK_BACK_{data['company_id']}:{data['ltd_id']}")
                kb.row(back, close)
            else:
                for k, v in data['all_device'].items():
                    btn = InlineKeyboardButton(text=f'{v["model"]}', callback_data=f'NAV_DEVICE_{data["company_id"]}:'
                                                                                   f'{data["ltd_id"]}:{data["address_id"]}:{v["device_id"]}')
                    kb.add(btn)
                kb.row(close)

    return kb


def view_navigate_menu(data: dict, back_link: str = None):

    kb = InlineKeyboardMarkup(row_width=2)

    ltd = data.get('all_ltd')
    address = data.get('all_address')
    device = data.get('all_device')

    kb_data: dict

    if ltd is not None:
        kb_data = ltd
        flag = 1
    elif address is not None:
        kb_data = address
        flag = 2
    elif device is not None:
        kb_data = device
        flag = 3
    else:
        kb_data = {
            "Создать заявку": "CREATE_TASK"
        }
        flag = 4
    print("LEN dta", len(kb_data))
    for k, v in kb_data.items():

        match flag:

            case 1:
                btn = InlineKeyboardButton(text=f"{v['title']}", callback_data=f'NAV_LTD_{data["company_id"]}:'
                                                                               f'{v["ltd_id"]}')
                kb.add(btn)
            case 2:
                btn = InlineKeyboardButton(text=f"{v['title']}", callback_data=f'NAV_ADDRESS_{data["company_id"]}:'
                                                                               f'{data["ltd_id"]}:'
                                                                               f'{v["address_id"]}')
                kb.add(btn)
            case 3:
                btn = InlineKeyboardButton(text=f"{v['model']}", callback_data=f'NAV_DEVICE_{data["company_id"]}:'
                                                                               f'{data["ltd_id"]}:'
                                                                               f'{data["address_id"]}:'
                                                                               f'{v["device_id"]}')
                kb.add(btn)
            case 4:
                btn = InlineKeyboardButton(text=f"{k}", callback_data=f"{v}")
                kb.add(btn)

    if back_link:
        back_btn = InlineKeyboardButton(text="⤴️", callback_data=f"BACK_BACK_{back_link}")
        kb.row(back_btn, close)
    else:
        kb.row(close)

    return kb
