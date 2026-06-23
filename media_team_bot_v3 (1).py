import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "7855256214:AAHLQH_vMLpQqwFKVT_n4QDowHHvtckLxj4")

DATA = {
    "montage_tips": """
🎬 نصائح المونتاج الأساسية

البرامج الموصى بها:
DaVinci Resolve - مجاني وقوي للاحتراف
CapCut - مثالي للموبايل والريلز
Adobe Premiere Pro - الأكثر استخداماً

قواعد ذهبية:
✅ اقص الفيديو على إيقاع الموسيقى
✅ لا تبالغ في التأثيرات
✅ طبق Color Grading لتوحيد الألوان
✅ الخط يجب ان يقرأ في 3 ثواني
✅ الصوت اهم من الصورة

إعدادات التصدير المثالية:
الدقة: 1080p او 4K
FPS: 25 او 30
Format: MP4 / H.264
Bitrate: 8-15 Mbps
    """,

    "filming_tips": """
📷 نصائح التصوير الاحترافي

الاضاءة:
✅ الضوء الطبيعي = افضل خيار مجاني
✅ لا تصور عكس الشمس
✅ ضع المصدر الضوئي على جانب وجه المتحدث

ضبط الكاميرا:
✅ صور بـ Manual Mode دائما
✅ اضبط White Balance يدويا
✅ Shutter Speed = ضعف الـ FPS
✅ استخدم Tripod للمشاهد الثابتة

التكوين البصري:
✅ قاعدة الاثلاث
✅ اترك مساحة نظر امام الشخص
✅ الخلفية البسيطة = تركيز اكبر

الصوت:
✅ ميكروفون Lapel للمقابلات
✅ تجنب الاماكن ذات الصدى
✅ اختبر الصوت قبل التصوير
    """,

    "logo_tool": """
🖼 طريقة اضافة اللوغو على الفيديو

اداة اونلاين مجانية:
https://vumt.page.gd/

عبر DaVinci Resolve:
1 - اسحب اللوغو PNG الى Timeline فوق الفيديو
2 - في Inspector اضبط Size و Position
3 - اضبط Opacity عند الحاجة
4 - انسخ الكليب على باقي الفيديو

عبر Adobe Premiere:
1 - ضع اللوغو في Track فوق الفيديو
2 - Effect Controls - Scale و Position
3 - اضبط Opacity حسب الرغبة
    """,
}

FONTS = [
    {"name": "Cairo - الاشمل والاكثر استخداما", "desc": "عصري، واضح، مناسب للعناوين والجسم", "url": "https://fonts.google.com/specimen/Cairo"},
    {"name": "Tajawal - مثالي للشاشات", "desc": "هندسي، خفيف، يدعم اوزان متعددة", "url": "https://fonts.google.com/specimen/Tajawal"},
    {"name": "Almarai - انيق ومقروء", "desc": "مصمم خصيصا للاعلام الرقمي العربي", "url": "https://fonts.google.com/specimen/Almarai"},
    {"name": "Noto Kufi Arabic - تراثي وحديث", "desc": "يجمع بين اسلوب الكوفي والوضوح الحديث", "url": "https://fonts.google.com/noto/specimen/Noto+Kufi+Arabic"},
    {"name": "El Messiri - للشعارات والعناوين", "desc": "شخصية بصرية مميزة", "url": "https://fonts.google.com/specimen/El+Messiri"},
    {"name": "Changa - للتايتلات الجريئة", "desc": "عريض وجذاب، مثالي للفيديوهات الديناميكية", "url": "https://fonts.google.com/specimen/Changa"},
    {"name": "Amiri - للمحتوى الاكاديمي", "desc": "نسخي كلاسيكي راق للنصوص الطويلة", "url": "https://fonts.google.com/specimen/Amiri"},
    {"name": "Harmattan - للعروض والتقارير", "desc": "دقيق وواضح للنصوص الرسمية", "url": "https://fonts.google.com/specimen/Harmattan"},
    {"name": "تصفح كل الخطوط العربية", "desc": "مكتبة Google Fonts كاملة", "url": "https://fonts.google.com/?subset=arabic"},
]

SOUNDS = [
    {
        "category": "مكتبات شاملة",
        "items": [
            {"name": "Pixabay Music - الاضخم مجانا", "desc": "الاف المقاطع بدون حقوق، تحميل مباشر MP3", "url": "https://pixabay.com/music/"},
            {"name": "Mixkit - موسيقى احترافية مجانية", "desc": "مقاطع سينمائية وتحفيزية، بدون ذكر مصدر", "url": "https://mixkit.co/free-stock-music/"},
            {"name": "YouTube Audio Library", "desc": "مكتبة يوتيوب الرسمية - آمنة 100%", "url": "https://studio.youtube.com/channel/UC/music"},
        ]
    },
    {
        "category": "موسيقى سينمائية وتحفيزية",
        "items": [
            {"name": "Bensound - للفيديوهات المؤثرة", "desc": "موسيقى سينمائية وتحفيزية مجانية مع ذكر المصدر", "url": "https://www.bensound.com/free-music-for-videos"},
            {"name": "Chosic - تصنيف حسب المزاج", "desc": "ابحث حسب الموود: هادئ، حماسي، حزين...", "url": "https://www.chosic.com/free-music/all/"},
        ]
    },
    {
        "category": "مؤثرات صوتية SFX",
        "items": [
            {"name": "Freesound.org - اكبر مكتبة مؤثرات", "desc": "مجتمع ضخم - مؤثرات لكل موقف", "url": "https://freesound.org"},
            {"name": "ZapSplat - مؤثرات احترافية", "desc": "تسجيل مجاني للوصول لالاف المؤثرات", "url": "https://www.zapsplat.com"},
            {"name": "Mixkit SFX - مؤثرات فورية", "desc": "بدون تسجيل، تحميل فوري", "url": "https://mixkit.co/free-sound-effects/"},
        ]
    },
    {
        "category": "قنوات يوتيوب للموسيقى المجانية",
        "items": [
            {"name": "RFM NCM Royalty Free Music", "desc": "مقاطع مصنفة حسب الموود، آمنة للنشر", "url": "https://www.youtube.com/@RFMNCMRoyaltyFreeMusic"},
            {"name": "Vlog No Copyright Music", "desc": "موسيقى للمحتوى العربي والعالمي", "url": "https://www.youtube.com/@VlogNoCopyrightMusic"},
        ]
    },
]

