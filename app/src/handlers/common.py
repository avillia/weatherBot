from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from app.common.models import User
from app.common.services.weather import obtain_weather
from app.common.services.timezone import fetch_timezone
from app.configs.extensions import Session
from app.src.fsm import UserState
from app.src.ui import location_keyboard, default_keyboard


async def cmd_start(message: Message, state: FSMContext):
    await state.finish()
    with Session() as session:
        with session.begin():
            if user := session.query(User).get(message.from_user.id):
                session.delete(user)
            user = User(id=message.from_user.id)
            session.add(user)
    await UserState.first_geolocation_request.set()
    await message.reply(
        "Hello there!\n"
        "I'm bot that can send you information about weather in your place!"
        "Just send me your location via button under text field:",
        reply_markup=location_keyboard,
    )


async def not_a_location(message: Message):
    await message.reply(
        "Please, send me your location with button bellow:"
    )


async def cmd_cancel(message: Message):
    await UserState.forecasting.set()
    await message.reply(
        "Action cancelled. Something else?",
        reply_markup=default_keyboard
    )