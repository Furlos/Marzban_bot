import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("API_URL")
class MarzbanStates(StatesGroup):
    waiting_for_data = State()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я управляю Marzban. Введите имя и пароль админа (В виде username password):"
    )
@dp.message(F.text)
async def process_direct_url(message: types.Message, state: FSMContext):
    data = message.text.strip()