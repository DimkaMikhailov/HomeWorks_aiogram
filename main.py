from aiogram.utils import executor
from config import dp
from handlers import start, ban, anketa, report, reference
from database.DataBase import DataBase


async def on_startup(_):
    await DataBase().async_create_tables()


start.register_start_handlers(dp)
anketa.register_user_fsm_handlers(dp)
report.register_report_handlers(dp)
reference.register_reference_handlers(dp)
# filter for messages always at the END
ban.register_ban_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
