from pathlib import Path

from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram import types

from middleware.user import _get_user_lang


I18N_DOMAIN = 'finance'
BASE_DIR = Path(__file__).parent.parent
LOCALES_DIR = BASE_DIR / 'locales'


async def get_lang(username: str):
    user = await _get_user_lang(username=username)
    if user:
        return user


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action, args):
        user = types.User.get_current()
        return await get_lang(user.username) or user.locale


def setup_middleware(dp):
    i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n
