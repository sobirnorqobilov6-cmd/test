import asyncio
import logging
import wikipedia
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import text
import os

# Bot sozlamalari
API_TOKEN = '8718708660:AAHdfBcBWQnOZ8YjO0c7aBG5FRVaA-clk9k'  # BotFather dan olingan tokenni qo'ying
wikipedia.set_lang('uz')  # O'zbek tilidagi Wikipedia (agar bo'lmasa, 'ru' yoki 'en' ishlatishingiz mumkin)

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)

# Bot va dispatcher yaratish
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Start komandasi
@dp.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text = text(
        "👋 Salom! Men Wikipedia qidiruv botiman.\n",
        f"Xush kelibsiz, {message.from_user.full_name}!\n\n",
        "📝 Menga istalgan mavzuni yozing, men Wikipedia'dan qidirib beraman.\n",
        "Misol: 'Oʻzbekiston', 'Toshkent', 'Amir Temur'\n\n",
        "🔍 Qidiruv tili: O'zbekcha (agar topilmasa, Inglizcha)",
        sep=""
    )
    await message.answer(welcome_text)

# Yordam komandasi
@dp.message(Command("help"))
async def cmd_help(message: Message):
    help_text = text(
        "🔍 **Qanday ishlaydi?**\n",
        "• Menga istalgan mavzuni yozing\n",
        "• Men Wikipedia'dan qisqacha ma'lumot topaman\n",
        "• Agar maqola topilsa, sizga yuboraman\n",
        "• Agar topilmasa, boshqa so'z bilan urinib ko'ring\n\n",
        "🌐 **Til sozlamalari:**\n",
        "/lang_uz - O'zbek tili\n",
        "/lang_ru - Rus tili\n",
        "/lang_en - Ingliz tili\n\n",
        "💡 **Maslahat:** Aniqroq mavzularni yozing",
        sep="\n"
    )
    await message.answer(help_text, parse_mode="Markdown")

# Tilni o'zbekcha qilish
@dp.message(Command("lang_uz"))
async def set_lang_uz(message: Message):
    wikipedia.set_lang('uz')
    await message.answer("✅ Qidiruv tili: O'zbekcha")

# Tilni ruscha qilish
@dp.message(Command("lang_ru"))
async def set_lang_ru(message: Message):
    wikipedia.set_lang('ru')
    await message.answer("✅ Qidiruv tili: Ruscha")

# Tilni inglizcha qilish
@dp.message(Command("lang_en"))
async def set_lang_en(message: Message):
    wikipedia.set_lang('en')
    await message.answer("✅ Qidiruv tili: Inglizcha")

# Asosiy qidiruv funksiyasi
@dp.message()
async def search_wikipedia(message: Message):
    search_query = message.text.strip()
    
    # Qidiruv boshlanganini bildirish
    wait_msg = await message.answer(f"🔍 '{search_query}' bo'yicha qidiryapman...")
    
    try:
        # Wikipedia'dan qidirish
        summary = wikipedia.summary(search_query, sentences=5, auto_suggest=False)
        
        # Maqola sarlavhasini olish
        page = wikipedia.page(search_query, auto_suggest=False)
        title = page.title
        
        # Maqola havolasi
        url = page.url
        
        # Natijani formatlash
        result_text = text(
            f"📚 **{title}**\n\n",
            f"{summary}\n\n",
            f"🔗 [Wikipedia'da o'qish]({url})",
            sep=""
        )
        
        # Natijani yuborish
        await wait_msg.delete()  # "Qidiryapman" xabarini o'chirish
        await message.answer(result_text, parse_mode="Markdown", disable_web_page_preview=True)
        
    except wikipedia.exceptions.PageError:
        await wait_msg.delete()
        await message.answer(f"❌ Kechirasiz, '{search_query}' mavzusida maqola topilmadi.\n\nBoshqa so'z bilan urinib ko'ring yoki /lang_en orqali ingliz tilida qidiring.")
        
    except wikipedia.exceptions.DisambiguationError as e:
        await wait_msg.delete()
        # Agar bir nechta maqola topilsa
        options = e.options[:10]  # Birinchi 10 ta variant
        options_text = "\n".join([f"• {opt}" for opt in options])
        await message.answer(f"📌 '{search_query}' bir nechta ma'noga ega. Aniqroq mavzu yozing:\n\n{options_text}\n\nMasalan: '{options[0]}'")
        
    except wikipedia.exceptions.WikipediaException as e:
        await wait_msg.delete()
        await message.answer(f"⚠️ Wikipedia bilan bog'liq xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

# Botni ishga tushirish
async def main():
    print("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())