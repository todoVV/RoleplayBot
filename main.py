import discord
from discord import app_commands
from dotenv import load_dotenv
import datetime
import os
import random
import pickle

#####################################################
##                                                 ##
##                PROGRAM INNARDS                  ##
##                                                 ##
#####################################################

#region Innards
#region Classes
#region Item
class Item:
    def __init__(self, name: str, weight: float, wearable: bool, desc: str = ''):
        self.name = name
        self.weight = weight
        self.wearable = wearable
        self.desc = desc
    
    def get_name(self):
        return self.name
    
    def get_desc(self):
        return self.desc
    
    def get_wearable_state(self):
        return self.wearable
    
    def get_weight(self):
        return self.weight
    
    def edit_name(self, name: str):
        self.name = name
        return
    
    def edit_desc(self, desc: str):
        self.desc = desc
        return
    
    def edit_weight(self, weight: float):
        self.weight = weight
        return
    
    def switch_wearable_state(self, wearable: bool):
        self.wearable = wearable
        return

#endregion
#region Object
class Object:
    def __init__(self, name: str, isContainer: bool, isLocked: bool, keyName: str = '', storage: int = -1, desc: str = ''):
        self.name = name
        self.desc = desc
        self.isContainer = isContainer
        self.isLocked = isLocked
        self.keyName = keyName
        self.storage = storage
        self.objItems = []

    def get_name(self):
        return self.name
    
    def get_desc(self):
        return self.desc

    def get_items(self):
        return self.objItems

    def get_locked_state(self):
        return self.isLocked
    
    def get_container_state(self):
        return self.isContainer

    def get_key_name(self):
        return self.keyName
    
    def get_storage(self):
        return self.storage

    def switch_locked_state(self, locked: bool):
        self.isLocked = locked
        return

    def switch_container_state(self, container: bool):
        self.isContainer = container
        return

    def add_item(self, item: Item):
        self.objItems.append(item)
        return

    def edit_name(self, name: str):
        self.name = name
        return

    def edit_item(self, origItem: Item, item: Item):
        self.objItems[origItem] = item
        return

    def edit_key_name(self, keyName: str):
        self.keyName = keyName
        return

    def edit_desc(self, desc: str):
        self.desc = desc
        return
    
    def set_storage(self, newStorageAmt: int):
        self.storage = newStorageAmt
        return

    def del_item(self, item: Item):
        self.objItems.remove(item)
        return
#endregion
#region Exit
class Exit:
    def __init__(self, room1: str, room2: str, isLocked: bool, keyName: str = ''):
        self.room1 = room1
        self.room2 = room2
        self.isLocked = isLocked
        self.keyName = keyName

    def get_room1(self):
        return self.room1
    
    def get_room2(self):
        return self.room2
    
    def get_locked_state(self):
        return self.isLocked

    def get_key_name(self):
        return self.keyName

    def edit_room1(self, newRoom1: str):
        self.room1 = newRoom1
        return
    
    def edit_room2(self, newRoom2: str):
        self.room2 = newRoom2
        return

    def edit_key_name(self, keyName: str):
        self.keyName = keyName
        return
    
    def switch_locked_state(self, isLocked: bool):
        self.isLocked = isLocked
        return
#endregion
#region Room
class Room:
    def __init__(self, name: str, id: int, desc: str = ''):
        self.name = name
        self.id = id
        self.roomItems = []
        self.roomObjects = []
        self.roomExits = []
        self.desc = desc

    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id
    
    def get_exits(self):
        return self.roomExits
    
    def get_items(self):
        return self.roomItems
    
    def get_objects(self):
        return self.roomObjects
    
    def get_desc(self):
        return desc

    def add_exit(self, exit: Exit):
        self.roomExits.append(exit)
        return
    
    def add_item(self, item: Item):
        self.roomItems.append(item)
        return
    
    def add_object(self, object: Object):
        self.roomObjects.append(object)
        return
    
    def edit_item(self, origItem: Item, item: Item):
        self.roomItems[origItem] = item
        return

    def edit_name(self, name: str):
        self.name = name
        return

    def edit_desc(self, desc: str):
        self.desc = desc
        return

    def del_item(self, item: Item):
        self.roomItems.remove(item)
        return
    
    def del_object(self, object: Object):
        self.roomObjects.remove(object)
        return
    
    def del_exit(self, exit: Exit):
        self.roomExits.remove(exit)
        return
#endregion
#region Player
class Player:
    def __init__(self, name: str, id: int, desc: str = ''):
        self.name = name
        self.id = id
        self.playerItems = []
        self.playerClothes = []
        self.room = None
        self.paused = None
        self.desc = desc
    
    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id
    
    def get_items(self):
        return self.playerItems
    
    def get_room(self):
        return self.room
    
    def get_desc(self):
        return self.desc
    
    def get_clothes(self):
        return self.playerClothes

    def get_weight(self):
        invWeight = 0
        for item in self.playerItems:
            invWeight += item.get_weight()
        return invWeight

    def get_clothes_weight(self):
        clothesWeight = 0
        for clothes in self.playerClothes:
            clothesWeight += clothes.get_weight()
        return clothesWeight
    
    def is_paused(self):
        return self.paused
    
    def pause(self):
        self.paused = True
        return
    
    def unpause(self):
        self.paused = False
        return

    def add_item(self, item: Item):
        self.playerItems.append(item)
        return
    
    def add_clothes(self, clothes: Item):
        self.playerClothes.append(clothes)

    def set_room(self, newRoom: Room):
        self.room = newRoom
        return
    
    def edit_item(self, origItem: Item, item: Item):
        self.playerItems[origItem] = item
        return

    def edit_name(self, name: str):
        self.name = name
        return

    def edit_desc(self, desc: str):
        self.desc = desc
        return

    def del_item(self, item: Item):
        self.playerItems.remove(item)
        return
    
    def del_clothes(self, item: Item):
        self.playerClothes.remove(item)
        return
#endregion
#endregion
#region Methods

#region Help Button
    
help_page_one = ("**Player Commands (Page 1/6):**\n\n" +
    "*Inputs in angle brackets (`<>`) are required. Inputs in square brackets (`[]`) are optional.*\n\n" +
    "`/goto <room_name>`\n Allows you to move to a room that is connected to your current room.\n" +
    "`/desc`\n Shows the room's description.\n" + 
    "`/take <item_name> [amount]`\n Takes any amount of a specific item in your current room. Will not pick up an item if it goes over your inventory's weight limit.\n" + 
    "`/drop <item_name> [amount]`\n Drops any amount of a specific item you are currently holding into your current room.\n" + 
    "`/wear <item_name>`\n Allows you to wear any clothing item in your inventory. Will not let you wear a clothing item if it goes over your clothing weight limit.\n")

help_page_two = ("**Player Commands (Page 2/6):**\n\n" +
    "*Inputs in angle brackets (`<>`) are required. Inputs in square brackets (`[]`) are optional.*\n\n" +
    "`/undress <item_name>`\n Drops any clothing item you are currently wearing into your inventory. Will not let you drop the clothing item if it goes over your inventory's weight limit.\n" + 
    "`/takewear <item_name>`\n Allows you to wear any clothing item in your current room. Will not let you wear a clothing item if it goes over your clothing weight limit.\n" + 
    "`/undressdrop <item_name>`\n Drops any clothing item you are currently wearing into your current room.\n" + 
    "`/takefrom <object_name> <item_name> [amount]`\n Takes any amount of a specific item from an object in your current room. Will not pick up an item if it goes over your inventory's weight limit.\n" + 
    "`/dropin <object_name> <item_name> [amount]`\n Drops any amount of a specific item you are currently holding into an object in your current room. Will not let you drop the item if it goes over the object's maximum storage.\n"
    )

    
help_page_three = ("**Player Commands (Page 3/6):**\n\n" +
    "*Inputs in angle brackets (`<>`) are required. Inputs in square brackets (`[]`) are optional.*\n\n" +
    "`/items`\n Shows a list of all items in your current room.\n" +
    "`/inventory`\n Shows a list of all the items in your inventory.\n" +
    "`/clothes`\n Shows a list of all the clothes you are wearing.\n" +
    "`/objects`\n Shows a list of all the objects in your current room.\n" +
    "`/players`\n Shows a list of all the players in your current room."
    )
    
help_page_four = ("**Player Commands (Page 4/6):**\n\n" +
    "*Inputs in angle brackets (`<>`) are required. Inputs in square brackets (`[]`) are optional.*\n\n" +
    "`/exits`\n Shows a list of all the exits in your current room.\n" +
    "`/contents <object_name`\n Shows a list of all the items in an object in your current room.\n" +
    "`/lookitem <item_name>`\n Shows details of a specific item in your current room.\n" +
    "`/lookinv <item_name>`\n Shows details of a specific item in your inventory.\n" +
    "`/lookclothes <item_name>`\n Shows details of a specific clothing item that you are currently wearing."
    )
    
help_page_five = ("**Player Commands (Page 5/6):**\n\n" +
    "*Inputs in angle brackets (`<>`) are required. Inputs in square brackets (`[]`) are optional.*\n\n" +
    "`/lookinside <object_name> <item_name>`\n Shows details of a specific item inside an object in your current room.\n" +
    "`/lookobject <object_name`\n Shows details of a specific object in your current room.\n" +
    "`/lookplayer <player_name>`\n Shows details of a specific player in your current room.\n" + 
    "`/lockobject <object_name> <key_name>`\n Locks an object in your current room using the specified key from your inventory.\n" +
    "`/unlockobject <object_name> <key_name>`\n Unlocks an object in your current room using the specified key from your inventory."
    )

help_page_six = ("**Player Commands (Page 6/6):**\n\n" +
    "*Inputs in angle brackets (`<>`) are required. Inputs in square brackets (`[]`) are optional.*\n\n" +
    "`/lockexit <exit_name> <key_name>`\n Locks an exit in your current room using the specified key from your inventory.\n" +
    "`/unlockexit <exit_name> <key_name>`\n Unlocks an exit in your current room using the specified key from your inventory.\n" +
    "`/roll <max_num> [passing_roll]`\n Rolls for a number between 1 and whatever you would like. If a passing roll is specified, also states whether the roll succeeds.\n" +
    "`/time`\n Checks the current time in roleplay.\n"
    )

helpPages = [help_page_one, help_page_two, help_page_three, help_page_four, help_page_five, help_page_six]

