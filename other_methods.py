from handliers import bot, dp

# --- make a list to string ---
def convert_to_str(text_list):
    s = ''
    for elem in text_list:
        s += elem
    return s

async def delete_message(chat_id, message_id):
    await bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )
