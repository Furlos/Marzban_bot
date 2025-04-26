from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router = Router()


# Заглушка API
class MockAPI:
    @staticmethod
    def authorize(username: str, password: str) -> bool:
        return username == "admin" and password == "admin"


# Состояния
class MarzbanStates(StatesGroup):
    waiting_for_credentials = State()
    waiting_for_action = State()


# Клавиатуры
def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="/registry"))
    builder.add(types.KeyboardButton(text="/help"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def get_actions_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="/user"))
    builder.add(types.KeyboardButton(text="/admin"))
    builder.add(types.KeyboardButton(text="/logout"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


# Обработчики команд
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я управляю Marzban. Для регистрации введите /registry",
        reply_markup=get_main_keyboard(),
    )


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "Доступные команды:\n"
        "/registry - регистрация\n"
        "/user - управление пользователями\n"
        "/admin - управление админами\n"
        "/logout - выход",
        reply_markup=get_main_keyboard(),
    )


@router.message(Command("registry"))
async def cmd_registry(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите имя пользователя и пароль в формате: username password",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.set_state(MarzbanStates.waiting_for_credentials)


@router.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(
            "Нет активных действий для отмены", reply_markup=get_main_keyboard()
        )
        return

    await state.clear()
    await message.answer(
        "Действие отменено. Вы вернулись в главное меню.",
        reply_markup=get_main_keyboard(),
    )


@router.message(MarzbanStates.waiting_for_credentials)
async def process_credentials(message: types.Message, state: FSMContext):
    if message.text.startswith("/"):
        await message.answer(
            "Пожалуйста, введите учетные данные или используйте /cancel для отмены"
        )
        return

    try:
        data = message.text.strip()
        if len(data.split()) != 2:
            raise ValueError

        username, password = data.split()

        if MockAPI.authorize(username, password):
            await message.answer(
                "✅ Авторизация успешна!\nВыберите действие:",
                reply_markup=get_actions_keyboard(),
            )
            await state.set_state(MarzbanStates.waiting_for_action)
        else:
            await message.answer(
                "❌ Неверные учетные данные. Попробуйте еще раз или нажмите /cancel",
                reply_markup=types.ReplyKeyboardRemove(),
            )
    except ValueError:
        await message.answer(
            "⚠️ Неверный формат. Введите имя пользователя и пароль через пробел: username password\n"
            "Или нажмите /cancel для отмены",
            reply_markup=types.ReplyKeyboardRemove(),
        )


@router.message(Command("user"))
async def cmd_user(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state != MarzbanStates.waiting_for_action.state:
        await message.answer("Сначала авторизуйтесь через /registry")
        return

    await message.answer(
        "Управление пользователями (заглушка)", reply_markup=get_actions_keyboard()
    )


@router.message(Command("admin"))
async def cmd_admin(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state != MarzbanStates.waiting_for_action.state:
        await message.answer("Сначала авторизуйтесь через /registry")
        return

    await message.answer(
        "Управление администраторами (заглушка)", reply_markup=get_actions_keyboard()
    )


@router.message(Command("logout"))
async def cmd_logout(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Вы вышли из системы. Для повторной авторизации используйте /registry",
        reply_markup=get_main_keyboard(),
    )