class Help(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.currentHelpPage = 0

    @discord.ui.button(label = 'Back', style = discord.ButtonStyle.gray, emoji = "◀️", disabled = True, custom_id = 'back', row = 0)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.currentHelpPage > 0:
            self.currentHelpPage -= 1
        emby = discord.Embed(description=helpPages[self.currentHelpPage])
        self.children[0].disabled = self.currentHelpPage == 0
        self.children[1].disabled = self.currentHelpPage == 5
        await interaction.response.edit_message(embed=emby, view=self)

    @discord.ui.button(label = 'Next', style = discord.ButtonStyle.gray, emoji = "▶️", disabled = False, custom_id = 'next', row = 0)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.currentHelpPage < 5:
            self.currentHelpPage += 1
        emby = discord.Embed(description=helpPages[self.currentHelpPage])
        self.children[0].disabled = self.currentHelpPage == 0
        self.children[1].disabled = self.currentHelpPage == 5
        await interaction.response.edit_message(embed=emby, view=self)

#endregion

#region Admin Help

adminhelp1 = ("**Admin Commands (Page 1/7):**\n\n" +
    "*Inputs in angle brackets (`<>`) are required. Inputs in square brackets (`[]`) are optional.*\n\n" +
    "`/addplayer <player_name> <player_id> [desc]`\n Connects a new player to a user.\n" +
    "`/delplayer <player_name>`\n Deletes an existing player.\n" +
    "`/addroom <room_name> <room_id> [desc]`\n Connects a new room to a channel.\n" +
    "`/delroom <room_name>`\n Deletes an existing channel.\n" +
    "`/addexit <first_room_name> <second_room_name> [is_locked] [key_name]`\n Adds an exit between two rooms that can be locked and have a key to open or close it." 
    )

adminhelp2 = ("**Admin Commands (Page 2/7):**\n\n" +
    "*Inputs in angle brackets (`<>`) are required. Inputs in square brackets (`[]`) are optional.*\n\n" +
    "`/delexit <first_room_name> <second_room_name>`\n Deletes an existing exit.\n" +
    "`/additem <container> <container_name> <item_name> <weight> [wearable] [desc] [amount] [object_room_name]`\n Adds an item into either a room, object, player's inventory, or player's clothes.\n" +
    "`/delitem <container> <container_name> <item_name> [object_room_name]`\n Deletes an existing item.\n" +
    "`/addobject <room_name> <object_name> <is_container> [is_locked] [key_name] [storage] [desc]`\n Adds an object to a room that can be locked and have a key to open or close it.\n" +
    "`/delobject <room_name> <object_name>`\n Deletes an existing object." 
    )

adminhelp3 = ("**Admin Commands (Page 3/7):**\n\n" +
    "*Inputs in angle brackets (`<>`) are required. Inputs in square brackets (`[]`) are optional.*\n\n" +
    "`/listplayers`\n Lists all current players in the experience.\n" +
    "`/listrooms`\n Lists all current rooms in the experience.\n" +
    "`/listexits <room_name>`\n Lists all exits in a room from anywhere.\n" +
    "`/listitems <container> <container_name> [object_room_name]`\n Lists all items in a container from anywhere.\n" +
    "`/listobjects <room_name>`\n Lists all objects in a room from anywhere." 
    )

adminhelp4 = ("**Admin Commands (Page 4/7):**\n\n" +
    "*Inputs in angle brackets (`<>`) are required. Inputs in square brackets (`[]`) are optional.*\n\n" +
    "`/drag <player_name> <room_name>`\n Moves a player to the room you specify.\n" +
    "`/dragall <room_name>`\n Moves all players to the room you specify.\n" +
    "`/findplayer <player_name>`\n Finds what room a player is currently in and sends a link.\n" +
    "`/findroom <room_name>` \nFinds the channel for a certain room and sends a link.\n" +
    "`/pause`\n Stops all player commands from being registered." 
    )

adminhelp5 = ("**Admin Commands (Page 5/7):**\n\n" +
    "*Inputs in angle brackets (`<>`) are required. Inputs in square brackets (`[]`) are optional.*\n\n" +
    "`/pauseplayer <player_name>`\n Stops a specific player's commands from being registered.\n" +
    "`/unpause`\n Allows all player commands to be registered once again.\n" +
    "`/unpauseplayer <player_name>`\n Allows a specific player's commands to be registered once again.\n" +
    "`/forcetake <player_name> <item_name> [amount]`\n Places a specific item into a player's inventory.\n" +
    "`/forcedrop <player_name> <item_name> [amount]`\n Drops a specific item from a player's inventory." 
    )

adminhelp6 = ("**Admin Commands (Page 6/7):**\n\n" +
    "*Inputs in angle brackets (`<>`) are required. Inputs in square brackets (`[]`) are optional.*\n\n" +
    "`/forcewear <player_name> <container> <item_name> [amount]`\n Makes a player wear a specific clothing item.\n" +
    "`/forceundress <player_name> <container> <item_name> [amount]`\n Makes a player undress a specific clothing item.\n" +
    "`/seeitem <container> <container_name> <item_name> [object_room_name]`\n See details on a specific item from anywhere.\n" +
    "`/seeobject <room_name> <object_name>`\n See details on a specific object from anywhere, including admin details such as the key name.\n" +
    "`/seeexit <room_one_name> <room_two_name>`\n See details on a specific exit from anywhere, including admin details such as the key name." 
    )

adminhelp7 = ("**Admin Commands (Page 7/7):**\n\n" +
    "*Inputs in angle brackets (`<>`) are required. Inputs in square brackets (`[]`) are optional.*\n\n" +
    "`/editplayer <player_name> [new_name] [new_desc]`\n Edits a player's name or description.\n" +
    "`/editroom <room_name> [new_name] [new_desc]`\n Edits a room's name or description.\n" +
    "`/editexit <room_one_name> <room_two_name> [new_locked_state] [new_key]`\n Edits an exit's locked state or key name.\n" +
    "`/edititem <container> <container_name> <item_name> [object_room_name] [new_name] [new_desc] [is_wearable] [new_weight]`\n Edits an item's name, description, wearable state, or weight.\n" +
    "`/editobject <room_name> <object_name> [new_name] [new_desc] [new_container_state] [new_locked_state] [new_key] [new_storage]`\n Edits an object's name, description, container state, locked state, key name, or storage amount." 
    )

adminHelpPages = [adminhelp1, adminhelp2, adminhelp3, adminhelp4, adminhelp5, adminhelp6, adminhelp7]

class AdminHelp(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.currentHelpPage = 0

    @discord.ui.button(label = 'Back', style = discord.ButtonStyle.gray, emoji = "◀️", disabled = True, custom_id = 'back', row = 0)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.currentHelpPage > 0:
            self.currentHelpPage -= 1
        emby = discord.Embed(description=adminHelpPages[self.currentHelpPage])
        self.children[0].disabled = self.currentHelpPage == 0
        self.children[1].disabled = self.currentHelpPage == 6
        await interaction.response.edit_message(embed=emby, view=self)

    @discord.ui.button(label = 'Next', style = discord.ButtonStyle.gray, emoji = "▶️", disabled = False, custom_id = 'next', row = 0)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.currentHelpPage < 6:
            self.currentHelpPage += 1
        emby = discord.Embed(description=adminHelpPages[self.currentHelpPage])
        self.children[0].disabled = self.currentHelpPage == 0
        self.children[1].disabled = self.currentHelpPage == 6
        await interaction.response.edit_message(embed=emby, view=self)

#endregion

#region Save
def save():
    playerdata_out = open('playerdata.pickle', 'wb')
    pickle.dump(playerdata, playerdata_out)
    playerdata_out.close()

    roomdata_out = open('roomdata.pickle', 'wb')
    pickle.dump(roomdata, roomdata_out)
    roomdata_out.close()
#endregion

#region Simplify string
def simplify_string(str):
    str = str.replace(' ', '')
    str = str.lower()
    return str
#endregion

#region Get Player methods

#region Get player name from ID
def get_player_name(id):
    name = ''
    for player in playerdata.values():
        if player.get_id() == id:
            name = player.name
    return name
#endregion
#region Get player from ID
def get_player_from_id(id):
    for player in playerdata.values():
        if player.get_id() == id:
            return player
#endregion
#region Get player from name
def get_player_from_name(name):
    for player in playerdata.values():
        if simplify_string(player.get_name()) == simplify_string(name):
            return player
#endregion

#endregion

#region Get Room methods

#region Get room from ID
def get_room_from_id(id):
    for room in roomdata.values():
        if room.get_id() == id:
            return room
#endregion
#region Get room from name
def get_room_from_name(name):
    for room in roomdata.values():
        if simplify_string(room.get_name()) == simplify_string(name):
            return room
#endregion

#endregion

#region Max weights
max_carry_weight = 10
max_wear_weight = 15

def get_max_carry_weight():
    return max_carry_weight

def set_max_carry_weight(new_max: int):
    global max_carry_weight
    max_carry_weight = new_max
    return

def get_max_wear_weight():
    return max_wear_weight

def set_max_wear_weight(new_max: int):
    global max_wear_weight
    max_wear_weight = new_max
    return
#endregion

#region Start bot
def configure():
    load_dotenv()

def data(file):
    try:
        with open(file, 'rb') as f:
            datafile = pickle.load(f)
    except FileNotFoundError:
        print(f'No {file} found; creating data file.')
        datafile = {}
        with open(file, 'wb') as f:
            pickle.dump(datafile, f)
    return datafile

configure()
GUILD = discord.Object(id=int(os.getenv('guild_id')))

class Client(discord.Client):
    def __init__(self, *, intents:discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)

intents = discord.Intents.all()
client = Client(intents=intents)
playerdata = data('playerdata.pickle')
roomdata = data('roomdata.pickle')

@client.event
async def on_ready():
    configure()
    print(f'Logged on as {client.user}!')
#endregion
#endregion
#endregion


#####################################################
##                                                 ##
##                 PLAYER COMMANDS                 ##
##                                                 ##
#####################################################

#region Pause method
async def check_paused(player, interaction):
    if player is not None and player.is_paused():
        await interaction.response.send_message(content="*Player commands are currently paused. Please wait until the admin unpauses your ability to use player commands.*", ephemeral=True)
        return True
    return False
#endregion

#region Player Commands
#region /desc
@client.tree.command(name = "desc", description = "Get the room's description.", guild=GUILD)
async def desc(interaction: discord.Interaction):
    channel_id = interaction.channel_id
    player_id = interaction.user.id
    player = get_player_from_id(player_id)
    room = get_room_from_id(channel_id)

    if await check_paused(player, interaction):
        return

    if room is None:
        await interaction.response.send_message("*You are not currently in a room. Please contact an admin if you believe this is a mistake*.")
        return

    lookedAt = f"Looked around the room **{room.get_name()}**"
    topic = interaction.channel.topic

    if player is not None:
        lookedAt = f"**{player.get_name()}** looked around the room **{room.get_name()}**"
    if topic is None:
        topic = f"`{room.get_name()} has no description.`"

    await interaction.response.send_message(f"*{lookedAt}*:\n\n{topic}")
#endregion
#region /take
@client.tree.command(name = "take", description = "Take an item from the room.", guild=GUILD)
@app_commands.describe(item_name = "The item you wish to take.")
@app_commands.describe(amount = "The amount of that item you wish to take.")
async def take(interaction: discord.Interaction, item_name: str, amount: int = 0):
    id = interaction.user.id
    channel_id = interaction.channel_id
    player = get_player_from_id(id)
    currRoom = get_room_from_id(channel_id)

    if await check_paused(player, interaction):
        return

    if player == None or not player.get_name() in playerdata.keys():
        await interaction.response.send_message("*You are not a valid player. Please contact the admin if you believe this is a mistake*.")
        return

    if currRoom is None:
        await interaction.response.send_message("*You are not currently in a room. Please contact an admin if you believe this is a mistake*.")
        return

    invWeight = player.get_weight()
    itemList = currRoom.get_items()

    if amount == 0 or amount == 1:
        for item in itemList:
            if simplify_string(item_name) == simplify_string(item.get_name()):
                if (invWeight + item.get_weight()) > max_carry_weight:
                    await interaction.response.send_message(f"***{player.get_name()}** tried to take the item **{item.get_name()}**, but they could not fit it into their inventory.*")
                    return
                player.add_item(item)
                currRoom.del_item(item)
                save()
                await interaction.response.send_message(f"***{player.get_name()}** took the item **{item.get_name()}***.")
                return
        await interaction.response.send_message(f"*Could not find the item **{item_name}**. Please use `/items` to see a list of items in the current room.*")
        return

    if amount < 0:
        await interaction.response.send_message(f"***{str(amount)}** is an invalid input; please use a positive number.*")
        return

    if amount != 0 or amount != 1:
        itemsFound = []
        searchedItem = None
        for item in itemList:
            if simplify_string(item_name) == simplify_string(item.get_name()):
                searchedItem = item
                itemsFound.append(item)
        if len(itemsFound) == 0:
            await interaction.response.send_message(f"*Could not find the item **{item_name}**. Please use `/items` to see a list of items in the current room.*")
            return
        if len(itemsFound) < amount:
            await interaction.response.send_message(f"*Could not find **{str(amount)}** of the item **{item_name}**. Please use `/items` to see a list of items in the current room.*")
            return
        try:
            newCarryWeight = 0
            for i in range(amount):
                newCarryWeight += itemsFound[i].get_weight()
            if (invWeight + newCarryWeight) > get_max_carry_weight():
                await interaction.response.send_message(f"***{player.get_name()}** tried to take **{str(amount)}** of the item **{searchedItem.get_name()}**, but they could not fit that much into their inventory.*")
                return
            for i in range(amount):
                player.add_item(itemsFound[i])
                currRoom.del_item(itemsFound[i])
            save()
            await interaction.response.send_message(f"***{player.get_name()}** took **{str(amount)}** of the item **{searchedItem.get_name()}***.")
            return
        except:
            await interaction.response.send_message(f"*Could not find **{str(amount)}** of the item **{item_name}**. Please use `/items` to see a list of items in the current room.*")
            return

    await interaction.response.send_message(f"*Could not find the item **{item_name}**. Please use `/items` to see a list of items in the current room.*")
#endregion
#region /drop
@client.tree.command(name = "drop", description = "Drop an item from your inventory into the room.", guild=GUILD)
@app_commands.describe(item_name = "The item you wish to drop.")
@app_commands.describe(amount = "The amount of that item you wish to drop.")
async def drop(interaction: discord.Interaction, item_name: str, amount: int = 0):
    id = interaction.user.id
    channel_id = interaction.channel_id
    player = get_player_from_id(id)
    currRoom = get_room_from_id(channel_id)

    if await check_paused(player, interaction):
        return

    if player == None or not player.get_name() in playerdata.keys():
        await interaction.response.send_message("*You are not a valid player. Please contact the admin if you believe this is a mistake.*")
        return

    if currRoom is None:
        await interaction.response.send_message("*You are not currently in a room. Please contact an admin if you believe this is a mistake.*")
        return

    itemList = player.get_items()

    if amount == 0 or amount == 1:
        for item in itemList:
            if simplify_string(item_name) == simplify_string(item.get_name()):
                player.del_item(item)
                currRoom.add_item(item)
                save()
                await interaction.response.send_message(f"***{player.get_name()}** dropped the item **{item.get_name()}**.*")
                return
        await interaction.response.send_message(f"*Could not find the item **{item_name}**. Please use `/inventory` to see a list of items in your inventory.*")
        return

    if amount < 0:
        await interaction.response.send_message(f"***{str(amount)}** is an invalid input; please use a positive number.*")
        return

    if amount != 0 or amount != 1:
        itemsFound = []
        searchedItem = None
        for item in itemList:
            if simplify_string(item_name) == simplify_string(item.get_name()):
                searchedItem = item
                itemsFound.append(item)
        if len(itemsFound) == 0:
            await interaction.response.send_message(f"*Could not find the item **{item_name}**. Please use `/inventory` to see a list of items in your inventory.*")
            return
        if len(itemsFound) < amount:
            await interaction.response.send_message(f"*Could not find **{str(amount)}** of the item **{item_name}**. Please use `/inventory` to see a list of items in your inventory.*")
            return
        try:
            for i in range(amount):
                player.del_item(itemsFound[i])
                currRoom.add_item(itemsFound[i])
            save()
            await interaction.response.send_message(f"***{player.get_name()}** dropped **{str(amount)}** of the item **{searchedItem.get_name()}**.*")
            return
        except:
            await interaction.response.send_message(f"*Could not find **{str(amount)}** of the item **{item_name}**. Please use `/inventory` to see a list of items in your inventory.*")
            return

    await interaction.response.send_message(f"*Could not find the item **{item_name}**. Please use `/inventory` to see a list of items in your inventory.*")
#endregion
#region /takewear
@client.tree.command(name = "takewear", description = "Take a clothing item from the room and wear it.", guild=GUILD)
@app_commands.describe(item_name = "The clothing item you wish to wear.")
async def takewear(interaction: discord.Interaction, item_name: str):
    id = interaction.user.id
    channel_id = interaction.channel_id
    player = get_player_from_id(id)
    currRoom = get_room_from_id(channel_id)

    if await check_paused(player, interaction):
        return

    if player == None or not player.get_name() in playerdata.keys():
        await interaction.response.send_message("*You are not a valid player. Please contact the admin if you believe this is a mistake.*")
        return

    if currRoom is None:
        await interaction.response.send_message("*You are not currently in a room. Please contact an admin if you believe this is a mistake.*")
        return

    clothesWeight = player.get_clothes_weight()
    itemList = currRoom.get_items()
    
    for item in itemList:
        if simplify_string(item_name) == simplify_string(item.get_name()):
            if item.get_wearable_state():
                if (clothesWeight + item.get_weight()) > max_wear_weight:
                    if len(player.get_clothes()) == 0:
                        await interaction.response.send_message(f"***{player.get_name()}** tried to take and wear the item **{item.get_name()}**, but it was too heavy.*")
                        return    
                    await interaction.response.send_message(f"***{player.get_name()}** tried to take and wear the item **{item.get_name()}**, but they were wearing too much already.*")
                    return
                player.add_clothes(item)
                currRoom.del_item(item)
                save()
                await interaction.response.send_message(f"***{player.get_name()}** took and wore the item **{item.get_name()}**.*")
                return
            else:
                await interaction.response.send_message(f"***{player.get_name()}** tried to take and wear the item **{item.get_name()}**, but it was not a piece of clothing.*")
                return

    await interaction.response.send_message(f"Could not find the item **{item_name}**. Please use `/items` to see a list of items in the current room.*")
#endregion
#region /undressdrop
@client.tree.command(name = "undressdrop", description = "Drop a clothing item that you are wearing into the room.", guild=GUILD)
@app_commands.describe(item_name = "The clothing item you wish to drop.")
async def undressdrop(interaction: discord.Interaction, item_name: str):
    id = interaction.user.id
    channel_id = interaction.channel_id
    player = get_player_from_id(id)
    currRoom = get_room_from_id(channel_id)

    if await check_paused(player, interaction):
        return

    if player == None or not player.get_name() in playerdata.keys():
        await interaction.response.send_message("*You are not a valid player. Please contact the admin if you believe this is a mistake.*")
        return

    if currRoom is None:
        await interaction.response.send_message("*You are not currently in a room. Please contact an admin if you believe this is a mistake.*")
        return

    itemList = player.get_clothes()

    for item in itemList:
        if simplify_string(item_name) == simplify_string(item.get_name()):
            if item.get_wearable_state():
                player.del_clothes(item)
                currRoom.add_item(item)
                save()
                await interaction.response.send_message(f"***{player.get_name()}** took off and dropped the item **{item.get_name()}**.*")
                return
            else:
                await interaction.response.send_message(f"***{player.get_name()}** tried to take off and drop **{item.get_name()}**, but it was not a piece of clothing... how are they wearing it?*")
                return


    await interaction.response.send_message(f"*Could not find **{item_name}**. Please use `/clothes` to see the clothes you are wearing.*")
#endregion
#region /wear
@client.tree.command(name = "wear", description = "Wear a clothing item from your inventory.", guild=GUILD)
@app_commands.describe(item_name = "The clothing item you wish to wear.")
async def wear(interaction: discord.Interaction, item_name: str):
    id = interaction.user.id
    player = get_player_from_id(id)

    if await check_paused(player, interaction):
        return

    if player == None or not player.get_name() in playerdata.keys():
        await interaction.response.send_message("*You are not a valid player. Please contact the admin if you believe this is a mistake.")
        return

    clothesWeight = player.get_clothes_weight()
    itemList = player.get_items()
    
    for item in itemList:
        if simplify_string(item_name) == simplify_string(item.get_name()):
            if item.get_wearable_state():
                if (clothesWeight + item.get_weight()) > max_wear_weight:
                    if len(player.get_clothes()) == 0:
                        await interaction.response.send_message(f"***{player.get_name()}** tried to wear the item **{item.get_name()}**, but it was too heavy.*")
                        return    
                    await interaction.response.send_message(f"***{player.get_name()}** tried to wear the item **{item.get_name()}**, but they were wearing too much already.*")
                    return
                player.add_clothes(item)
                player.del_item(item)
                save()
                await interaction.response.send_message(f"***{player.get_name()}** wore the item **{item.get_name()}**.*")
                return
            else:
                await interaction.response.send_message(f"***{player.get_name()}** tried to wear the item **{item.get_name()}**, but it was not a piece of clothing.*")
                return

    await interaction.response.send_message(f"*Could not find the item **{item_name}**. Please use `/inventory` to see a list of items in your inventory.*")
#endregion
#region /undress
@client.tree.command(name = "undress", description = "Take off a clothing item and place it into your inventory.", guild=GUILD)
@app_commands.describe(item_name = "The clothing item you wish to take off.")
async def undress(interaction: discord.Interaction, item_name: str):
    id = interaction.user.id
    player = get_player_from_id(id)

    if await check_paused(player, interaction):
        return

    if player == None or not player.get_name() in playerdata.keys():
        await interaction.response.send_message("*You are not a valid player. Please contact the admin if you believe this is a mistake.*")
        return

    itemList = player.get_clothes()

    for item in itemList:
        if simplify_string(item_name) == simplify_string(item.get_name()):
            if item.get_wearable_state():
                if (player.get_weight() + item.get_weight()) > max_carry_weight:
                    await interaction.response.send_message(f"***{player.get_name()}** tried to take off **{item.get_name()}**, but they could not fit into their inventory.*")
                    return
                player.del_clothes(item)
                player.add_item(item)
                save()
                await interaction.response.send_message(f"***{player.get_name()}** took off the item **{item.get_name()}**.*")
                return
            else:
                await interaction.response.send_message(f"***{player.get_name()}** tried to take off **{item.get_name()}**, but it was not a piece of clothing... how are they wearing it?*")
                return


    await interaction.response.send_message(f"*Could not find **{item_name}**. Please use `/clothes` to see the clothes you are wearing.*")
#endregion
#region /items
@client.tree.command(name = "items", description = "List all of the items in the current room.", guild=GUILD)
async def items(interaction: discord.Interaction):
    channel_id = interaction.channel_id
    player_id = interaction.user.id
    player = get_player_from_id(player_id)
    currRoom = get_room_from_id(channel_id)

    if await check_paused(player, interaction):
        return

    if currRoom is None:
        await interaction.response.send_message("*You are not currently in a room. Please contact an admin if you believe this is a mistake.*")
        return

    itemList = currRoom.get_items()
    
    itemNames = []
    for item in itemList:
        itemNames.append("`" + item.get_name() + "`")

    allItems = ', '.join(itemNames)
    if player is None:
        if len(itemList) == 0:
            await interaction.response.send_message(f"*Looked at the items in the room **{str(currRoom.get_name())}**:*\n\n`No items found.`")
            return
        await interaction.response.send_message(f"*Looked at the items in the room **{str(currRoom.get_name())}**:*\n\n{allItems}")
        return
    
    if len(itemList) == 0:
            await interaction.response.send_message(f"***{player.get_name()}** looked at the items in the room **{str(currRoom.get_name())}**:*\n\n`No items could be found in the room.`")
            return
    await interaction.response.send_message(f"***{player.get_name()}** looked at the items in the room **{str(currRoom.get_name())}**:*\n\n{allItems}")
#endregion
#region /lookitem
@client.tree.command(name = "lookitem", description = "Get the description of a specific item in the current room.", guild=GUILD)
@app_commands.describe(item_name = "The name of the item you wish to look at.")
async def lookitem(interaction: discord.Interaction, item_name: str):
    channel_id = interaction.channel_id
    player_id = interaction.user.id
    player = get_player_from_id(player_id)
    currRoom = get_room_from_id(channel_id)

    if await check_paused(player, interaction):
        return

    if currRoom is None:
        await interaction.response.send_message("*You are not currently in a room. Please contact an admin if you believe this is a mistake.*")
        return
    
    itemList = currRoom.get_items()

    if len(itemList) == 0:
        await interaction.response.send_message("*No items could be found in the room.*")
        return
    
    searchedItem = None
    for item in itemList:
        if simplify_string(item.get_name()) == simplify_string(item_name):
            searchedItem = item
    
    if searchedItem is None:
        await interaction.response.send_message(f"*Could not find the item **{item_name}**. Please use `/items` to see a list of all the items in the current room.*")
        return
    
    if player is not None:
        if searchedItem.get_desc() == '':
            await interaction.response.send_message(f"***{player.get_name()}** looked at the item **{searchedItem.get_name()}**:*\n\n__`{searchedItem.get_name()}`__\n\n__`Weight`__: `{str(searchedItem.get_weight())}`\n__`Wearable`__: `{str(searchedItem.get_wearable_state())}`\n\nItem has no description.")
            return
        else:
            await interaction.response.send_message(f"***{player.get_name()}** looked at the item **{searchedItem.get_name()}**:*\n\n__`{searchedItem.get_name()}`__\n\n__`Weight`__: `{str(searchedItem.get_weight())}`\n__`Wearable`__: `{str(searchedItem.get_wearable_state())}`\n\n{searchedItem.get_desc()}")
        return
    
    if searchedItem.get_desc() == '':
        await interaction.response.send_message(f"*Looked at the item **{searchedItem.get_name()}**:*\n\n__`{searchedItem.get_name()}`__\n\n__`Weight`__: `{str(searchedItem.get_weight())}`\n__`Wearable`__: `{str(searchedItem.get_wearable_state())}`\n\nItem has no description.")
        return

    await interaction.response.send_message(f"*Looked at the item **{searchedItem.get_name()}**:*\n\n__`{searchedItem.get_name()}`__\n\n__`Weight`__: `{str(searchedItem.get_weight())}`\n__`Wearable`__: `{str(searchedItem.get_wearable_state())}`\n\n{searchedItem.get_desc()}")
#endregion
#region /objects
@client.tree.command(name = "objects", description = "List all of the objects in the current room.", guild=GUILD)
async def objects(interaction: discord.Interaction):
    channel_id = interaction.channel_id
    player_id = interaction.user.id
    player = get_player_from_id(player_id)
    currRoom = get_room_from_id(channel_id)

    if await check_paused(player, interaction):
        return

    if currRoom is None:
        await interaction.response.send_message("*You are not currently in a room. Please contact an admin if you believe this is a mistake.*")
        return

    objList = currRoom.get_objects()
    
    objNames = []
    for obj in objList:
        objNames.append("`" + obj.get_name() + "`")

    allObjs = ', '.join(objNames)

    if player is not None:
        if len(objList) == 0:
            await interaction.response.send_message(f"***{player.get_name()}** looked at the objects in the room **{currRoom.get_name()}**:*\n\n`No objects found.`")
            return
        await interaction.response.send_message(f"***{player.get_name()}** looked at the objects in the room **{currRoom.get_name()}**:*\n\n{allObjs}")
        return

    if len(objList) == 0:
            await interaction.response.send_message(f"*Looked at the objects in the room **{currRoom.get_name()}**:*\n\n`No objects found.`")
            return
    await interaction.response.send_message(f"*Looked at the objects in the room **{currRoom.get_name()}**:*\n\n{allObjs}")
#endregion
#region /lockobject
@client.tree.command(name = "lockobject", description = "Lock an object in the current room using a key from your inventory.")
@app_commands.describe(object_name = "The name of the object you wish to lock.")
@app_commands.describe(key_name = "The name of the item in your inventory that can lock the object.")    
async def lockobject(interaction: discord.Interaction, object_name: str, key_name: str):
    player_id = interaction.user.id
    player = get_player_from_id(player_id)
    channel_id = interaction.channel_id
    currRoom = get_room_from_id(channel_id)

    if await check_paused(player, interaction):
        return

    if player is None or not player.get_name() in playerdata.keys():
        await interaction.response.send_message("You are not a valid player. Please contact an admin if you believe this is a mistake.")
        return

    if currRoom is None:
        await interaction.response.send_message("*You are not currently in a room. Please contact an admin if you believe this is a mistake.*")
        return

    searchedObj = None
    for object in currRoom.get_objects():
        if simplify_string(object.get_name()) == simplify_string(object_name):
            searchedObj = object
    
    if searchedObj is None:
        await interaction.response.send_message(f"*Could not find the object **{object_name}**. Please use `/objects` to see a list of all the objects in the current room.*")
        return
    
    if not searchedObj.get_container_state():
        await interaction.response.send_message(f"***{player.get_name()}** tried to lock **{searchedObj.get_name()}**, but it had no lock.*")
        return
    
    if searchedObj.get_locked_state():
        await interaction.response.send_message(f"***{player.get_name()}** tried to lock the object **{searchedObj.get_name()}**, but it was already locked.*")
        return

    searchedItem = None
    
    itemList = player.get_items()
    for item in itemList:
        if simplify_string(item.get_name()) == simplify_string(key_name):
            searchedItem = item

    if searchedItem is None:
        await interaction.response.send_message(f"*Could not find the item **{key_name}**. Please use `/inventory` to see a list of all the items in your inventory.*")
        return

    if simplify_string(searchedObj.get_key_name()) == simplify_string(searchedItem.get_name()):
        searchedObj.switch_locked_state(True)
        save()
        await interaction.response.send_message(f"***{player.get_name()}** locked the object **{searchedObj.get_name()}** using **{searchedItem.get_name()}**.*")
        return

    await interaction.response.send_message(f"***{player.get_name()}** tried to lock the object **{searchedObj.get_name()}**, but **{searchedItem.get_name()}** was not the key.*")
    return
#endregion
#region /unlockobject
@client.tree.command(name = "unlockobject", description = "Unlock an object in the current room using a key from your inventory.")
@app_commands.describe(object_name = "The name of the object you wish to unlock.")
@app_commands.describe(key_name = "The name of the item in your inventory that can unlock the object.")    
async def unlockobject(interaction: discord.Interaction, object_name: str, key_name: str):
    player_id = interaction.user.id
    player = get_player_from_id(player_id)
    channel_id = interaction.channel_id
    currRoom = get_room_from_id(channel_id)

    if await check_paused(player, interaction):
        return

    if player is None or not player.get_name() in playerdata.keys():
        await interaction.response.send_message("*You are not a valid player. Please contact an admin if you believe this is a mistake.*")
        return

    if currRoom is None:
        await interaction.response.send_message("*You are not currently in a room. Please contact an admin if you believe this is a mistake.*")
        return

    searchedObj = None
    for object in currRoom.get_objects():
        if simplify_string(object.get_name()) == simplify_string(object_name):
            searchedObj = object
    
    if searchedObj is None:
        await interaction.response.send_message(f"*Could not find the object **{object_name}**. Please use `/objects` to see a list of all the objects in the current room.*")
        return
    
    if not searchedObj.get_container_state():
        await interaction.response.send_message(f"***{player.get_name()}** tried to unlock **{searchedObj.get_name()}**, but it had no lock.*")
        return
    
    if not searchedObj.get_locked_state():
        await interaction.response.send_message(f"***{player.get_name()}** tried to unlock the object **{searchedObj.get_name()}**, but it was already unlocked.*")
        return

    searchedItem = None
    
    itemList = player.get_items()
    for item in itemList:
        if simplify_string(item.get_name()) == simplify_string(key_name):
            searchedItem = item

    if searchedItem is None:
        await interaction.response.send_message(f"*Could not find the item **{key_name}**. Please use `/inventory` to see a list of all the items in your inventory.*")
        return

    if simplify_string(searchedObj.get_key_name()) == simplify_string(searchedItem.get_name()):
        searchedObj.switch_locked_state(False)
        save()
        await interaction.response.send_message(f"***{player.get_name()}** unlocked the object **{searchedObj.get_name()}** using **{searchedItem.get_name()}**.*")
        return

    await interaction.response.send_message(f"***{player.get_name()}** tried to unlock the object **{searchedObj.get_name()}**, but **{searchedItem.get_name()}** was not the key.*")
    return
#endregion
#region /lookobject
@client.tree.command(name = "lookobject", description = "Get the description of a specific object in the current room.", guild=GUILD)
@app_commands.describe(object_name = "The name of the object you wish to look at.")
async def lookitem(interaction: discord.Interaction, object_name: str):
    channel_id = interaction.channel_id
    player_id = interaction.user.id
    player = get_player_from_id(player_id)
    currRoom = get_room_from_id(channel_id)

    if await check_paused(player, interaction):
        return

    if currRoom is None:
        await interaction.response.send_message("*You are not currently in a room. Please contact an admin if you believe this is a mistake.*")
        return
    
    objList = currRoom.get_objects()

    if len(objList) == 0:
        await interaction.response.send_message("*No objects could be found in the room.*")
        return
    
    searchedObj = None
    for obj in objList:
        if simplify_string(obj.get_name()) == simplify_string(object_name):
            searchedObj = obj
    
    if searchedObj is None:
        await interaction.response.send_message(f"*Could not find the item **{object_name}**. Please use `/objects` to see a list of all the objects in the current room.*")
        return
    
    is_locked = ''
    if searchedObj.get_locked_state():
        is_locked = 'Locked'
    else:
        is_locked = 'Opened'

    storage_amt = ''
    if searchedObj.get_storage() == -1:
        storage_amt = 'Infinite'
    else:
        storage_amt = str(searchedObj.get_storage())
    if player is not None:
        if searchedObj.get_container_state():
            if searchedObj.get_desc() == '':
                await interaction.response.send_message(f"***{player.get_name()}** looked at the object **{searchedObj.get_name()}**:*\n\n__`{searchedObj.get_name()}`__\n\n__`Storage`__: `{str(storage_amt)}`\n__`State`__: `{is_locked}`\n\n`Object has no description.`")
                return
            await interaction.response.send_message(f"***{player.get_name()}** looked at the object **{searchedObj.get_name()}**:*\n\n__`{searchedObj.get_name()}`__\n\n__`Storage`__: `{str(storage_amt)}`\n__`State`__: `{is_locked}`\n\n{searchedObj.get_desc()}")
            return
        if searchedObj.get_desc() == '':
            await interaction.response.send_message(f"***{player.get_name()}** looked at the object **{searchedObj.get_name()}**:*\n\n__`{searchedObj.get_name()}`__\n\n`Object has no description.`")
            return
        await interaction.response.send_message(f"***{player.get_name()}** looked at the object **{searchedObj.get_name()}**:*\n\n__`{searchedObj.get_name()}`__\n\n{searchedObj.get_desc()}")
        return
    
    containerState = searchedObj.get_container_state()
    if containerState == True:
        if searchedObj.get_desc() == '':
            await interaction.response.send_message(f"*Looked at the object **{searchedObj.get_name()}**:*\n\n__`{searchedObj.get_name()}`__\n\n__`Storage`__: `{str(storage_amt)}`\n__`State`__: `{is_locked}`\n\n`Object has no description.`")
            return
        await interaction.response.send_message(f"*Looked at the object **{searchedObj.get_name()}**:*\n\n__`{searchedObj.get_name()}`__\n\n__`Storage`__: `{str(storage_amt)}`\n__`State`__: `{is_locked}`\n\n{searchedObj.get_desc()}")
        return
    
    if searchedObj.get_desc() == '':
        await interaction.response.send_message(f"*Looked at the object **{searchedObj.get_name()}**:*\n\n__`{searchedObj.get_name()}`__\n\n`Object has no description.`")
        return
    await interaction.response.send_message(f"*Looked at the object **{searchedObj.get_name()}**:*\n\n__`{searchedObj.get_name()}`__\n\n{searchedObj.get_desc()}")
    return
#endregion
#region /contents
@client.tree.command(name = "contents", description = "List all of the items inside of an object.")
@app_commands.describe(object_name = "The name of the object you wish to look inside of.")
async def contents(interaction: discord.Interaction, object_name: str):
    channel_id = interaction.channel_id
    player_id = interaction.user.id
    player = get_player_from_id(player_id)
    currRoom = get_room_from_id(channel_id)

    if await check_paused(player, interaction):
        return

    if currRoom is None:
        await interaction.response.send_message("*You are not currently in a room. Please contact an admin if you believe this is a mistake.*")
        return
    
    searchedObj = None
    for object in currRoom.get_objects():
        if simplify_string(object.get_name()) == simplify_string(object_name):
            searchedObj = object
    
    if searchedObj is None:
        await interaction.response.send_message(f"*Could not find the object **{object_name}**. Please use `/objects` to see a list of all the objects in the current room.*")
        return
    
    if not searchedObj.get_container_state():
        if player is not None:
            await interaction.response.send_message(f"***{player.get_name()}** tried to look inside of the object **{searchedObj.get_name()}**, but it was not a container.*")
            return
        await interaction.response.send_message(f"*Tried to look inside of the object **{searchedObj.get_name()}**, but it was not a container.*")
        return
    
    if searchedObj.get_locked_state():
        if player is not None:
            await interaction.response.send_message(f"***{player.get_name()}** tried to look inside of the object **{searchedObj.get_name()}**, but it was locked.*")
            return
        await interaction.response.send_message(f"*Tried to look inside of the object **{searchedObj.get_name()}**, but it was locked.*")
        return
    
    itemList = searchedObj.get_items()
    if len(itemList) == 0:
        if player is not None:
            await interaction.response.send_message(f"***{player.get_name()}** looked inside of the object **{searchedObj.get_name()}**:*\n\n`No items could be found`.")
            return
        await interaction.response.send_message(f"*Looked inside of the object **{searchedObj.get_name()}**:*\n\n`No items could be found`.")
        return
    
    itemNames = []
    for item in itemList:
        itemNames.append("`" + item.get_name() + "`")
        
    allItems = ', '.join(itemNames)
    if player is not None:
        await interaction.response.send_message(f"***{player.get_name()}** looked inside of the object **{searchedObj.get_name()}**:*\n\n{allItems}")
        return
    await interaction.response.send_message(f"*Looked inside of the object **{searchedObj.get_name()}**:*\n\n{allItems}")
#endregion
#region /lookinside
@client.tree.command(name = "lookinside", description = "Get the description of a specific item in an object.", guild=GUILD)
@app_commands.describe(object_name = "The name of the object you wish to look inside of.")
@app_commands.describe(item_name = "The name of the item you wish to look at.")
async def lookinside(interaction: discord.Interaction, object_name: str, item_name: str):
    channel_id = interaction.channel_id
    player_id = interaction.user.id
    player = get_player_from_id(player_id)
    currRoom = get_room_from_id(channel_id)

    if await check_paused(player, interaction):
        return

    if currRoom is None:
        await interaction.response.send_message("*You are not currently in a room. Please contact an admin if you believe this is a mistake.*")
        return
    
    searchedObj = None
    for object in currRoom.get_objects():
        if simplify_string(object.get_name()) == simplify_string(object_name):
            searchedObj = object
    
    if searchedObj is None:
        await interaction.response.send_message(f"*Could not find the object **{object_name}**. Please use `/objects` to see a list of all the objects in the current room.*")
        return
    
    if not searchedObj.get_container_state():
        if player is not None:
            await interaction.response.send_message(f"***{player.get_name()}** tried to look inside of the object **{searchedObj.get_name()}**, but it was not a container.*")
            return
        await interaction.response.send_message(f"*Tried to look inside of the object **{searchedObj.get_name()}**, but it was not a container.*")
        return
    
    if searchedObj.get_locked_state():
        if player is not None:
            await interaction.response.send_message(f"***{player.get_name()}** tried to look inside of the object **{searchedObj.get_name()}**, but it was locked.*")
            return
        await interaction.response.send_message(f"*Tried to look inside of the object **{searchedObj.get_name()}**, but it was locked.*")
        return

    itemList = searchedObj.get_items()

    if len(itemList) == 0:
        await interaction.response.send_message(f"*No items could be found in the object **{searchedObj.get_name()}**.*")
        return
    
    searchedItem = None
    for item in itemList:
        if simplify_string(item.get_name()) == simplify_string(item_name):
            searchedItem = item
    
    if searchedItem is None:
        await interaction.response.send_message(f"*Could not find the item **{item_name}** inside of the object **{searchedObj.get_name()}**. Please use `/contents` to see a list of all the items in an object.*")
        return
    
    if player is not None:
        if searchedItem.get_desc() == '':
            await interaction.response.send_message(f"***{player.get_name()}** looked inside of the object **{searchedObj.get_name()}** at the item **{searchedItem.get_name()}**:*\n\n__`{searchedItem.get_name()}`__\n\n__`Weight`__: `{searchedItem.get_weight()}`\n\n__`Wearable`__: `{searchedItem.get_wearable_state()}`\n\n`Item has no description.`")
            return
        else:
            await interaction.response.send_message(f"***{player.get_name()}** looked inside of the object **{searchedObj.get_name()}** at the item **{searchedItem.get_name()}**:*\n\n__`{searchedItem.get_name()}`__\n\n__`Weight`__: `{searchedItem.get_weight()}`\n\n__`Wearable`__: `{searchedItem.get_wearable_state()}`\n\n{searchedItem.get_desc()}")
            return
    
    if searchedItem.get_desc() == '':
        await interaction.response.send_message(f"*Looked inside of the object **{searchedObj.get_name()}** at the item **{searchedItem.get_name()}**:*\n\n__`{searchedItem.get_name()}`__\n\n__`Weight`__: `{searchedItem.get_weight()}`\n\n__`Wearable`__: `{searchedItem.get_wearable_state()}`\n\n`Item has no description.`")
        return
    
    await interaction.response.send_message(f"*Looked inside of the object **{searchedObj.get_name()}** at the item **{searchedItem.get_name()}**:*\n\n__`{searchedItem.get_name()}`__\n\n__`Weight`__: `{searchedItem.get_weight()}`\n\n__`Wearable`__: `{searchedItem.get_wearable_state()}`\n\n{searchedItem.get_desc()}")
#endregion
#region /takefrom
@client.tree.command(name = "takefrom", description = "Take an item from an object in the room.", guild=GUILD)
@app_commands.describe(object_name = "The object you wish to take an item from.")
@app_commands.describe(item_name = "The item you wish to take.")
@app_commands.describe(amount = "The amount of that item you wish to take.")
async def take(interaction: discord.Interaction, object_name: str, item_name: str, amount: int = 0):
    id = interaction.user.id
    channel_id = interaction.channel_id
    player = get_player_from_id(id)
    currRoom = get_room_from_id(channel_id)

    if await check_paused(player, interaction):
        return

    if player == None or not player.get_name() in playerdata.keys():
        await interaction.response.send_message("*You are not a valid player. Please contact the admin if you believe this is a mistake.*")
        return

    if currRoom is None:
        await interaction.response.send_message("*You are not currently in a room. Please contact an admin if you believe this is a mistake.*")
        return

    searchedObj = None
    for object in currRoom.get_objects():
        if simplify_string(object.get_name()) == simplify_string(object_name):
            searchedObj = object
    
    if searchedObj is None:
        await interaction.response.send_message(f"*Could not find the object **{object_name}**. Please use `/objects` to see a list of all the objects in the current room.*")
        return
    
    if not searchedObj.get_container_state():
        await interaction.response.send_message(f"***{player.get_name()}** tried to take an item from the object **{searchedObj.get_name()}**, but it was not a container.*")
        return
    
    if searchedObj.get_locked_state():
        await interaction.response.send_message(f"***{player.get_name()}** tried to take an item from the object **{searchedObj.get_name()}**, but it was locked.*")
        return

    invWeight = player.get_weight()
    itemList = searchedObj.get_items()

    if amount == 0 or amount == 1:
        for item in itemList:
            if simplify_string(item_name) == simplify_string(item.get_name()):
                if (invWeight + item.get_weight()) > max_carry_weight:
                    await interaction.response.send_message(f"***{player.get_name()}** tried to take the item **{item.get_name()}** from the object **{searchedObj.get_name()}**, but they could not fit it into their inventory.*")
                    return
                player.add_item(item)
                searchedObj.del_item(item)
                save()
                await interaction.response.send_message(f"***{player.get_name()}** took the item **{item.get_name()}** from **{searchedObj.get_name()}***.")
                return
        await interaction.response.send_message(f"*Could not find the item **{item_name}** insode of the object **{searchedObj.get_name()}**. Please use `/contents` to see a list of items in an object.*")
        return

    if amount < 0:
        await interaction.response.send_message(f"***{str(amount)}** is an invalid input; please use a positive number.*")
        return

    if amount != 0 or amount != 1:
        itemsFound = []
        searchedItem = None
        for item in itemList:
            if simplify_string(item_name) == simplify_string(item.get_name()):
                searchedItem = item
                itemsFound.append(item)
        if len(itemsFound) == 0:
            await interaction.response.send_message(f"*Could not find the item **{item_name}** inside of the object **{searchedObj.get_name()}**. Please use `/contents` to see a list of all the items in an object.*")
            return
        if len(itemsFound) < amount:
            await interaction.response.send_message(f"*Could not find **{str(amount)}** of the item **{item_name}** inside of the object **{searchedObj.get_name()}**. Please use `/contents` to see a list of all the items in an object.*")
            return
        try:
            newCarryWeight = 0
            for i in range(amount):
                newCarryWeight += itemsFound[i].get_weight()
            if (invWeight + newCarryWeight) > get_max_carry_weight():
                await interaction.response.send_message(f"***{player.get_name()}** tried to take **{str(amount)}** of the item **{searchedItem.get_name()}** from the object **{searchedObj.get_name()}**, but they could not fit that much into their inventory.*")
                return
            for i in range(amount):
                player.add_item(itemsFound[i])
                searchedObj.del_item(itemsFound[i])
            save()
            await interaction.response.send_message(f"***{player.get_name()}** took **{str(amount)}** of the item **{searchedItem.get_name()}** from **{searchedObj.get_name()}***.")
            return
        except:
            await interaction.response.send_message(f"*Could not find **{str(amount)}** of the item **{item_name}** inside of the object **{searchedObj.get_name()}**. Please use `/contents` to see a list of all the items in an object.*")
            return

    await interaction.response.send_message(f"*Could not find the item **{item_name}** inside of the object **{searchedObj.get_name()}**. Please use `/contents` to see a list of all the items in an object.*")
#endregion
#region /dropin
@client.tree.command(name = "dropin", description = "Drop an item from your inventory into an object.", guild=GUILD)
@app_commands.describe(object_name = "The object you wish to drop the item into.")
@app_commands.describe(item_name = "The item you wish to drop.")
@app_commands.describe(amount = "The amount of that item you wish to drop.")
async def drop(interaction: discord.Interaction, object_name: str, item_name: str, amount: int = 0):
    id = interaction.user.id
    channel_id = interaction.channel_id
    player = get_player_from_id(id)
    currRoom = get_room_from_id(channel_id)

    if await check_paused(player, interaction):
        return

    if player == None or not player.get_name() in playerdata.keys():
        await interaction.response.send_message("*You are not a valid player. Please contact the admin if you believe this is a mistake.*")
        return

    if currRoom is None:
        await interaction.response.send_message("*You are not currently in a room. Please contact an admin if you believe this is a mistake.*")
        return

    searchedObj = None
    for object in currRoom.get_objects():
        if simplify_string(object.get_name()) == simplify_string(object_name):
            searchedObj = object
    
    if searchedObj is None:
        await interaction.response.send_message(f"*Could not find the object **{object_name}**. Please use `/objects` to see a list of all the objects in the current room.*")
        return
    
    if not searchedObj.get_container_state():
        await interaction.response.send_message(f"***{player.get_name()}** tried to drop an item from the object **{searchedObj.get_name()}**, but it was locked.*")
        return
    
    if searchedObj.get_locked_state():
        await interaction.response.send_message("`" + player.get_name() + "` tried to drop an item inside of the object `" + searchedObj.get_name() + "`, but it was locked.")
        return

    maxStorage = searchedObj.get_storage()
    contentsList = searchedObj.get_items()
    itemList = player.get_items()

    if amount == 0 or amount == 1:
        for item in itemList:
            if simplify_string(item_name) == simplify_string(item.get_name()):
                if (len(contentsList) + 1) > maxStorage and not searchedObj.get_storage() == -1:
                    await interaction.response.send_message(f"***{player.get_name()}** tried to drop the item **{item.get_name()}** into the object **{searchedObj.get_name()}**, but there wasn't enough space.*")
                    return
                player.del_item(item)
                searchedObj.add_item(item)
                save()
                await interaction.response.send_message(f"***{player.get_name()}** dropped the item **{item.get_name()}** into **{searchedObj.get_name()}***.")
                return
        await interaction.response.send_message(f"*Could not find the item **{item_name}** insode of the object **{searchedObj.get_name()}**. Please use `/inventory` to see a list of items in your inventory.*")
        return

    if amount < 0:
        await interaction.response.send_message(f"***{str(amount)}** is an invalid input; please use a positive number.*")
        return

    if amount != 0 or amount != 1:
        itemsFound = []
        searchedItem = None
        for item in itemList:
            if simplify_string(item_name) == simplify_string(item.get_name()):
                searchedItem = item
                itemsFound.append(item)
        if len(itemsFound) == 0:
            await interaction.response.send_message(f"*Could not find the item **{item_name}** inside of the object **{searchedObj.get_name()}**. Please use `/inventory` to see a list of items in your inventory.*")
            return
        if len(itemsFound) < amount:
            await interaction.response.send_message(f"*Could not find **{str(amount)}** of the item **{item_name}** inside of the object **{searchedObj.get_name()}**. Please use `/inventory` to see a list of items in your inventory.*")
            return
        try:
            newStorageAmount = 0
            for i in range(amount):
                newStorageAmount += 1
            if (len(contentsList) + newStorageAmount) > maxStorage and not searchedObj.get_storage() == -1:
                await interaction.response.send_message(f"***{player.get_name()}** tried to drop **{str(amount)}** of the item **{searchedItem.get_name()}** into the object **{searchedObj.get_name()}**, but there wasn't enough space.*")
                return
            for i in range(amount):
                player.del_item(itemsFound[i])
                searchedObj.add_item(itemsFound[i])
            save()
            await interaction.response.send_message(f"***{player.get_name()}** dropped **{str(amount)}** of the item **{searchedItem.get_name()}** into **{searchedObj.get_name()}***.")
            return
        except:
            await interaction.response.send_message(f"*Could not find **{str(amount)}** of the item **{item_name}** inside of the object **{searchedObj.get_name()}**. Please use `/inventory` to see a list of items in your inventory.*")
            return

    await interaction.response.send_message(f"*Could not find the item **{item_name}** inside of the object **{searchedObj.get_name()}**. Please use `/inventory` to see a list of items in your inventory.*")
#endregion
#region /inventory
@client.tree.command(name = "inventory", description = "List all of the items in your inventory.")
async def inv(interaction: discord.Interaction):
    id = interaction.user.id
    player = get_player_from_id(id)

    if await check_paused(player, interaction):
        return

    if player == None or not player.get_name() in playerdata.keys():
        await interaction.response.send_message("*You are not a valid player. Please contact the admin if you believe this is a mistake.*")
        return
    
    playerItems = player.get_items()

    if len(playerItems) == 0:
            await interaction.response.send_message(f"***{player.get_name()}** looked into their inventory:*\n\n`No items found.`")
            return

    itemNames = []
    for item in playerItems:
        itemNames.append("`" + item.get_name() + "`")

    allItems = ', '.join(itemNames)
    await interaction.response.send_message(f"***{player.get_name()}** looked into their inventory:*\n\n{allItems}")
#endregion
#region /lookinv
@client.tree.command(name = "lookinv", description = "Get the description of a specific item in your inventory.", guild=GUILD)
@app_commands.describe(item_name = "The name of the item you wish to look at.")
async def lookinv(interaction: discord.Interaction, item_name: str):
    player_id = interaction.user.id
    player = get_player_from_id(player_id)

    if await check_paused(player, interaction):
        return

    if player == None or not player.get_name() in playerdata.keys():
        await interaction.response.send_message("*You are not a valid player. Please contact the admin if you believe this is a mistake.*")
        return
    
    itemList = player.get_items()

    if len(itemList) == 0:
        await interaction.response.send_message(f"*No items could be found in **{player.get_name()}'s** inventory.*")
        return
    
    searchedItem = None
    for item in itemList:
        if simplify_string(item.get_name()) == simplify_string(item_name):
            searchedItem = item
    
    if searchedItem is None:
        await interaction.response.send_message(f"*Could not find the item **{item_name}**. Please use `/inventory` to see a list of items in your inventory.*")
        return
    
    if searchedItem.get_desc() == '':
        await interaction.response.send_message(f"***{player.get_name()}** looked at the item **{searchedItem.get_name()}** in their inventory:*\n\n__`{searchedItem.get_name()}`__\n\n__`Weight`__: `{searchedItem.get_weight()}`\n\n__`Wearable`__: `{searchedItem.get_wearable_state()}`\n\n`Item has no description.`")
        return

    await interaction.response.send_message(f"***{player.get_name()}** looked at the item **{searchedItem.get_name()}** in their inventory:*\n\n__`{searchedItem.get_name()}`__\n\n__`Weight`__: `{searchedItem.get_weight()}`\n\n__`Wearable`__: `{searchedItem.get_wearable_state()}`\n\n{searchedItem.get_desc()}")
#endregion
#region /clothes
@client.tree.command(name = "clothes", description = "List all of the clothes you are currently wearing.")
async def clothes(interaction: discord.Interaction):
    id = interaction.user.id
    player = get_player_from_id(id)

    if await check_paused(player, interaction):
        return

    if player == None or not player.get_name() in playerdata.keys():
        await interaction.response.send_message("*You are not a valid player. Please contact the admin if you believe this is a mistake.*")
        return
    
    playerClothes = player.get_clothes()

    if len(playerClothes) == 0:
            await interaction.response.send_message(f"***{player.get_name()}** looked at their clothes:*\n\n`No clothes found.`")
            return

    clothesNames = []
    for clothes in playerClothes:
        clothesNames.append("`" + clothes.get_name() + "`")

    allClothes = ', '.join(clothesNames)
    await interaction.response.send_message(f"***{player.get_name()}** looked at their clothes:*\n\n{allClothes}")
#endregion
#region /lookclothes
@client.tree.command(name = "lookclothes", description = "Get the description of a specific clothing item you are currently wearing.", guild=GUILD)
@app_commands.describe(clothes_name = "The name of the clothing item you wish to look at.")
async def lookclothes(interaction: discord.Interaction, clothes_name: str):
    player_id = interaction.user.id
    player = get_player_from_id(player_id)

    if await check_paused(player, interaction):
        return

    if player == None or not player.get_name() in playerdata.keys():
        await interaction.response.send_message("*You are not a valid player. Please contact the admin if you believe this is a mistake.*")
        return
    
    clothesList = player.get_clothes()

    if len(clothesList) == 0:
        await interaction.response.send_message(f"*No clothes could be found on **{player.get_name()}**.*")
        return
    
    searchedClothes = None
    for clothes in clothesList:
        if simplify_string(clothes.get_name()) == simplify_string(clothes_name):
            searchedClothes = clothes
    
    if searchedClothes is None:
        await interaction.response.send_message(f"*Could not find the clothing item **{clothes_name}**. Please use `/clothes` to see a list of clothes you are wearing.*")
        return
    
    if searchedClothes.get_desc() == '':
        await interaction.response.send_message(f"***{player.get_name()}** looked at their clothing item **{searchedClothes.get_name()}**:*\n\n__`{searchedClothes.get_name()}`__\n\n__`Weight`__: `{searchedClothes.get_weight()}`\n\n`Clothing item has no description.`")
        return

    await interaction.response.send_message(f"***{player.get_name()}** looked at their clothing item **{searchedClothes.get_name()}**:*\n\n__`{searchedClothes.get_name()}`__\n\n__`Weight`__: `{searchedClothes.get_weight()}`\n\n{searchedClothes.get_desc()}")
#endregion
#region /goto
@client.tree.command(name = "goto", description = "Move to the room that you specify.")
@app_commands.describe(room_name = "The name of the room you wish the move to.")
async def goto(interaction: discord.Interaction, room_name: str):
    id = interaction.user.id
    channel_id = interaction.channel_id
    player = get_player_from_id(id)
    currRoom = None

    if await check_paused(player, interaction):
        return

    if player == None or not player.get_name() in playerdata.keys():
        await interaction.response.send_message("*You are not a valid player. Please contact the admin if you believe this is a mistake.*")
        return
    
    room = get_room_from_name(room_name)

    if room is None:
        await interaction.response.send_message(f"*Could not find the exit **{room_name}**. Please use `/exits` to see a list of exits in the current room.*")
        return

    for newRoom in roomdata.values():
        if newRoom.get_id() == channel_id:
            currRoom = newRoom

    if currRoom is None:
            await interaction.response.send_message(f"*You are not currently in a room. Please contact an admin if you believe this is a mistake.*")
            return

    exits = currRoom.get_exits()

    if len(exits) == 0:
        await interaction.response.send_message(f"*There are no exits in the room **{str(currRoom.get_name())}**.*")
        return

    currExitName = None
    currExit = None
    for exit in exits:
        if exit.get_room1() == currRoom.get_name():
            if simplify_string(exit.get_room2()) == simplify_string(room_name):
                currExitName = exit.get_room2()
                currExit = exit
        else:
            if simplify_string(exit.get_room1()) == simplify_string(room_name):
                currExitName = exit.get_room1()
                currExit = exit

    if currExitName is None:
        await interaction.response.send_message(f"*There is no exit to the room **{room_name}** from **{currRoom.get_name()}**. Please use `/exits` to see a list of exits in the current room.*")
        return

    if currExit.get_locked_state():
        await interaction.response.send_message(f"***{player.get_name()}** tried to enter the room **{currExitName}**, but the exit was locked.*")
        return

    player.set_room(room)
    save()
    
    currChannel = client.get_channel(int(currRoom.get_id()))

    channel = client.get_channel(int(room.get_id()))
    user = client.get_user(int(player.get_id()))

    if channel is None:
        await interaction.response.send_message(f"*Could not find the channel for **{room_name}**. The room may need to be fixed — please contact an admin.*")
    
    if currRoom is not None and currChannel is None:
        await interaction.response.send_message(f"*Could not find the channel for **{currChannel.get_name()}**. The room may need to be fixed — please contact an admin.*")

    if user is None:
        await interaction.response.send_message(f"*Could not find the user <@{player.get_id()}>. The player may need to be fixed — please contact an admin.*")

    await interaction.response.send_message(f"***{player.get_name()}** moved to **{currExitName}**.*")

    if currChannel is not None:
        await channel.send(f"***{player.get_name()}** entered from **{currRoom.get_name()}**.*")
    else:
        await channel.send(f"***{player.get_name()}** entered.*")

    if currChannel is not None:
        await currChannel.set_permissions(user, read_messages = False)
    
    await channel.set_permissions(user, read_messages = True)
#endregion
#region /exits
@client.tree.command(name = "exits", description = "List all locations that are connected to your current room.")
async def exits(interaction: discord.Interaction):
    channel_id = interaction.channel_id
    player_id = interaction.user.id
    player = get_player_from_id(player_id)
    currRoom = get_room_from_id(channel_id)
    
    if await check_paused(player, interaction):
        return

    if currRoom is None:
        await interaction.response.send_message("*You are not currently in a room. Please contact an admin if you believe this is a mistake.*")
        return
    
    exits = currRoom.get_exits()

    if len(exits) == 0:
        await interaction.response.send_message(f"***{player.get_name()}** looked at the exits in the room **{currRoom.get_name()}**:*\n\n`No exits found.`")
        return
    
    exitNames = []
    for exit in exits:
        currExit = ''
        if exit.get_room1() == currRoom.get_name():
            currExit = exit.get_room2()
        else:
            currExit = exit.get_room1()
        exitNames.append("`" + currExit + "`")
    
    allExits = ', '.join(exitNames)
    await interaction.response.send_message(f"***{player.get_name()}** looked at the exits in the room **{currRoom.get_name()}**:*\n\n{allExits}")
#endregion
#region /lockexit
@client.tree.command(name = "lockexit", description = "Locks an exit that is connected to the current room using a key.")
@app_commands.describe(exit_name = "The name of the exit you wish to lock.")
@app_commands.describe(key_name = "The name of the item in your inventory that can lock the exit.")
async def lockexit(interaction: discord.Interaction, exit_name: str, key_name: str):
    player_id = interaction.user.id
    player = get_player_from_id(player_id)
    channel_id = interaction.channel_id
    currRoom = get_room_from_id(channel_id)
    
    if await check_paused(player, interaction):
        return

    if player == None or not player.get_name() in playerdata.keys():
        await interaction.response.send_message("*You are not a valid player. Please contact the admin if you believe this is a mistake.*")
        return

    if currRoom is None:
        await interaction.response.send_message("*You are not currently in a room. Please contact an admin if you believe this is a mistake.*")
        return
    
    exits = currRoom.get_exits()

    if len(exits) == 0:
        await interaction.response.send_message(f"*There are no exits in the room **{currRoom.get_name()}**.*")
        return
    
    searchedExit = None
    searchedExitName = ''
    for exit in exits:
        if simplify_string(exit_name) == simplify_string(exit.get_room1()):
            searchedExit = exit
            searchedExitName = exit.get_room1()
        elif simplify_string(exit_name) == simplify_string(exit.get_room2()):
            searchedExit = exit
            searchedExitName = exit.get_room2()

    if searchedExit is None:
        await interaction.response.send_message(f"*There is no exit to the room **{exit_name}** from **{currRoom.get_name()}**. Please use `/exits` to see a list of exits in the current room.*")
        return

    if searchedExit.get_locked_state():
        await interaction.response.send_message(f"***{player.get_name()}** tried to lock the exit to **{searchedExitName}**, but it was already locked.*")
        return

    searchedItem = None
    itemList = player.get_items()
    for item in itemList:
        if simplify_string(item.get_name()) == simplify_string(key_name):
            searchedItem = item

    if searchedItem is None:
        await interaction.response.send_message(f"*Could not find the item **{key_name}**. Please use `/inventory` to see a list of all the items in your inventory.*")
        return

    if simplify_string(searchedExit.get_key_name()) == simplify_string(searchedItem.get_name()):
        searchedExit.switch_locked_state(True)
        save()
        await interaction.response.send_message(f"***{player.get_name()}** locked the exit to **{searchedExitName}** using **{searchedItem.get_name()}***.")
        return

    await interaction.response.send_message(f"***{player.get_name()}** tried to lock the exit to **{searchedExitName}**, but **{searchedItem.get_name()}** was not the key.*")
    return
#endregion
#region /unlockexit
@client.tree.command(name = "unlockexit", description = "Unlocks an exit that is connected to the current room using a key.")
@app_commands.describe(exit_name = "The name of the exit you wish to unlock.")
@app_commands.describe(key_name = "The name of the item in your inventory that can unlock the exit.")
async def unlockexit(interaction: discord.Interaction, exit_name: str, key_name: str):
    player_id = interaction.user.id
    player = get_player_from_id(player_id)
    channel_id = interaction.channel_id
    currRoom = get_room_from_id(channel_id)
    
    if await check_paused(player, interaction):
        return

    if player == None or not player.get_name() in playerdata.keys():
        await interaction.response.send_message("*You are not a valid player. Please contact the admin if you believe this is a mistake.*")
        return

    if currRoom is None:
        await interaction.response.send_message("*You are not currently in a room. Please contact an admin if you believe this is a mistake.*")
        return
    
    exits = currRoom.get_exits()

    if len(exits) == 0:
        await interaction.response.send_message(f"*There are no exits in the room **{currRoom.get_name()}**.*")
        return
    
    searchedExit = None
    searchedExitName = ''
    for exit in exits:
        if simplify_string(exit_name) == simplify_string(exit.get_room1()):
            searchedExit = exit
            searchedExitName = exit.get_room1()
        elif simplify_string(exit_name) == simplify_string(exit.get_room2()):
            searchedExit = exit
            searchedExitName = exit.get_room2()

    if searchedExit is None:
        await interaction.response.send_message(f"*There is no exit to the room **{exit_name}** from **{currRoom.get_name()}**. Please use `/exits` to see a list of exits in the current room.*")
        return

    if not searchedExit.get_locked_state():
        await interaction.response.send_message(f"***{player.get_name()}** tried to unlock the exit to **{searchedExitName}**, but it was already unlocked.*")
        return

    searchedItem = None
    itemList = player.get_items()
    for item in itemList:
        if simplify_string(item.get_name()) == simplify_string(key_name):
            searchedItem = item

    if searchedItem is None:
        await interaction.response.send_message(f"*Could not find the item **{key_name}**. Please use `/inventory` to see a list of all the items in your inventory.*")
        return

    if simplify_string(searchedExit.get_key_name()) == simplify_string(searchedItem.get_name()):
        searchedExit.switch_locked_state(False)
        save()
        await interaction.response.send_message(f"***{player.get_name()}** unlocked the exit to **{searchedExitName}** using **{searchedItem.get_name()}***.")
        return

    await interaction.response.send_message(f"***{player.get_name()}** tried to unlock the exit to **{searchedExitName}**, but **{searchedItem.get_name()}** was not the key.*")
    return
#endregion
#region /lookplayer
@client.tree.command(name = "lookplayer", description = "Get the description of a specific player in the current room.")
@app_commands.describe(player_name = "The list of players in the current room.")
async def lookplayer(interaction: discord.Interaction, player_name: str):
    player_id = interaction.user.id
    lookingPlayer = get_player_from_id(player_id)
    
    if await check_paused(lookingPlayer, interaction):
        return

    simplified = simplify_string(player_name)
    player = None

    for p in playerdata.values():
        if simplify_string(p.get_name()) == simplified:
            player = p
    
    if player is None:
        await interaction.response.send_message(f"*Could not find player **{player_name}**. Please use `/players` to see a list of all players in the current room.*")
        return

    clothesList = player.get_clothes()
    clothesNames = []
    for clothing in clothesList:
        clothesNames.append("`" + clothing.get_name() + "`")
    allClothes = ', '.join(clothesNames)

    if lookingPlayer is None:
        if player.get_desc() == '':
            if len(clothesList) == 0:
                await interaction.response.send_message(f"*Looked at **{player.get_name()}**:*\n\n__`{player.get_name()}`__\n\n__`Wearing`__: `Nothing.`\n\n`Player has no description.`")
                return
            await interaction.response.send_message(f"*Looked at **{player.get_name()}**:*\n\n__`{player.get_name()}`__\n\n__`Wearing`__: {allClothes}\n\n`Player has no description.`")
            return
        if len(clothesList) == 0:
            await interaction.response.send_message(f"*Looked at **{player.get_name()}**:*\n\n__`{player.get_name()}`__\n\n__`Wearing`__: `Nothing.`\n\n{player.get_desc()}")
            return
        await interaction.response.send_message(f"*Looked at **{player.get_name()}**:*\n\n__`{player.get_name()}`__\n\n__`Wearing`__: {allClothes}\n\n{player.get_desc()}")
        return

    if lookingPlayer is player:
        if player.get_desc() == '':
            if len(clothesList) == 0:
                await interaction.response.send_message(f"***{lookingPlayer.get_name()}** looked at themself:*\n\n__`{player.get_name()}`__\n\n__`Wearing`__: `Nothing.`\n\n`Player has no description.`")
                return
            await interaction.response.send_message(f"***{lookingPlayer.get_name()}** looked at themself:*\n\n__`{player.get_name()}`__\n\n__`Wearing`__: {allClothes}\n\n`Player has no description.`")
            return
        if len(clothesList) == 0:
            await interaction.response.send_message(f"***{lookingPlayer.get_name()}** looked at themself:*\n\n__`{player.get_name()}`__\n\n__`Wearing`__: `Nothing.`\n\n{player.get_desc()}")
            return
        await interaction.response.send_message(f"***{lookingPlayer.get_name()}** looked at themself:*\n\n__`{player.get_name()}`__\n\n__`Wearing`__: {allClothes}\n\n{player.get_desc()}")
        return


    if player.get_desc() == '':
            if len(clothesList) == 0:
                await interaction.response.send_message(f"***{lookingPlayer.get_name()}** looked at **{player.get_name()}**:*\n\n__`{player.get_name()}`__\n\n__`Wearing`__: `Nothing.`\n\n`Player has no description.`")
                return
            await interaction.response.send_message(f"***{lookingPlayer.get_name()}** looked at **{player.get_name()}**:*\n\n__`{player.get_name()}`__\n\n__`Wearing`__: {allClothes}\n\n`Player has no description.`")
            return

    if len(clothesList) == 0:
        await interaction.response.send_message(f"***{lookingPlayer.get_name()}** looked at **{player.get_name()}**:*\n\n__`{player.get_name()}`__\n\n__`Wearing`__: `Nothing.`\n\n{player.get_desc()}")
        return
    await interaction.response.send_message(f"***{lookingPlayer.get_name()}** looked at **{player.get_name()}**:*\n\n__`{player.get_name()}`__\n\n__`Wearing`__: {allClothes}\n\n{player.get_desc()}")
#endregion
#region /players
@client.tree.command(name = "players", description = "List all players in the current room.")
async def players(interaction: discord.Interaction):
    channel_id = interaction.channel_id
    player_id = interaction.user.id
    player = get_player_from_id(player_id)
    currRoom = get_room_from_id(channel_id)

    if await check_paused(player, interaction):
        return

    if currRoom is None:
        await interaction.response.send_message("*You are not currently in a room. Please contact an admin if you believe this is a mistake.*")
        return

    playerList = []
    for thisPlayer in playerdata.values():
        currPlayer = ''
        if thisPlayer.get_room() is not None:
            if thisPlayer.get_room().get_name() == currRoom.get_name():
                currPlayer = thisPlayer.get_name()
                playerList.append("`" + currPlayer + "`")

    allPlayers = ", ".join(playerList)

    if player is None:
        if len(playerList) == 0:
            await interaction.response.send_message(f"*Looked at the players in the room **{currRoom.get_name()}**:*\n\n`No players found.`")
            return
        await interaction.response.send_message(f"*Looked at the players in the room **{currRoom.get_name()}**:*\n\n{allPlayers}")
        return
    

    if len(playerList) == 0:
        await interaction.response.send_message(f"***{player.get_name()}** looked at the players in the room **{currRoom.get_name()}**:*\n\n`No players found.`")
        return

    await interaction.response.send_message(f"***{player.get_name()}** looked at the players in the room **{currRoom.get_name()}**:*\n\n{allPlayers}")
#endregion
#region /roll
@client.tree.command(name = "roll", description = "Roll for a random number.")
@app_commands.describe(max_num = "The maximum number for the roll.")
@app_commands.describe(passing_roll = "Optional; The number that the roll must be more than to be considered a passing roll.")
async def roll(interaction: discord.Interaction, max_num: int, passing_roll: int = -1):
    player_id = interaction.user.id
    player = get_player_from_id(player_id)
    rollNum = random.randint(1, max_num)
    passingString = '.'

    if passing_roll != -1:
        if rollNum >= passing_roll:
            passingString = ', attempting to beat **' + str(passing_roll) + '**. Roll **succeeded**!'
        else:
            passingString = ', attempting to beat **' + str(passing_roll) + '**. Roll **failed**.'

    if player is not None:
        await interaction.response.send_message(f"***{player.get_name()}** rolled **{str(rollNum)}** out of **{str(max_num)}**{passingString}*")
        return
    
    if passing_roll == -1:
            passingString = ''
    await interaction.response.send_message(f"*Rolled **{str(rollNum)}** out of **{str(max_num)}**{passingString}*")
    return
#endregion
#region /time
@client.tree.command(name = "time", description = "Check the current time in roleplay.")
async def time(interaction: discord.Interaction):
    player_id = interaction.user.id
    player = get_player_from_id(player_id)

    t = datetime.datetime.now()
    current_time = t.strftime("%I:%M %p")

    if player is not None:
        await interaction.response.send_message(f"***{player.get_name()}** checked the time:*\n`{current_time }`")
        return

    await interaction.response.send_message(f"`{current_time}`")
#endregion
#region /help
@client.tree.command(name = "help", description = "Gives descriptions of every player command.")
async def help(interaction: discord.Interaction):
    emby = discord.Embed(description=help_page_one)
    await interaction.response.send_message(embed=emby, view = Help(), ephemeral=True)

#endregion
#endregion

#####################################################
##                                                 ##
##                  ADMIN COMMANDS                 ##
##                                                 ##
#####################################################

#region Admin Commands
#region /addplayer
@client.tree.command(name = "addplayer", description = "Add a new player to the experience.", guild=GUILD)
@app_commands.describe(player_name = "The new player's name.")
@app_commands.describe(player_id = "The Discord ID of the user that controls the player.")
@app_commands.describe(desc = "The description of the player you wish to add to the experience.")
@app_commands.default_permissions()
async def addplayer(interaction: discord.Interaction, player_name: str, player_id: str, desc: str = ''):
    
    if player_name in playerdata.keys():
        await interaction.response.send_message(f"*Player **{player_name}** already exists. Please use a different name.*")
        return

    try:
        player_id = int(player_id)
    except:
        await interaction.response.send_message(f"*A user ID must be made up entirely of integers. Please enter a valid user ID.*")
        return
    
    if interaction.guild.get_member(player_id) == None:
        await interaction.response.send_message(f"*Could not find <@{str(player_id)}>. Please enter a valid user ID.*")
        return

    if get_player_from_id(player_id) != None:
        await interaction.response.send_message(f"*<@{str(player_id)}> is already connected to the player **{get_player_name(player_id)}**.*")
        return

    playerdata[player_name] = Player(player_name, player_id, desc)
    save()
    await interaction.response.send_message(f"*Player **{player_name}** connected to <@{str(player_id)}>.*")
#endregion
#region /delplayer
@client.tree.command(name = "delplayer", description = "Remove a player from the experience.", guild=GUILD)
@app_commands.describe(player_name = "The player you wish to remove's name.")
@app_commands.default_permissions()
async def delplayer(interaction: discord.Interaction, player_name: str):

    simplified_player = simplify_string(player_name)
    simplified_player_keys = {simplify_string(key): key for key in playerdata.keys()}

    if simplified_player in simplified_player_keys:
        original_key = simplified_player_keys[simplified_player]
        try:
            del playerdata[original_key]
            save()
            await interaction.response.send_message(f"*Deleted player **{original_key}***.")
            return
        except:
            await interaction.response.send_message(f"*Failed to delete **{original_key}**. Please contact the bot's developer.*")
            return
    else:
        await interaction.response.send_message(f"*Could not find player **{player_name}**. Please use `/listplayers` to see all current players.*")
#endregion
#region /listplayers
@client.tree.command(name = "listplayers", description = "List all the current players added to the experience.", guild=GUILD)
@app_commands.default_permissions()
async def listplayers(interaction: discord.Interaction):

    if len(playerdata) == 0:
        await interaction.response.send_message(f"*There are currently no players.*")
        return

    playerList = ''
    for key in playerdata:
        currPlayer = playerdata[key]
        nextPlayer = ("`", currPlayer.get_name(), "`: <@", str(currPlayer.get_id()), ">")
        nextPlayer = ''.join(nextPlayer)
        playerList = playerList + "\n" + nextPlayer

    await interaction.response.send_message(playerList)
#endregion
#region /addroom
@client.tree.command(name = "addroom", description = "Add a room to the experience.")
@app_commands.describe(room_name = "The name of the room you wish to create.")
@app_commands.describe(room_id = "The Discord ID of the channel you wish to connect the room to.")
@app_commands.describe(desc = "The description of the room you wish to add to the experience.")
@app_commands.default_permissions()
async def addroom(interaction: discord.Interaction, room_name: str, room_id: str, desc: str = ''):
    
    try:
        room_id = int(room_id)
    except:
        await interaction.response.send_message(f"*A room ID must be made up entirely of integers. Please enter a valid room ID.*")
        return

    if interaction.guild.get_channel(int(room_id)) == None:
        await interaction.response.send_message(f"*Could not find the channel <#{str(room_id)}>.*")
        return

    for room in roomdata.values():
        if simplify_string(room_name) == simplify_string(room.get_name()):
            await interaction.response.send_message(f"*Room name **{room_name}** is already in use. Please give the room a separate name.*")
            return
        if room.get_id() == room_id:
            await interaction.response.send_message(f"*The channel <#**{str(room_id)}**> is already in use. Please give the room a separate channel.*")
            return

    roomdata[room_name] = Room(room_name, room_id, desc)
    channel = client.get_channel(int(room_id))
    await channel.edit(topic=desc)
    save()

    await interaction.response.send_message(f"*Room **{room_name}** connected to <#{str(room_id)}>.*")
#endregion
#region /delroom
@client.tree.command(name = "delroom", description = "Remove a room from the experience.")
@app_commands.describe(room_name = "The name of the room you wish to remove.")
@app_commands.default_permissions()
async def delroom(interaction: discord.Interaction, room_name: str):
    simplified_room = simplify_string(room_name)
    simplified_keys = {simplify_string(key): key for key in roomdata.keys()}
    if simplified_room in simplified_keys:
        original_key = simplified_keys[simplified_room]
        try:
            del roomdata[original_key]
            for room in roomdata.values():
                exits = room.get_exits()
                for exit in exits:
                    if exit.get_room1() == original_key or exit.get_room2() == original_key:
                        room.del_exit(exit)
            save()
            await interaction.response.send_message(f"*Deleted room **{original_key}**.*")
            return
        except:
            await interaction.response.send_message(f"*Failed to delete room **{original_key}**. Please contact the bot's developer.*")
            return
    
    else:
        await interaction.response.send_message(f"*Could not find room **{room_name}**. Please use `/listrooms` to see all current rooms.*")
#endregion
#region /listrooms
@client.tree.command(name = "listrooms", description = "List all rooms that have been added to the experience.")
@app_commands.default_permissions()
async def listrooms(interaction: discord.Interaction):
    if len(roomdata) == 0:
        await interaction.response.send_message("There are currently no rooms.")
        return
    
    roomList = ''
    for key in roomdata:
        currRoom = roomdata[key]
        nextRoom = ("`", currRoom.get_name(), "`: <#", str(currRoom.get_id()), ">.")
        nextRoom = ''.join(nextRoom)
        roomList = roomList + "\n" + nextRoom
    
    await interaction.response.send_message(roomList)
#endregion
#region /addexit
@client.tree.command(name = "addexit", description = "Add a connection between two rooms.")
@app_commands.describe(first_room_name = "The first of the two rooms you wish to add a connection between.")
@app_commands.describe(second_room_name = "The second of the two rooms you wish to add a connection between.")
@app_commands.describe(is_locked = "True or false; whether or not you wish the exit to be locked.")
@app_commands.describe(key_name = "The name of the item you wish to be able lock and unlock the exit.")
@app_commands.default_permissions()
async def addexit(interaction: discord.Interaction, first_room_name: str, second_room_name: str, is_locked: bool = False, key_name: str = ''):

    room_one = get_room_from_name(first_room_name)
    room_two = get_room_from_name(second_room_name)

    if room_one is None:
        await interaction.response.send_message(f"*Room **{first_room_name}** could not be found. Please use `/listrooms` to see all current rooms.*")
        return
    if room_two is None:
        await interaction.response.send_message(f"*Room **{second_room_name}** could not be found. Please use `/listrooms` to see all current rooms.*")
        return

    for exit in room_one.get_exits():
        if simplify_string(exit.get_room1()) == simplify_string(room_one.get_name()):
            if simplify_string(exit.get_room2()) == simplify_string(room_two.get_name()):
                await interaction.response.send_message(f"*Connection from **{room_one.get_name()}** to **{room_two.get_name()}** already exists. Please use `/editexit` if you would like to change it.*")
                return
        elif simplify_string(exit.get_room1()) == simplify_string(room_two.get_name()):
            if simplify_string(exit.get_room2()) == simplify_string(room_one.get_name()):
                await interaction.response.send_message(f"*Connection from **{room_one.get_name()}** to **{room_two.get_name()}** already exists. Please use `/editexit` if you would like to change it.*")
                return

    exit: Exit = Exit(room_one.get_name(), room_two.get_name(), is_locked, key_name)

    room_one.add_exit(exit)
    room_two.add_exit(exit)

    save()

    await interaction.response.send_message(f"*Connection created between **{room_one.get_name()}** and **{room_two.get_name()}**.*")
#endregion 
#region /delexit
@client.tree.command(name = "delexit", description = "Delete a connection between two rooms.")
@app_commands.describe(first_room_name = "The first of the two rooms you wish to add a connection between.")
@app_commands.describe(second_room_name = "The second of the two rooms you wish to add a connection between.")
@app_commands.default_permissions()
async def delexit(interaction: discord.Interaction, first_room_name: str, second_room_name: str):

    simplified_room_one = simplify_string(first_room_name)
    simplified_room_two = simplify_string(second_room_name)
    simplified_keys = {simplify_string(key): key for key in roomdata.keys()}

    if simplified_room_one not in simplified_keys:
        await interaction.response.send_message(f"*Room **{first_room_name}** could not be found. Please use `/listrooms` to see all current rooms.*")
        return
    if simplified_room_two not in simplified_keys:
        await interaction.response.send_message(f"*Room **{second_room_name}** could not be found. Please use `/listrooms` to see all current rooms.*")
        return
    
    room_one = get_room_from_name(simplified_room_one)
    room_two = get_room_from_name(simplified_room_two)
    original_room_one = simplified_keys[simplified_room_one]
    original_room_two = simplified_keys[simplified_room_two]

    exitsOne = room_one.get_exits()
    exitsTwo = room_two.get_exits()

    if len(exitsOne) == 0:
        await interaction.response.send_message(f"*There are no exits in the room **{str(room_one.get_name())}**.*")
        return
    if len(exitsTwo) == 0:
        await interaction.response.send_message(f"*There are no exits in the room **{str(room_two.get_name())}**.*")
        return

    exit = None
    for exit in exitsOne:
        if exit.get_room1() == room_one.get_name():
            if simplify_string(exit.get_room2()) == simplify_string(first_room_name):
                exit = exit
        else:
            if simplify_string(exit.get_room1()) == simplify_string(first_room_name):
                exit = exit

    room_one.del_exit(exit)
    room_two.del_exit(exit)

    save()

    await interaction.response.send_message(f"*Connection removed between **{original_room_one}** and **{original_room_two}**.*")
#endregion 
#region /drag 
@client.tree.command(name = "drag", description = "Drag a player into a room.")
@app_commands.describe(player_name = "The name of the player that you wish to drag.")
@app_commands.describe(room_name = "The name of the room you wish to drag the player into.")
@app_commands.default_permissions()
async def drag(interaction: discord.Interaction, player_name: str, room_name: str):

    simplified_player = simplify_string(player_name)
    simplified_player_keys = {simplify_string(key): key for key in playerdata.keys()}

    simplified_room = simplify_string(room_name)
    simplified_room_keys = {simplify_string(key): key for key in roomdata.keys()}

    if simplified_player not in simplified_player_keys:
        await interaction.response.send_message(f"*Player **{player_name}** could not be found. Please use `/listplayers` to see all current players.*")
        return
    
    if simplified_room not in simplified_room_keys:
        await interaction.response.send_message(f"*Room `" + {room_name} + "` could not be found. Please use `/listrooms` to see all current rooms.*")
        return

    player = get_player_from_name(player_name)
    prevRoom = player.get_room()
    room = get_room_from_name(room_name)

    if room is None:
        await interaction.response.send_message(f"*Room **{room_name}** could not be found. Please use `/listrooms` to see all current rooms.*")
        return
    
    player.set_room(room)
    save()

    if prevRoom is not None:
        prevChannel = client.get_channel(int(prevRoom.get_id()))
    else:
        prevChannel = None

    channel = client.get_channel(int(room.get_id()))
    user = client.get_user(int(player.get_id()))

    if channel is None:
        await interaction.response.send_message(f"*Could not find the channel for **{room_name}**. Is there an error in the ID?*")
    
    if prevRoom is not None and prevChannel is None:
        await interaction.response.send_message(f"*Could not find the channel for **{prevRoom.get_name()}**. Is there an error in the ID?*")

    if user is None:
        await interaction.response.send_message(f"*Could not find the user <@{player.get_id()}>. Is there an error in the ID?*")

    await interaction.response.send_message(f"*Dragged **{player.get_name()}** to **{room.get_name()}**.*")
    
    if prevChannel is not None:
        await prevChannel.send(f"***{player.get_name()}** was dragged to **{room.get_name()}**.*")
        await channel.send(f"***{player.get_name()}** entered from **{prevRoom.get_name()}**.*")
    else:
        await channel.send(f"***{player.get_name()}** entered the room.*")

    if prevChannel is not None:
        await prevChannel.set_permissions(user, read_messages = False)
    
    await channel.set_permissions(user, read_messages = True)
#endregion 
#region /dragall
@client.tree.command(name = "dragall", description = "Drag all players into a room.")
@app_commands.describe(room_name = "The name of the room you wish to drag the player into.")
@app_commands.default_permissions()
async def dragall(interaction: discord.Interaction, room_name: str):
    room = get_room_from_name(room_name)
    for player in playerdata.values():
        prevRoom = player.get_room()

        if room is None:
            await interaction.response.send_message(f"*Room **{room_name}** could not be found. Please use `/listrooms` to see all current rooms.*")
            return
        
        player.set_room(room)
        save()

        if prevRoom is not None:
            prevChannel = client.get_channel(int(prevRoom.get_id()))
        else:
            prevChannel = None

        channel = client.get_channel(int(room.get_id()))
        user = client.get_user(int(player.get_id()))

        if channel is None:
            await interaction.response.send_message(f"*Could not find the channel for **{room_name}**. Is there an error in the ID?*")
        
        if prevRoom is not None and prevChannel is None:
            await interaction.response.send_message(f"*Could not find the channel for **{prevRoom.get_name()}**. Is there an error in the ID?*")

        if user is None:
            await interaction.response.send_message(f"*Could not find the user <@{player.get_id()}>. Is there an error in the ID?*")

        if prevChannel is not None:
            await prevChannel.set_permissions(user, read_messages = False)
        
        await channel.set_permissions(user, read_messages = True)
    
    await interaction.response.send_message(f"*All players dragged to **{room.get_name()}**.*")
#endregion 
#region /findplayer 
@client.tree.command(name = "findplayer", description = "Tells which room a player is currently in.")
@app_commands.describe(player_name = "The name of the player you wish to find.")
@app_commands.default_permissions()
async def findplayer(interaction: discord.Interaction, player_name: str):
    
    simplified_player = simplify_string(player_name)
    simplified_player_keys = {simplify_string(key): key for key in playerdata.keys()}

    if simplified_player not in simplified_player_keys:
        await interaction.response.send_message(f"*Player **{player_name}** could not be found. Please use `/listplayers` to see all current players.*")
        return

    player = get_player_from_name(player_name)
    room = player.get_room()

    if room is None:
        await interaction.response.send_message(f"***{player.get_name()}** is not yet in a room.*")
        return

    await interaction.response.send_message(f"***{player.get_name()}** is currently in the room **{room.get_name()}**.*\n\n`Jump`: <#" + str(room.get_id()) + ">")
#endregion
#region /findroom 
@client.tree.command(name = "findroom", description = "Tells what channel is connected to a room.")
@app_commands.describe(room_name = "The name of the room you wish to find.")
@app_commands.default_permissions()
async def findroom(interaction: discord.Interaction, room_name: str):
    
    room = get_room_from_name(room_name)

    if room is None:
        await interaction.response.send_message(f"*Could not find the room **{room_name}***")
        return

    await interaction.response.send_message(f"`{room.get_name()}`: <#" + str(room.get_id()) + ">")
#endregion
#region /additem
@client.tree.command(name = "additem", description = "Add an item into the experience.", guild=GUILD)
@app_commands.choices(container = [
    app_commands.Choice(name = "Room", value = 0),
    app_commands.Choice(name = "Player's inventory", value = 1),
    app_commands.Choice(name = "Player's clothes", value = 2),
    app_commands.Choice(name = "Object", value = 3)
    ])
@app_commands.describe(container_name = "The name of the container you wish to add the item to. If an object, be sure to specify a room name.")
@app_commands.describe(item_name = "The name of the item you wish to add.")
@app_commands.describe(weight = "The weight of the item you wish to add.")
@app_commands.describe(wearable = "True or false; whether you wish the item to be wearable or not.")
@app_commands.describe(desc = "The description of the item you wish to add.")
@app_commands.describe(amount = "The amount of the item you wish to add.")
@app_commands.describe(object_room_name = "Optional; if the container is an object, specify the room name.")
@app_commands.default_permissions()
async def additem(interaction: discord.Interaction, container: app_commands.Choice[int], container_name: str, item_name: str, weight: float, wearable: bool = False, desc: str = '', amount: int = 1, object_room_name: str = ''):
    
    ifNone = ''
    containerType = ''
    amountStr = 'the'
    containerVar = None
    currentWeight = 0
    capacity = 0
    checkCapacity = False

    if amount < 1:
        await interaction.response.send_message(f"***{str(amount)}** is an invalid input; please use a positive number greater than one.*")
        return

    if container.value == 0:
        ifNone = f"*Room **{container_name}** could not be found. Please use `/listrooms` to see all current rooms.*"
        containerType = "room"
        containerVar = get_room_from_name(container_name)
    
    elif container.value == 1:
        ifNone = f"*Player **{container_name}** could not be found. Please use `/listplayers` to see all current players.*"
        containerType = "inventory of"
        containerVar = get_player_from_name(container_name)
        currentWeight = containerVar.get_weight()
        checkCapacity = True
        capacity = max_carry_weight

    elif container.value == 2:
        ifNone = f"*Player **{container_name}** could not be found. Please use `/listplayers` to see all current players.*"
        containerType = "clothes of"
        containerVar = get_player_from_name(container_name)
        currentWeight = containerVar.get_clothes_weight()
        checkCapacity = True
        capacity = max_wear_weight

    elif container.value == 3:

        if object_room_name == '':
            await interaction.response.send_message(f"*To add an item to an object, you must specify the room name as well. Please use `/listrooms` to see all current rooms.*")
            return

        room = get_room_from_name(object_room_name)

        if room is None:
            await interaction.response.send_message(f"*Room **{object_room_name}** could not be found. Please use `/listrooms` to see all current rooms.*")
            return

        for obj in room.get_objects():
            if simplify_string(obj.get_name()) == simplify_string(container_name):
                containerVar = obj

        ifNone = f"*Object **{container_name}** could not be found. Please use `/listobjects` to see the objects in a room.*"
        
        containerType = "object"
        if containerVar.get_storage() != -1:
            checkCapacity = True

    if containerVar is None:
        await interaction.response.send_message(ifNone)
        return
    
    addedWeight = 0
    if checkCapacity:
        if containerType == "object":
            if (amount + len(containerVar.get_items())) > containerVar.get_storage():
                await interaction.response.send_message(f"*Could not add **{item_name}** to the object **{containerVar.get_name()}**: Maximum storage reached.*")
                return
        else:
            for i in range(amount):
                addedWeight += weight
            if (addedWeight + currentWeight) > capacity:
                await interaction.response.send_message(f"*Could not add **{item_name}** to the {containerType} **{containerVar.get_name()}**: Maximum weight reached.*")
                return

    if amount > 1:
        amountStr = f"**{amount}** of the"

    # self, name: str, weight: float, wearable: bool, desc: str = ''
    item: Item = Item(item_name, weight, wearable, desc)
    
    if container.value == 2:
        if not item.get_wearable_state():
            await interaction.response.send_message(f"*Could not add **{item_name}** to **{containerVar.get_name()}**'s clothes: Item must be wearable.*")
            return
        for i in range(amount):
            containerVar.add_clothes(item)

    else:
        for i in range(amount):
            containerVar.add_item(item)

    save()
    await interaction.response.send_message(f"*Added {amountStr} item **{item_name}** to the {containerType} **{containerVar.get_name()}**.*")
#endregion
#region /delitem
@client.tree.command(name = "delitem", description = "Delete an item from the experience.", guild=GUILD)
@app_commands.choices(container = [
    app_commands.Choice(name = "Room", value = 0),
    app_commands.Choice(name = "Player's inventory", value = 1),
    app_commands.Choice(name = "Player's clothes", value = 2),
    app_commands.Choice(name = "Object", value = 3)
    ])
@app_commands.describe(container_name = "The name of the container you wish to delete the item from.")
@app_commands.describe(item_name = "The name of the item you wish to delete.")
@app_commands.describe(object_room_name = "Optional; if the container is an object, specify the room name.")
@app_commands.default_permissions()
async def delitem(interaction: discord.Interaction, container: app_commands.Choice[int], container_name: str, item_name: str, amount: int = 1, object_room_name: str = ''):
    
    ifNone = ''
    containerType = ''
    containerVar = None

    if amount < 1:
        await interaction.response.send_message(f"***{str(amount)}** is an invalid input; please use a positive number greater than one.*")
        return

    if container.value == 0:
        ifNone = f"*Room **{container_name}** could not be found. Please use `/listrooms` to see all current rooms.*"
        containerType = "room"
        containerVar = get_room_from_name(container_name)
    
    elif container.value == 1:
        ifNone = f"*Player **{container_name}** could not be found. Please use `/listplayers` to see all current players.*"
        containerType = "player"
        containerVar = get_player_from_name(container_name)

    elif container.value == 2:
        ifNone = f"*Player **{container_name}** could not be found. Please use `/listplayers` to see all current players.*"
        containerType = "clothes of"
        containerVar = get_player_from_name(container_name)

    elif container.value == 3:

        if object_room_name == '':
            await interaction.response.send_message(f"*To add an item to an object, you must specify the room name as well. Please use `/listrooms` to see all current rooms.*")
            return

        room = get_room_from_name(object_room_name)

        if room is None:
            await interaction.response.send_message(f"*Room **{object_room_name}** could not be found. Please use `/listrooms` to see all current rooms.*")
            return

        for obj in room.get_objects():
            if simplify_string(obj.get_name()) == simplify_string(container_name):
                containerVar = obj

        ifNone = f"*Object **{container_name}** could not be found. Please use `/listobjects` to see the objects in a room.*"
        
        containerType = "object"

    if containerVar is None:
        await interaction.response.send_message(ifNone)
        return

    if container.value == 2:
        itemList = containerVar.get_clothes()    
    else:
        itemList = containerVar.get_items()

    if len(itemList) == 0:
        await interaction.response.send_message("*No items could be found in that container.*")
        return
    
    searchedItem = None
    for item in itemList:
        if simplify_string(item.get_name()) == simplify_string(item_name):
            searchedItem = item

    if searchedItem is None:
        await interaction.response.send_message(f"*Could not find the item **{item_name}**.*")
        return

    if container.value == 2:
        for i in range(amount):
            containerVar.del_clothes(searchedItem)
    else:
        for i in range(amount):
            containerVar.del_item(searchedItem)

    if amount > 1:
        amountStr = f'**{amount}** of the'
    else:
        amountStr = 'the'

    save()
    await interaction.response.send_message(f"*Deleted {amountStr} item **{searchedItem.get_name()}** from the {containerType} **{containerVar.get_name()}**.*")
#endregion
#region /addobject 
@client.tree.command(name = "addobject", description = "Add an object into a room.", guild=GUILD)
@app_commands.describe(room_name = "The room you wish to add the object to.")
@app_commands.describe(object_name = "The name of the object you wish to add to the room.")
@app_commands.describe(is_container = "True or false; whether or not you wish the object to be able to store items.")
@app_commands.describe(is_locked = "True or false; whether or not you wish the object to be locked.")
@app_commands.describe(key_name = "The name of the item you wish to be able lock and unlock the object.")
@app_commands.describe(storage = "The max amount of items you wish to be able to store in the object. If left blank, there will be no maximum.")
@app_commands.describe(desc = "The description of the object you wish to add to the room.")
@app_commands.default_permissions()
async def addobject(interaction: discord.Interaction, room_name: str, object_name: str, is_container: bool, is_locked: bool = False, key_name: str = '', storage: int = -1, desc: str = ''):

    room = get_room_from_name(room_name)

    if room is None:
        await interaction.response.send_message(f"*Room **{room_name}** could not be found. Please use `/listrooms` to see all current rooms.*")
        return
    
    object: Object = Object(object_name, is_container, is_locked, key_name, storage, desc)
    room.add_object(object)

    save()
    await interaction.response.send_message(f"*Added the object **{object_name}** to the room **{room.get_name()}**.*")
#endregion
#region /delobject 
@client.tree.command(name = "delobject", description = "Delete an object in a room.", guild=GUILD)
@app_commands.describe(room_name = "The room you wish to add the object to.")
@app_commands.describe(object_name = "The name of the object you wish to add to the room.")
@app_commands.default_permissions()
async def delobject(interaction: discord.Interaction, room_name: str, object_name: str):

    room = get_room_from_name(room_name)

    if room is None:
        await interaction.response.send_message(f"*Room **{room_name}** could not be found. Please use `/listrooms` to see all current rooms.*")
        return
    
    objList = room.get_objects()

    if len(objList) == 0:
        await interaction.response.send_message("*No objects could be found in that room.*")
        return
    
    searchedObj = None
    for obj in objList:
        if simplify_string(obj.get_name()) == simplify_string(object_name):
            searchedObj = obj
    
    if searchedObj is None:
        await interaction.response.send_message(f"*Could not find the item **{object_name}**. Please use `/objects` in <#{room.get_id()}> to see a list of all the objects in that room.*")
        return

    room.del_object(searchedObj)

    save()
    await interaction.response.send_message(f"*Deleted the object **{searchedObj.get_name()}** from the room **{room.get_name()}**.*")
#endregion
#region /pause
@client.tree.command(name = "pause", description = "Pause all player commands.")
@app_commands.default_permissions()
async def pause(interaction: discord.Interaction):
    for player in playerdata.values():
        player.pause()
    save()
    await interaction.response.send_message("*Game paused.*")
#endregion
#region /pauseplayer
@client.tree.command(name = "pauseplayer", description = "Pause all player commands for a certain player.")
@app_commands.describe(player_name = "The name of the player you wish to pause.")
@app_commands.default_permissions()
async def pauseplayer(interaction: discord.Interaction, player_name: str):
    player = get_player_from_name(player_name) 
    player.pause()
    save()
    await interaction.response.send_message(f"***{player.get_name()}** paused.*")
#endregion
#region /unpause
@client.tree.command(name = "unpause", description = "Unpause all player commands.")
@app_commands.default_permissions()
async def unpause(interaction: discord.Interaction):
    for player in playerdata.values():
        player.unpause()
    save()
    await interaction.response.send_message("*Game unpaused.*")
#endregion
#region /unpauseplayer
@client.tree.command(name = "unpauseplayer", description = "Unpause all player commands for a certain player.")
@app_commands.describe(player_name = "The name of the player you wish to unpause.")
@app_commands.default_permissions()
async def unpauseplayer(interaction: discord.Interaction, player_name: str):
    player = get_player_from_name(player_name) 
    player.unpause()
    save()
    await interaction.response.send_message(f"***{player.get_name()}** unpaused.*")
#endregion
#region /forcetake
@client.tree.command(name = "forcetake", description = "Force a player to take an item from their room.", guild=GUILD)
@app_commands.describe(player_name = "The name of the player you wish to take an item.")
@app_commands.describe(item_name = "The item you wish the player to take.")
@app_commands.describe(amount = "The amount of that item you wish the player to take.")
@app_commands.default_permissions()
async def forcetake(interaction: discord.Interaction, player_name: str, item_name: str, amount: int = 0):
    player = get_player_from_name(player_name)
    currRoom = player.get_room()

    if player == None or not player.get_name() in playerdata.keys():
        await interaction.response.send_message(f"***{player_name}** is not a valid player. Please use `/listplayers` to see a list of all the current players.*.")
        return

    if currRoom is None:
        await interaction.response.send_message(f"***{player_name}** is not currently in a room. Please use `/drag` to bring them into a room first.*.")
        return

    invWeight = player.get_weight()
    itemList = currRoom.get_items()

    if amount == 0 or amount == 1:
        for item in itemList:
            if simplify_string(item_name) == simplify_string(item.get_name()):
                if (invWeight + item.get_weight()) > max_carry_weight:
                    await interaction.response.send_message(f"***{player.get_name()}** tried to take the item **{item_name}**, but they could not fit it into their inventory.*")
                    return
                player.add_item(item)
                currRoom.del_item(item)
                save()
                await interaction.response.send_message(f"***{player.get_name()}** took the item **{item_name}***.")
                return
        await interaction.response.send_message(f"*Could not find the item **{item_name}**. Please use `/listitems` to see a list of items in the player's room.*")
        return

    if amount < 0:
        await interaction.response.send_message(f"***{str(amount)}** is an invalid input; please use a positive number.*")
        return

    if amount != 0 or amount != 1:
        itemsFound = []
        searchedItem = None
        for item in itemList:
            if simplify_string(item_name) == simplify_string(item.get_name()):
                searchedItem = item
                itemsFound.append(item)
        if len(itemsFound) == 0:
            await interaction.response.send_message(f"*Could not find the item **{item_name}**. Please use `/listitems` to see a list of items in the player's room.*")
            return
        if len(itemsFound) < amount:
            await interaction.response.send_message(f"*Could not find **{str(amount)}** of the item **{item_name}**. Please use `/listitems` to see a list of items in the player's room.*")
            return
        try:
            newCarryWeight = 0
            for i in range(amount):
                newCarryWeight += itemsFound[i].get_weight()
            if (invWeight + newCarryWeight) > get_max_carry_weight():
                await interaction.response.send_message(f"***{player.get_name()}** tried to take **{str(amount)}** of the item **{searchedItem.get_name()}**, but they could not fit that much into their inventory.*")
                return
            for i in range(amount):
                player.add_item(itemsFound[i])
                currRoom.del_item(itemsFound[i])
            save()
            await interaction.response.send_message(f"***{player.get_name()}** took **{str(amount)}** of the item **{searchedItem.get_name()}***.")
            return
        except:
            await interaction.response.send_message(f"*Could not find **{str(amount)}** of the item **{item_name}**. Please use `/listitems` to see a list of items in the player's room.*")
            return

    await interaction.response.send_message(f"*Could not find the item **{item_name}**. Please use `/listitems` to see a list of items in the player's room.*")
#endregion
#region /forcedrop
@client.tree.command(name = "forcedrop", description = "Drop an item from a player's inventory into their current room.", guild=GUILD)
@app_commands.describe(player_name = "The name of the player you wish to drop an item.")
@app_commands.describe(item_name = "The item you wish for the player to drop.")
@app_commands.describe(amount = "The amount of that item you wish for the player to drop.")
@app_commands.default_permissions()
async def forcedrop(interaction: discord.Interaction, player_name: str, item_name: str, amount: int = 0):
    player = get_player_from_name(player_name)
    currRoom = player.get_room()

    if player == None or not player.get_name() in playerdata.keys():
        await interaction.response.send_message(f"***{player_name}** is not a valid player. Please use `/listplayers` to see a list of all the current players.*.")
        return

    if currRoom is None:
        await interaction.response.send_message(f"***{player_name}** is not currently in a room. Please use `/drag` to bring them into a room first.*.")
        return

    itemList = player.get_items()

    if amount == 0 or amount == 1:
        for item in itemList:
            if simplify_string(item_name) == simplify_string(item.get_name()):
                player.del_item(item)
                currRoom.add_item(item)
                save()
                await interaction.response.send_message(f"***{player.get_name()}** dropped the item **{item.get_name()}**.*")
                return
        await interaction.response.send_message(f"*Could not find the item **{item_name}**. Please use `/listitems` to see a list of items in a player's inventory.*")
        return

    if amount < 0:
        await interaction.response.send_message(f"***{str(amount)}** is an invalid input; please use a positive number.*")
        return

    if amount != 0 or amount != 1:
        itemsFound = []
        searchedItem = None
        for item in itemList:
            if simplify_string(item_name) == simplify_string(item.get_name()):
                searchedItem = item
                itemsFound.append(item)
        if len(itemsFound) == 0:
            await interaction.response.send_message(f"*Could not find the item **{item_name}**. Please use `/listitems` to see a list of items in a player's inventory.*")
            return
        if len(itemsFound) < amount:
            await interaction.response.send_message(f"*Could not find **{str(amount)}** of the item **{item_name}**. Please use `/listitems` to see a list of items in a player's inventory.*")
            return
        try:
            for i in range(amount):
                player.del_item(itemsFound[i])
                currRoom.add_item(itemsFound[i])
            save()
            await interaction.response.send_message(f"***{player.get_name()}** dropped **{str(amount)}** of the item **{searchedItem.get_name()}**.*")
            return
        except:
            await interaction.response.send_message(f"*Could not find **{str(amount)}** of the item **{item_name}**. Please use `/listitems` to see a list of items in a player's inventory.*")
            return

    await interaction.response.send_message(f"*Could not find the item **{item_name}**. Please use `/listitems` to see a list of items in a player's inventory.*")
#endregion
#region /forcewear
@client.tree.command(name = "forcewear", description = "Make a player wear a clothing item that is currently available to them.", guild=GUILD)
@app_commands.describe(player_name = "The name of the player you wish to wear a clothing item.")
@app_commands.choices(container = [
    app_commands.Choice(name = "From the room", value = 0),
    app_commands.Choice(name = "From the player's inventory", value = 1)
    ])
@app_commands.describe(item_name = "The clothing item you wish for the player to wear.")
@app_commands.default_permissions()
async def forcewear(interaction: discord.Interaction, player_name: str, container: app_commands.Choice[int], item_name: str):
    player = get_player_from_name(player_name)
    currRoom = player.get_room()
    
    midStr = ''
    midStr2 = ''
    containerVar = None

    if container.value == 0:
        containerVar = currRoom
        midStr = 'take and wear'
        midStr2 = 'took and wore'

        if currRoom is None:
            await interaction.response.send_message(f"***{player_name}** is not currently in a room. Please use `/drag` to bring them into a room first.*.")
            return

    elif container.value == 1:
        containerVar = player
        midStr = 'wear'
        midStr2 = 'wore'
    
    if player == None or not player.get_name() in playerdata.keys():
        await interaction.response.send_message(f"***{player_name}** is not a valid player. Please use `/listplayers` to see a list of all the current players.*.")
        return

    clothesWeight = player.get_clothes_weight()
    itemList = containerVar.get_items()
    
    for item in itemList:
        if simplify_string(item_name) == simplify_string(item.get_name()):
            if item.get_wearable_state():
                if (clothesWeight + item.get_weight()) > max_wear_weight:
                    if len(player.get_clothes()) == 0:
                        await interaction.response.send_message(f"***{player.get_name()}** tried to {midStr} the item **{item.get_name()}**, but it was too heavy.*")
                        return    
                    await interaction.response.send_message(f"***{player.get_name()}** tried to {midStr} the item **{item.get_name()}**, but they were wearing too much already.*")
                    return
                player.add_clothes(item)
                containerVar.del_item(item)
                save()
                await interaction.response.send_message(f"***{player.get_name()}** {midStr2} the item **{item.get_name()}**.*")
                return
            else:
                await interaction.response.send_message(f"***{player.get_name()}** tried to {midStr} the item **{item.get_name()}**, but it was not a piece of clothing.*")
                return

    await interaction.response.send_message(f"Could not find the item **{item_name}**. Please use `/listitems` to see a list of items in a container.*")
#endregion
#region /forceundress
@client.tree.command(name = "forceundress", description = "Make a player take off a clothing item they are currently wearing.", guild=GUILD)
@app_commands.describe(player_name = "The name of the player you wish to drop a clothing item.")
@app_commands.choices(container = [
    app_commands.Choice(name = "Drop into the room", value = 0),
    app_commands.Choice(name = "Drop into the player's inventory", value = 1)
    ])
@app_commands.describe(item_name = "The clothing item you wish for a player to drop.")
@app_commands.default_permissions()
async def forceundress(interaction: discord.Interaction, player_name: str, container: app_commands.Choice[int], item_name: str):
    player = get_player_from_name(player_name)
    currRoom = player.get_room()
    
    midStr = ''
    midStr2 = ''
    containerVar = None

    if container.value == 0:
        containerVar = currRoom
        midStr = 'take off and drop'
        midStr2 = 'took off and dropped'

        if currRoom is None:
            await interaction.response.send_message(f"***{player_name}** is not currently in a room. Please use `/drag` to bring them into a room first.*.")
            return

    elif container.value == 1:
        containerVar = player
        midStr = 'take off'
        midStr2 = 'took off'


    if player == None or not player.get_name() in playerdata.keys():
        await interaction.response.send_message(f"***{player_name}** is not a valid player. Please use `/listplayers` to see a list of all the current players.*.")
        return

    if currRoom is None:
        await interaction.response.send_message(f"***{player_name}** is not currently in a room. Please use `/drag` to bring them into a room first.*.")
        return

    itemList = player.get_clothes()

    for item in itemList:
        if simplify_string(item_name) == simplify_string(item.get_name()):
            if item.get_wearable_state():
                if container.value == 1:
                    if (player.get_weight() + item.get_weight()) > max_carry_weight:
                        await interaction.response.send_message(f"***{player.get_name()}** tried to take off **{item.get_name()}**, but they could not fit into their inventory.*")
                        return
                player.del_clothes(item)
                containerVar.add_item(item)
                save()
                await interaction.response.send_message(f"***{player.get_name()}** {midStr2} the item **{item.get_name()}**.*")
                return
            else:
                await interaction.response.send_message(f"***{player.get_name()}** tried to {midStr} **{item.get_name()}**, but it was not a piece of clothing... how are they wearing it?*")
                return


    await interaction.response.send_message(f"*Could not find **{item_name}**. Please use `/listclothes` to see the clothes a player is wearing.*")
#endregion
#region /listitems
@client.tree.command(name = "listitems", description = "List the items in a container.")
@app_commands.choices(container = [
    app_commands.Choice(name = "Room", value = 0),
    app_commands.Choice(name = "Player's inventory", value = 1),
    app_commands.Choice(name = "Player's clothes", value = 2),
    app_commands.Choice(name = "Object", value = 3)
    ])
@app_commands.describe(container_name = "The name of the container you wish to add the item to.")
@app_commands.describe(object_room_name = "Optional; if the container is an object, specify the room name.")
@app_commands.default_permissions()
async def listitems(interaction: discord.Interaction, container: app_commands.Choice[int], container_name: str, object_room_name: str = ''):

    endMsg = ''
    containerVar = None
    if container.value == 0:
        containerVar = get_room_from_name(container_name)

        if containerVar is None:
            await interaction.response.send_message(f"*Room **{container_name}** could not be found. Please use `/listrooms` to see a list of all current rooms.*")
            return

        endMsg = f"the room **{containerVar.get_name()}**"

    elif container.value == 1:
        containerVar = get_player_from_name(container_name)

        if containerVar is None:
            await interaction.response.send_message(f"*Player **{container_name}** could not be found. Please use `/listplayers` to see a list of all current players.*")
            return

        endMsg = f"**{containerVar.get_name()}**'s inventory"

    
    elif container.value == 2:
        containerVar = get_player_from_name(container_name)

        if containerVar is None:
            await interaction.response.send_message(f"*Player **{container_name}** could not be found. Please use `/listplayers` to see a list of all current players.*")
            return

        endMsg = f"**{containerVar.get_name()}**'s clothes"        


    elif container.value == 3:

        if object_room_name == '':
            await interaction.response.send_message(f"*To look inside of an object, you must specify the room name as well. Please use `/listrooms` to see all current rooms.*")
            return

        room = get_room_from_name(object_room_name)

        if room is None:
            await interaction.response.send_message(f"*Room **{object_room_name}** could not be found. Please use `/listrooms` to see all current rooms.*")
            return

        for obj in room.get_objects():
            if simplify_string(obj.get_name()) == simplify_string(container_name):
                containerVar = obj

        if containerVar is None:
            await interaction.response.send_message(f"*Object **{container_name}** could not be found. Please use `/listobjects` to see the objects in a room.*")
            return
        
        endMsg = f"the object **{containerVar.get_name()}** in the room **{room.get_name()}**"

    if container.value == 2:
        itemList = containerVar.get_clothes()
    else:
        itemList = containerVar.get_items()
    
    if len(itemList) == 0:
        await interaction.response.send_message(f"*Looked inside of {endMsg}:*\n\n`No items found.`")
        return

    itemNames = []
    for item in itemList:
        itemNames.append("`" + item.get_name() + "`")

    allItems = ', '.join(itemNames)

    await interaction.response.send_message(f"*Looked inside of {endMsg}:*\n\n{allItems}")
#endregion
#region /listexits
@client.tree.command(name = "listexits", description = "List all locations that are connected to a room.")
@app_commands.describe(room_name = "The name of the room you wish to see the exits of.")
@app_commands.default_permissions()
async def exits(interaction: discord.Interaction, room_name: str):
    currRoom = get_room_from_name(room_name)

    if currRoom is None:
        await interaction.response.send_message(f"*Could not find the room **{room_name}**. Please use `/listrooms` to see a list of all current rooms.*")
        return
    
    exits = currRoom.get_exits()

    if len(exits) == 0:
        await interaction.response.send_message(f"*Looked at the exits in the room **{currRoom.get_name()}**:*\n\n`No exits found.`")
        return
    
    exitNames = []
    for exit in exits:
        currExit = ''
        if exit.get_room1() == currRoom.get_name():
            currExit = exit.get_room2()
        else:
            currExit = exit.get_room1()
        exitNames.append("`" + currExit + "`")
    
    allExits = ', '.join(exitNames)
    await interaction.response.send_message(f"*Looked at the exits in the room **{currRoom.get_name()}**:*\n\n{allExits}")

#endregion
#region /listobjects
@client.tree.command(name = "listobjects", description = "List all of the objects in a room.", guild=GUILD)
@app_commands.describe(room_name = "The room that you wish to see the objects of.")
@app_commands.default_permissions()
async def listobjects(interaction: discord.Interaction, room_name: str):
    currRoom = get_room_from_name(room_name)

    if currRoom is None:
        await interaction.response.send_message(f"*Could not find the room **{room_name}**. Please use `/listrooms` to see a list of all current rooms.*")
        return

    objList = currRoom.get_objects()
    
    objNames = []
    for obj in objList:
        objNames.append("`" + obj.get_name() + "`")

    allObjs = ', '.join(objNames)

    if len(objList) == 0:
            await interaction.response.send_message(f"*Looked at the objects in the room **{currRoom.get_name()}**:*\n\n`No objects found.`")
            return
    await interaction.response.send_message(f"*Looked at the objects in the room **{currRoom.get_name()}**:*\n\n{allObjs}")
#endregion
#region /seeitem
@client.tree.command(name = "seeitem", description = "Get the description of a specific item.", guild=GUILD)
@app_commands.choices(container = [
    app_commands.Choice(name = "Room", value = 0),
    app_commands.Choice(name = "Player's inventory", value = 1),
    app_commands.Choice(name = "Player's clothes", value = 2),
    app_commands.Choice(name = "Object", value = 3)
    ])
@app_commands.describe(container_name = "The name of the container you wish to look inside of.")
@app_commands.describe(item_name = "The name of the item you wish to look at.")
@app_commands.describe(object_room_name = "Optional; if the container is an object, specify the room name.")
@app_commands.default_permissions()
async def seeitem(interaction: discord.Interaction, container: app_commands.Choice[int], container_name: str, item_name: str, object_room_name: str = ''):
    
    endMsg = ''
    containerVar = None
    if container.value == 0:
        containerVar = get_room_from_name(container_name)

        if containerVar is None:
            await interaction.response.send_message(f"*Room **{container_name}** could not be found. Please use `/listrooms` to see a list of all current rooms.*")
            return

        endMsg = f"the room **{containerVar.get_name()}**"

    elif container.value == 1:
        containerVar = get_player_from_name(container_name)

        if containerVar is None:
            await interaction.response.send_message(f"*Player **{container_name}** could not be found. Please use `/listplayers` to see a list of all current players.*")
            return

        endMsg = f"**{containerVar.get_name()}**'s inventory"

    
    elif container.value == 2:
        containerVar = get_player_from_name(container_name)

        if containerVar is None:
            await interaction.response.send_message(f"*Player **{container_name}** could not be found. Please use `/listplayers` to see a list of all current players.*")
            return

        endMsg = f"**{containerVar.get_name()}**'s clothes"        


    elif container.value == 3:

        if object_room_name == '':
            await interaction.response.send_message(f"*To look inside of an object, you must specify the room name as well. Please use `/listrooms` to see all current rooms.*")
            return

        room = get_room_from_name(object_room_name)

        if room is None:
            await interaction.response.send_message(f"*Room **{object_room_name}** could not be found. Please use `/listrooms` to see all current rooms.*")
            return

        for obj in room.get_objects():
            if simplify_string(obj.get_name()) == simplify_string(container_name):
                containerVar = obj

        if containerVar is None:
            await interaction.response.send_message(f"*Object **{container_name}** could not be found. Please use `/listobjects` to see the objects in a room.*")
            return
        
        endMsg = f"the object **{containerVar.get_name()}** in the room **{room.get_name()}**"

    if container.value == 2:
        itemList = containerVar.get_clothes()
    else:
        itemList = containerVar.get_items()
    
    searchedItem = None
    for item in itemList:
        if simplify_string(item.get_name()) == simplify_string(item_name):
            searchedItem = item
    
    if searchedItem is None:
        await interaction.response.send_message(f"*Could not find the item **{item_name}** in {endMsg}.*")
        return
    
    if searchedItem.get_desc() == '':
        await interaction.response.send_message(f"*Looked at the item **{searchedItem.get_name()}**:*\n\n__`{searchedItem.get_name()}`__\n\n__`Weight`__: `{str(searchedItem.get_weight())}`\n__`Wearable`__: `{str(searchedItem.get_wearable_state())}`\n\nItem has no description.")
        return

    await interaction.response.send_message(f"*Looked at the item **{searchedItem.get_name()}**:*\n\n__`{searchedItem.get_name()}`__\n\n__`Weight`__: `{str(searchedItem.get_weight())}`\n__`Wearable`__: `{str(searchedItem.get_wearable_state())}`\n\n{searchedItem.get_desc()}")
#endregion
#region /seeobject
@client.tree.command(name = "seeobject", description = "Get the description of a specific object from anywhere.", guild=GUILD)
@app_commands.describe(room_name = "The room of the object you wish to look at.")
@app_commands.describe(object_name = "The name of the object you wish to look at.")
@app_commands.default_permissions()
async def seeobject(interaction: discord.Interaction, room_name: str, object_name: str):
    currRoom = get_room_from_name(room_name)

    if currRoom is None:
        await interaction.response.send_message(f"*Room **{room_name}** could not be found. Please use `/listrooms` to see a list of all current rooms.*")
        return
    
    objList = currRoom.get_objects()

    if len(objList) == 0:
        await interaction.response.send_message("*No objects could be found in the room.*")
        return
    
    searchedObj = None
    for obj in objList:
        if simplify_string(obj.get_name()) == simplify_string(object_name):
            searchedObj = obj
    
    if searchedObj is None:
        await interaction.response.send_message(f"*Could not find the item **{object_name}**. Please use `/objects` to see a list of all the objects in the current room.*")
        return
    
    is_locked = ''
    if searchedObj.get_locked_state():
        is_locked = 'Locked'
    else:
        is_locked = 'Opened'

    storage_amt = ''
    if searchedObj.get_storage() == -1:
        storage_amt = 'Infinite'
    else:
        storage_amt = str(searchedObj.get_storage())

    keyName = str(searchedObj.get_key_name())
    if keyName == '':
        keyName = "None"

    if searchedObj.get_desc() == '':
        await interaction.response.send_message(f"*Looked at the object **{searchedObj.get_name()}**:*\n\n__`{searchedObj.get_name()}`__\n\n__`Storage`__: `{str(storage_amt)}`\n__`State`__: `{is_locked}`\n__`Key Name`__: `{keyName}`\n\n`Object has no description.`")
        return
    await interaction.response.send_message(f"*Looked at the object **{searchedObj.get_name()}**:*\n\n__`{searchedObj.get_name()}`__\n\n__`Storage`__: `{str(storage_amt)}`\n__`State`__: `{is_locked}`\n__`Key Name`__: `{keyName}`\n\n{searchedObj.get_desc()}")
    return
#endregion
#region /seeexit
@client.tree.command(name = "seeexit", description = "Get the locked state of any exit.")
@app_commands.describe(room_one_name = "The first room of the exit.")
@app_commands.describe(room_two_name = "The second room of the exit.")
@app_commands.default_permissions()
async def seeexit(interaction: discord.Interaction, room_one_name: str, room_two_name: str):
    room_one = get_room_from_name(room_one_name)
    room_two = get_room_from_name(room_two_name)

    if room_one is None:
        await interaction.response.send_message(f"*Could not find the room **{room_one_name}**. Please use `/listrooms` to see a list of all current rooms.")
        return
    
    if room_two is None:
        await interaction.response.send_message(f"*Could not find the room **{room_two_name}**. Please use `/listrooms` to see a list of all current rooms.")
        return
    
    exitsOne = room_one.get_exits()
    exitsTwo = room_two.get_exits()

    if len(exitsOne) == 0:
        await interaction.response.send_message(f"*There are no exits in the room **{str(room_one.get_name())}**.*")
        return
    if len(exitsTwo) == 0:
        await interaction.response.send_message(f"*There are no exits in the room **{str(room_two.get_name())}**.*")
        return

    exit = None
    for exit in exitsOne:
        if exit.get_room1() == room_one.get_name():
            if simplify_string(exit.get_room2()) == simplify_string(room_one_name):
                exit = exit
        else:
            if simplify_string(exit.get_room1()) == simplify_string(room_one_name):
                exit = exit

    isLocked = ''
    if exit.get_locked_state():
        isLocked = 'locked'
    else:
        isLocked = 'opened'

    if exit.get_key_name() == '':
        hasKey = "has no key"
    else:
        hasKey = (f"can be locked or unlocked using the key **{exit.get_key_name()}**")

    await interaction.response.send_message(f"*The connection between **{room_one.get_name()}** and **{room_two.get_name()}** is **{isLocked}** and {hasKey}.*")
#endregion
#region /editplayer
@client.tree.command(name = "editplayer", description = "Edit the value of a player.")
@app_commands.describe(player_name = "The player you wish to edit.")
@app_commands.describe(new_name = "The new name you wish to give the player.")
@app_commands.describe(new_desc = "The new description you wish to give the player.")
@app_commands.default_permissions()
async def editplayer(interaction: discord.Interaction, player_name: str, new_name: str = '', new_desc: str = ''):
    player = get_player_from_name(player_name)

    if player is None:
        await interaction.response.send_message(f"*Could not find the player **{player_name}**. Please use `/listplayers` to get a list of all current players.*")

    player_id = player.get_id()
    
    edited = ''

    if new_name != '':
        old_name = player.get_name()
        player.edit_name(new_name)
        playerdata[new_name] = playerdata[old_name]
        del playerdata[old_name]
        edited = edited + f" name to **{new_name}**"
    if new_desc != '':
        player.edit_desc(new_desc)
        if edited == '':
            edited = edited + ' description'
        else:
            edited = edited + ' and edited their description'
    
    edited = edited + "."
    
    if new_name == '' and new_desc == '':
        await interaction.response.send_message(f"*Please enter a value for either `new_name` or `new_desc` to edit the player **{player.get_name}**.*")
        return

    save()
    await interaction.response.send_message(f"*Changed <@{player_id}>'s player{edited}*")
#endregion
#region /editroom
@client.tree.command(name = "editroom", description = "Edit the value of a room.")
@app_commands.describe(room_name = "The room you wish to edit.")
@app_commands.describe(new_name = "The new name you wish to give the room.")
@app_commands.describe(new_desc = "The new description you wish to give the room.")
@app_commands.default_permissions()
async def editroom(interaction: discord.Interaction, room_name: str, new_name: str = '', new_desc: str = ''):
    room = get_room_from_name(room_name)
    
    if room is None:
        await interaction.response.send_message(f"*Could not find the room **{room_name}**. Please use `/listrooms` to get a list of the current rooms.*")
        return

    room_id = room.get_id()
    
    edited = ''

    if new_name != '':
        old_name = room.get_name()
        exits = room.get_exits()
        for exit in exits:
            if exit.get_room1() == room.get_name():
                exit.edit_room1(new_name)
            elif exit.get_room2() == room.get_name():
                exit.edit_room2(new_name)
        room.edit_name(new_name)
        roomdata[new_name] = roomdata[old_name]
        del roomdata[old_name]
        edited = edited + f" name to **{new_name}**"
    if new_desc != '':
        room.edit_desc(new_desc)
        channel = client.get_channel(int(room_id))
        await channel.edit(topic=new_desc)
        if edited == '':
            edited = edited + ' description'
        else:
            edited = edited + ' and edited its description'
    
    edited = edited + "."

    if new_name == '' and new_desc == '':
        await interaction.response.send_message(f"*Please enter a value for either `new_name` or `new_desc` to edit the room **{room.get_name}**.*")
        return

    save()
    await interaction.response.send_message(f"*Changed <#{room_id}>'s room{edited}*")
#endregion
#region /edititem
@client.tree.command(name = "edititem", description = "Edit the value of an item.", guild=GUILD)
@app_commands.choices(container = [
    app_commands.Choice(name = "Room", value = 0),
    app_commands.Choice(name = "Player's inventory", value = 1),
    app_commands.Choice(name = "Player's clothes", value = 2),
    app_commands.Choice(name = "Object", value = 3)
    ])
@app_commands.describe(container_name = "The name of the container the item is in.")
@app_commands.describe(item_name = "The name of the item you wish to edit.")
@app_commands.describe(object_room_name = "Optional; if the container is an object, specify the room name.")
@app_commands.describe(new_name = "The new name of the item.")
@app_commands.describe(new_desc = "The new description of the item.")
@app_commands.describe(is_wearable = "Whether you would like the item to be wearable.")
@app_commands.describe(new_weight = "The new weight of the item.")
@app_commands.default_permissions()
async def edititem(interaction: discord.Interaction, container: app_commands.Choice[int], container_name: str, item_name: str, object_room_name: str = '', new_name:str = '', new_desc: str = '', is_wearable: bool = None, new_weight: float = -1.0):
    
    endMsg = ''
    containerVar = None
    if container.value == 0:
        containerVar = get_room_from_name(container_name)

        if containerVar is None:
            await interaction.response.send_message(f"*Room **{container_name}** could not be found. Please use `/listrooms` to see a list of all current rooms.*")
            return

        endMsg = f"the room **{containerVar.get_name()}**"

    elif container.value == 1:
        containerVar = get_player_from_name(container_name)

        if containerVar is None:
            await interaction.response.send_message(f"*Player **{container_name}** could not be found. Please use `/listplayers` to see a list of all current players.*")
            return

        endMsg = f"**{containerVar.get_name()}**'s inventory"

    
    elif container.value == 2:
        containerVar = get_player_from_name(container_name)

        if containerVar is None:
            await interaction.response.send_message(f"*Player **{container_name}** could not be found. Please use `/listplayers` to see a list of all current players.*")
            return

        endMsg = f"**{containerVar.get_name()}**'s clothes"        


    elif container.value == 3:

        if object_room_name == '':
            await interaction.response.send_message(f"*To edit an item inside of an object, you must specify the room name as well. Please use `/listrooms` to see all current rooms.*")
            return

        room = get_room_from_name(object_room_name)

        if room is None:
            await interaction.response.send_message(f"*Room **{object_room_name}** could not be found. Please use `/listrooms` to see all current rooms.*")
            return

        for obj in room.get_objects():
            if simplify_string(obj.get_name()) == simplify_string(container_name):
                containerVar = obj

        if containerVar is None:
            await interaction.response.send_message(f"*Object **{container_name}** could not be found. Please use `/listobjects` to see the objects in a room.*")
            return
        
        endMsg = f"the object **{containerVar.get_name()}** in the room **{room.get_name()}**"

    if container.value == 2:
        itemList = containerVar.get_clothes()
    else:
        itemList = containerVar.get_items()
    
    searchedItem = None
    for item in itemList:
        if simplify_string(item.get_name()) == simplify_string(item_name):
            searchedItem = item
    
    if searchedItem is None:
        await interaction.response.send_message(f"*Could not find the item **{item_name}** in {endMsg}.*")
        return
    

    strs = []
    if new_name != '':
        searchedItem.edit_name(new_name)
        nameStr = 'name'
        strs.append(nameStr)
    if new_desc != '':
        searchedItem.edit_desc(new_desc)
        descStr = 'description'
        strs.append(descStr)
    if is_wearable != None:
        searchedItem.switch_wearable_state(is_wearable)
        wearStr = 'wearable state'
        strs.append(wearStr)
    if new_weight != -1:
        searchedItem.edit_weight(new_weight)
        weightStr = 'weight'
        strs.append(weightStr)

    if new_name == '' and new_desc == '' and is_wearable == None and new_weight == -1:
        await interaction.response.send_message(f"*Please select an option and enter a new value to edit the item **{searchedItem.get_name}**.*")
        return

    edited = ''
    if len(strs) == 0:
        edited = ''
    elif len(strs) == 1:
        edited = strs[0]
    elif len(strs) == 2:
        edited = strs[0] + " and " + strs[1]
    else:
        edited = ", ".join(strs[:-1]) + f", and {strs[-1]}"

    save()
    await interaction.response.send_message(f"*Changed the item **{searchedItem.get_name()}**'s {edited}.*")
#endregion
#region /editexit
@client.tree.command(name = "editexit", description = "Edit the value of an exit.")
@app_commands.describe(room_one_name = "The first room of the exit.")
@app_commands.describe(room_two_name = "The second room of the exit.")
@app_commands.describe(new_locked_state = "The new locked state of the exit.")
@app_commands.describe(new_key = "The new key for the exit.")
@app_commands.default_permissions()
async def editexit(interaction: discord.Interaction, room_one_name: str, room_two_name: str, new_locked_state: bool = None, new_key: str = ''):
    room_one = get_room_from_name(room_one_name)
    room_two = get_room_from_name(room_two_name)

    if room_one is None:
        await interaction.response.send_message(f"*Could not find the room **{room_one_name}**. Please use `/listrooms` to see a list of all current rooms.")
        return
    
    if room_two is None:
        await interaction.response.send_message(f"*Could not find the room **{room_two_name}**. Please use `/listrooms` to see a list of all current rooms.")
        return
    
    exitsOne = room_one.get_exits()
    exitsTwo = room_two.get_exits()

    if len(exitsOne) == 0:
        await interaction.response.send_message(f"*There are no exits in the room **{str(room_one.get_name())}**.*")
        return
    if len(exitsTwo) == 0:
        await interaction.response.send_message(f"*There are no exits in the room **{str(room_two.get_name())}**.*")
        return

    exit = None
    for exit in exitsOne:
        if exit.get_room1() == room_one.get_name():
            if simplify_string(exit.get_room2()) == simplify_string(room_one_name):
                exit = exit
        else:
            if simplify_string(exit.get_room1()) == simplify_string(room_one_name):
                exit = exit

    if new_locked_state == None and new_key == '':
        await interaction.response.send_message(f"*Please select an option and enter a new value to edit an exit.*")
        return

    strs = []
    if new_locked_state != None:
        exit.switch_locked_state(new_locked_state)
        strs.append("locked state")
    if new_key != '':
        exit.edit_key_name(new_key)
        strs.append("key name")
    
    edited = ''
    if len(strs) == 0:
        edited = ''
    elif len(strs) == 1:
        edited = strs[0]
    else:
        edited = strs[0] + " and " + strs[1]

    save()
    await interaction.response.send_message(f"*Changed the exit between **{room_one.get_name()}** and **{room_two.get_name()}**'s {edited}.*")
#endregion
#region /editobject
@client.tree.command(name = "editobject", description = "Edit the value of an object.", guild=GUILD)
@app_commands.describe(room_name = "The room of the object you wish to edit.")
@app_commands.describe(object_name = "The name of the object you wish to edit.")
@app_commands.describe(new_name = "The new name of the object.")
@app_commands.describe(new_desc = "The new description of the object.")
@app_commands.describe(new_container_state = "Whether the object is a container or not.")
@app_commands.describe(new_locked_state = "Whether the object is locked or not.")
@app_commands.describe(new_key = "The name of the key for the object.")
@app_commands.describe(new_storage = "The new amount of items that can fit into the object. If infinite, input -1.")
@app_commands.default_permissions()
async def editobject(interaction: discord.Interaction, room_name: str, object_name: str, new_name: str = '', new_desc: str = '', new_container_state: bool = None, new_locked_state: bool = None, new_key: str = '', new_storage: int = -2):
    currRoom = get_room_from_name(room_name)

    if new_storage <= -3:
        await interaction.response.send_message((f"***{str(new_storage)}** is an invalid storage input; please use a positive number or -1 for infinity.*"))
        return

    if currRoom is None:
        await interaction.response.send_message("*You are not currently in a room. Please contact an admin if you believe this is a mistake.*")
        return
    
    objList = currRoom.get_objects()

    if len(objList) == 0:
        await interaction.response.send_message("*No objects could be found in the room.*")
        return
    
    searchedObj = None
    for obj in objList:
        if simplify_string(obj.get_name()) == simplify_string(object_name):
            searchedObj = obj
    
    if searchedObj is None:
        await interaction.response.send_message(f"*Could not find the item **{object_name}**. Please use `/objects` to see a list of all the objects in the current room.*")
        return
    
    if new_name == '' and new_desc == '' and new_container_state == None and new_locked_state == None and new_key == '' and new_storage == -2:
        await interaction.response.send_message(f"*Please select an option and enter a new value to edit an exit.*")
        return
    
    str = []
    if new_name != '':
        searchedObj.edit_name(new_name)
        str.append("name")
    if new_desc != '':
        searchedObj.edit_desc(new_desc)
        str.append("description")
    if new_container_state != None:
        searchedObj.switch_container_state(new_container_state)
        str.append("container state")
    if new_locked_state != None:
        searchedObj.switch_locked_state(new_locked_state)
        str.append("locked state")
    if new_key != '':
        searchedObj.edit_key_name(new_key)
        str.append("key name")
    if new_storage != -2:
        searchedObj.set_storage(new_storage)
        str.append("storage")
    
    edited = ''
    if len(str) == 0:
        edited = ''
    elif len(str) == 1:
        edited = str[0]
    elif len(str) == 2:
        edited = str[0] + " and " + str[1]
    else:
        edited = ", ".join(str[:-1]) + f", and {str[-1]}"

    save()
    await interaction.response.send_message(f"*Changed the object **{searchedObj.get_name()}**'s {edited}.*")
#endregion
#region /adminhelp
@client.tree.command(name = "adminhelp", description = "Gives descriptions of every admin command.")
@app_commands.default_permissions()
async def help(interaction: discord.Interaction):
    emby = discord.Embed(description=adminhelp1)
    await interaction.response.send_message(embed=emby, view = AdminHelp(), ephemeral=True)
#endregion
#endregion

client.run(os.getenv('token'))