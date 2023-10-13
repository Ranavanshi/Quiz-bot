from pyrogram import filters

# Custom filter for checking if the user is the owner
is_owner = filters.create(lambda _, __, message: message.from_user.id == OWNER_ID)