LOGOS = [
    {"name": "لوغو جامعة دمشق", "file_id": "BQACAgQAAxkBAAMGajp3qnFvgCv7oWKBNXIDphKLEeIAAoMcAALaR9FRGgf0mrzW7xE8BA"},
    {"name": "لوغو الفريق الاعلامي", "file_id": "BQACAgQAAxkBAAMWajp8llvUlFtvRDFcF6MyLAt2bogAAogcAALaR9FR86A6JTV-kHs8BA"},
]


def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎬 نصائح المونتاج", callback_data="montage")],
        [InlineKeyboardButton("📷 نصائح التصوير", callback_data="filming")],
        [InlineKeyboardButton("🎨 اللوغوهات", callback_data="logos")],
        [InlineKeyboardButton("✏️ مكتبة الخطوط", callback_data="fonts_main")],
        [InlineKeyboardButton("🎵 مكتبة الأصوات", callback_data="sounds_main")],
        [InlineKeyboardButton("🖼️ كيفية إضافة اللوغو", callback_data="logo_tool")],
    ]
    return InlineKeyboardMarkup(keyboard)

def back_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = "أهلاً " + user.first_name + "!\n\nبوت الفريق الإعلامي الجامعي\nاختر ما تحتاجه من القائمة:"
    await update.message.reply_text(msg, reply_markup=main_keyboard())


async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    if update.message.document:
        fid = update.message.document.file_id
        await update.message.reply_text("file_id: " + fid)
    elif update.message.photo:
        fid = update.message.photo[-1].file_id
        await update.message.reply_text("file_id: " + fid)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main_menu":
        await query.edit_message_text("بوت الفريق الإعلامي الجامعي\nاختر ما تحتاجه:", reply_markup=main_keyboard())

    elif data == "montage":
        await query.edit_message_text(DATA["montage_tips"], reply_markup=back_keyboard())

    elif data == "filming":
        await query.edit_message_text(DATA["filming_tips"], reply_markup=back_keyboard())

    elif data == "logo_tool":
        await query.edit_message_text(DATA["logo_tool"], reply_markup=back_keyboard())

    elif data == "logos":
        keyboard = []
        for i, logo in enumerate(LOGOS):
            keyboard.append([InlineKeyboardButton(logo["name"], callback_data="logo_" + str(i))])
        keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
        await query.edit_message_text("اللوغوهات\n\nاختر اللوغو:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("logo_"):
        idx = int(data.split("_")[1])
        logo = LOGOS[idx]
        await query.message.reply_document(document=logo["file_id"], caption=logo["name"])

    elif data == "fonts_main":
        keyboard = []
        for i, font in enumerate(FONTS):
            keyboard.append([InlineKeyboardButton(font["name"], callback_data="font_" + str(i))])
        keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
        await query.edit_message_text("مكتبة الخطوط العربية\n\nاختر الخط:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("font_"):
        idx = int(data.split("_")[1])
        font = FONTS[idx]
        text = font["name"] + "\n\n" + font["desc"] + "\n\nالرابط: " + font["url"]
        keyboard = [
            [InlineKeyboardButton("⬅️ العودة للخطوط", callback_data="fonts_main")],
            [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")],
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "sounds_main":
        keyboard = []
        for i, cat in enumerate(SOUNDS):
            keyboard.append([InlineKeyboardButton(cat["category"], callback_data="sound_cat_" + str(i))])
        keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
        await query.edit_message_text("مكتبة الأصوات والموسيقى\n\nاختر التصنيف:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("sound_cat_"):
        cat_idx = int(data.split("_")[2])
        cat = SOUNDS[cat_idx]
        keyboard = []
        for j, item in enumerate(cat["items"]):
            keyboard.append([InlineKeyboardButton(item["name"], callback_data="sound_" + str(cat_idx) + "_" + str(j))])
        keyboard.append([InlineKeyboardButton("⬅️ العودة للأصوات", callback_data="sounds_main")])
        keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
        await query.edit_message_text(cat["category"] + "\n\nاختر المصدر:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("sound_"):
        parts = data.split("_")
        cat_idx = int(parts[1])
        item_idx = int(parts[2])
        item = SOUNDS[cat_idx]["items"][item_idx]
        text = item["name"] + "\n\n" + item["desc"] + "\n\nالرابط: " + item["url"]
        keyboard = [
            [InlineKeyboardButton("⬅️ العودة للتصنيف", callback_data="sound_cat_" + str(cat_idx))],
            [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")],
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(MessageHandler(filters.ALL, get_file_id))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("البوت يعمل...")
    app.run_polling()


if __name__ == "__main__":
    main()
