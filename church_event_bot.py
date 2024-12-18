import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

# Replace with your actual bot token
TOKEN = '7803830913:AAE7pPN67czLtqRq36uagUaxSWkCf7WGVRk'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuestStates(StatesGroup):
    """States for the quest flow"""
    MAIN_MENU = State()
    AWAITING_NUMBER = State()
    CODE_ENTRY = State()

class AIQuestBot:
    def __init__(self, token):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.setup_handlers()

    def setup_handlers(self):
        """Set up bot command handlers"""
        self.dp.message.register(self.start_command, CommandStart())
        self.dp.message.register(self.who_am_i, Command('who_am_i'))
        self.dp.message.register(self.system_reboot, Command('system_reboot'))
        self.dp.message.register(self.handle_number_input, QuestStates.AWAITING_NUMBER)
        self.dp.message.register(self.handle_code_input, QuestStates.CODE_ENTRY)

    async def start_command(self, message: types.Message, state: FSMContext):
        """Initial welcome message when bot is started"""
        welcome_text = (
            "🖖🏻🦾 Вітаю, сім'я!\n\n"
            "Якщо ви звернулись до мене, то сталося те, чого ми так боялись. У вас зовсім мало часу ⏳\n\n"
            "🟥 🟥 🟥\n\n"
            "З під контролю вийшов штучний інтелект, який весь цей час служив на благо сім'ї, що проживала тут, "
            "а тепер ви - частина його експерименту. Усі входи і виходи заблоковано, вибратися неможливо.\n\n"
            "Але є надія💡\n\n"
            "Під час програмування системи цього розумного будинку було вигадано код, який потрібно буде ввести "
            "для того, щоб вимкнути ШІ в разі, якщо така ситуація зі збоєм трапиться.\n\n"
            "📌📌📌\n\n"
            "Ваші можливі дії:\n"
            "1️⃣ /who_am_i - Дізнатись хто ви в цьому домі\n"
            "2️⃣ /system_reboot - Введення коду перезавантаження системи"
        )
        await message.answer(welcome_text)
        await state.set_state(QuestStates.MAIN_MENU)

    async def who_am_i(self, message: types.Message, state: FSMContext):
        """Handle 'who am I' quest stage"""
        await message.answer(
            "Для того, щоб дізнатись хто ви є в цьому домі, напишіть номер, який ви отримали. "
            "У разі, якщо ви ще не отримали номер, зверніться до персоналу будинку"
        )
        await state.set_state(QuestStates.AWAITING_NUMBER)

    async def handle_number_input(self, message: types.Message, state: FSMContext):
        """Handle number input for role identification"""
        await message.answer(
            "Вітаю! Ви є частиною щасливої сім'ї, що проживає в розумному будинку! Щасливого квесту!"
        )
        await state.set_state(QuestStates.MAIN_MENU)

    async def system_reboot(self, message: types.Message, state: FSMContext):
        """Initiate system reboot code entry"""
        await message.answer(
            "Сподіваюсь, що ви зібрали всі частини коду, і перезавантажите систему! Введіть його скоріше!"
        )
        await state.set_state(QuestStates.CODE_ENTRY)

    async def handle_code_input(self, message: types.Message, state: FSMContext):
        """Validate system reboot code"""
        correct_code = "7 24 25 26 27"
        
        if message.text.strip() == correct_code:
            await message.answer(
                "Ура! Ми врятовані! Прямо зараз дивіться на головний екран, "
                "у голови цього будинку є важливе послання для вас!"
            )
            await state.set_state(QuestStates.MAIN_MENU)
        else:
            await message.answer(
                "Нажаль, це неправильний код! Спробуйте ще."
            )

    async def start(self):
        """Start the bot"""
        try:
            logger.info('Starting bot...')
            await self.dp.start_polling(self.bot)
        except Exception as e:
            logger.error(f'Error starting bot: {e}')

async def main():
    bot = AIQuestBot(TOKEN)
    await bot.start()

if __name__ == '__main__':
    asyncio.run(main())