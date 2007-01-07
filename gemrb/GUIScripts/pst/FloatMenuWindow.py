# -*-python-*-
# GemRB - Infinity Engine Emulator
# Copyright (C) 2003 The GemRB Project
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# $Header: /data/gemrb/cvs2svn/gemrb/gemrb/gemrb/GUIScripts/pst/FloatMenuWindow.py,v 1.13 2007/01/07 16:19:17 avenger_teambg Exp $

# FloatMenuWindow.py - display PST's floating menu window from GUIWORLD winpack

###################################################

import GemRB
from GUIDefines import *
from GUICommonWindows import GetActorPortrait, SetSelectionChangeMultiHandler
from ie_stats import *

FloatMenuWindow = None

MENU_MODE_SINGLE = 0
MENU_MODE_GROUP = 1
MENU_MODE_WEAPONS = 2
MENU_MODE_ITEMS = 3
MENU_MODE_SPELLS = 4
MENU_MODE_ABILITIES = 5

float_menu_mode = MENU_MODE_SINGLE
float_menu_index = 0


def OpenFloatMenuWindow ():
	global FloatMenuWindow
	global float_menu_mode, float_menu_index
	
	GemRB.HideGUI ()

	if FloatMenuWindow:
		GemRB.UnloadWindow (FloatMenuWindow)
		FloatMenuWindow = None

		#FIXME: UnpauseGameTimer
		GemRB.GamePause (False, 0)
		GemRB.SetVar ("FloatWindow", -1)
		SetSelectionChangeMultiHandler (None)
		GemRB.UnhideGUI ()
		return


	if not GemRB.GameGetFirstSelectedPC ():
		GemRB.UnhideGUI ()
		return
	# FIXME: remember current selection
	#FIXME: PauseGameTimer
	GemRB.GamePause (True, 0)

	GemRB.LoadWindowPack ("GUIWORLD")
	FloatMenuWindow = Window = GemRB.LoadWindow (3)
	GemRB.SetVar ("FloatWindow", Window)

	x, y = GemRB.GetVar ("MenuX"), GemRB.GetVar ("MenuY")

	# FIXME: keep the menu inside the viewport!!!
	GemRB.SetWindowPos (Window, x, y, WINDOW_CENTER | WINDOW_BOUNDED)

	# portrait button
	Button = GemRB.GetControl (Window, 0)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "FloatMenuSelectNextPC")
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_RIGHT_PRESS, "OpenFloatMenuWindow")

	# Initiate Dialogue
	Button = GemRB.GetControl (Window, 1)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "FloatMenuSelectDialog")
	GemRB.SetTooltip (Window, Button, 8191)

	# Attack/Select Weapon
	Button = GemRB.GetControl (Window, 2)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "FloatMenuSelectWeapons")
	GemRB.SetTooltip (Window, Button, 8192)

	# Cast spell
	Button = GemRB.GetControl (Window, 3)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "FloatMenuSelectSpells")
	GemRB.SetTooltip (Window, Button, 8193)

	# Use Item
	Button = GemRB.GetControl (Window, 4)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "FloatMenuSelectItems")
	GemRB.SetTooltip (Window, Button, 8194)

	# Use Special Ability
	Button = GemRB.GetControl (Window, 5)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "FloatMenuSelectAbilities")
	GemRB.SetTooltip (Window, Button, 8195)

	# Menu Anchors/Handles
	Button = GemRB.GetControl (Window, 11)
	GemRB.SetTooltip (Window, Button, 8199)
	GemRB.SetButtonFlags (Window, Button, IE_GUI_BUTTON_DRAGGABLE, OP_OR)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_DRAG, "FloatMenuDrag")
	
	Button = GemRB.GetControl (Window, 12)
	GemRB.SetTooltip (Window, Button, 8199)
	GemRB.SetButtonFlags (Window, Button, IE_GUI_BUTTON_DRAGGABLE, OP_OR)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_DRAG, "FloatMenuDrag")

	# Rotate Items left (to begin)
	Button = GemRB.GetControl (Window, 13)
	GemRB.SetTooltip (Window, Button, 8197)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "FloatMenuPreviousItem")

	# Rotate Items right (to end)
	Button = GemRB.GetControl (Window, 14)
	GemRB.SetTooltip (Window, Button, 8198)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "FloatMenuNextItem")

	# 6 - 10 - items/spells/other
	for i in range (6, 11):
		Button = GemRB.GetControl (Window, i)
		GemRB.SetControlPos (Window, Button, 65535, 65535)

	# 15 - 19 - empty item slot
	for i in range (15, 20):
		Button = GemRB.GetControl (Window, i)
		GemRB.SetButtonFlags (Window, Button, IE_GUI_BUTTON_ALIGN_RIGHT | IE_GUI_BUTTON_ALIGN_BOTTOM, OP_OR)
		#GemRB.SetButtonFont (Window, Button, 'NUMBER')
		#GemRB.SetVarAssoc (Window, Button, 'ItemButton', i)


	# BAMs:
	# AMALLSTP - 41655
	# AMATTCK - 41654
	#AMGENB1
	#AMGENS
	#AMGUARD - 31657, 32431, 41652, 48887
	#AMHILITE - highlight frame
	#AMINVNT - 41601, 41709
	#AMJRNL - 41623, 41714
	#AMMAP - 41625, 41710
	#AMSPLL - 4709
	#AMSTAT - 4707
	#AMTLK - 41653
	
	#AMPANN
	#AMPDKK
	#AMPFFG
	#AMPIGY
	#AMPMRT
	#AMPNDM
	#AMPNM1
	#AMPVHA

	num = 0
	for i in range (GemRB.GetPartySize ()):
		if GemRB.GameIsPCSelected (i + 1):
			num = num + 1

	# if more than one is selected, start in group menu mode (mode 1)
	if num == 1:
		float_menu_mode = MENU_MODE_SINGLE
	else:
		float_menu_mode = MENU_MODE_GROUP

	float_menu_index = 0

	SetSelectionChangeMultiHandler (FloatMenuSelectAnotherPC)
	UpdateFloatMenuWindow ()
	
	GemRB.UnhideGUI ()


def UpdateFloatMenuWindow ():
	Window = FloatMenuWindow
	
	pc = GemRB.GameGetFirstSelectedPC ()

	Button = GemRB.GetControl (Window, 0)
	#GemRB.SetButtonFlags(Window, Button, IE_GUI_BUTTON_NO_IMAGE | IE_GUI_BUTTON_PICTURE, OP_SET)
	GemRB.SetButtonSprites (Window, Button, GetActorPortrait (pc, 'FMENU'), 0, 0, 1, 2, 3)

	if float_menu_mode == MENU_MODE_SINGLE:
		for i in range (5):
			UpdateFloatMenuSingleAction (i)
	elif float_menu_mode == MENU_MODE_GROUP:
		for i in range (5):
			UpdateFloatMenuGroupAction (i)
	elif float_menu_mode == MENU_MODE_WEAPONS:
		# weapons
		for i in range (5):
			UpdateFloatMenuItem (pc, i, 1)
	elif float_menu_mode == MENU_MODE_ITEMS:
		# items
		for i in range (5):
			UpdateFloatMenuItem (pc, i, 0)
	elif float_menu_mode == MENU_MODE_SPELLS:
		for i in range (5):
			UpdateFloatMenuSpell (pc, i, False)
	elif float_menu_mode == MENU_MODE_ABILITIES:
		for i in range (5):
			UpdateFloatMenuSpell (pc, i, True)

def UpdateFloatMenuSingleAction (i):
	Window = FloatMenuWindow
	butts = [ ('AMMAP', 41625, ''),
		  ('AMJRNL', 41623, ''),
		  ('AMINVNT', 41601, ''),
		  ('AMSTAT', 4707, ''),
		  ('AMSPLL', 4709, '') ]  # or 41624
	# Map Screen
	# Journal Screen
	# Inventory screen
	# Statistics screen
	# Mage Spell Book / Priest Scroll
	
	Button = GemRB.GetControl (Window, 15 + i)

	GemRB.SetButtonSprites (Window, Button, butts[i][0], 0, 0, 1, 2, 3)
	GemRB.SetTooltip (Window, Button, butts[i][1])
	GemRB.SetText (Window, Button, '')


def UpdateFloatMenuGroupAction (i):
	Window = FloatMenuWindow
	butts = [ ('AMGUARD', 31657, ''),
		  ('AMTLK', 41653, ''),
		  ('AMATTCK', 41654, ''),
		  ('AMALLSTP', 41655, ''),
		  ('AMGENS', '', '') ]
	# Guard
	# Initiate dialogue
	# Attack
	# Abort Current Action
	Button = GemRB.GetControl (Window, 15 + i)

	GemRB.SetButtonSprites (Window, Button, butts[i][0], 0, 0, 1, 2, 3)
	GemRB.SetTooltip (Window, Button, butts[i][1])
	GemRB.SetText (Window, Button, '')


def UpdateFloatMenuItem (pc, i, weapons):
	Window = FloatMenuWindow
	if weapons:
		slot_item = GemRB.GetSlotItem (pc, 9 + i + float_menu_index)
	else:
		slot_item = GemRB.GetSlotItem (pc, 20 + i + float_menu_index)
	Button = GemRB.GetControl (Window, 15 + i)
	GemRB.SetButtonSprites (Window, Button, 'AMGENS', 0, 0, 1, 2, 3)

	# Weapons - the last action is 'Guard'
	
	#if slot_item and slottype:
	if slot_item:
		item = GemRB.GetItem (slot_item['ItemResRef'])
		identified = slot_item['Flags'] & IE_INV_ITEM_IDENTIFIED


		#GemRB.SetButtonSprites (Window, Button, 'IVSLOT', 0,  0, 0, 0, 0)
		GemRB.SetItemIcon (Window, Button, slot_item['ItemResRef'])
		if item['StackAmount'] > 1:
			GemRB.SetText (Window, Button, str (slot_item['Usages0']))
		else:
			GemRB.SetText (Window, Button, '')
		if not identified or item['ItemNameIdentified'] == -1:
			GemRB.SetTooltip (Window, Button, item['ItemName'])
		else:
			GemRB.SetTooltip (Window, Button, item['ItemNameIdentified'])
		GemRB.SetButtonFlags (Window, Button, IE_GUI_BUTTON_NO_IMAGE, OP_NAND)
	else:

		GemRB.SetItemIcon (Window, Button, '')
		GemRB.SetText (Window, Button, '')
		GemRB.SetTooltip (Window, Button, '')


def UpdateFloatMenuSpell (pc, i, innate):
	Window = FloatMenuWindow
	if innate:
		type = IE_SPELL_TYPE_INNATE
	else:
		Table = GemRB.LoadTable ("clskills")
		if (GemRB.GetTableValue (Table, GemRB.GetPlayerStat( pc, IE_CLASS), 1)=="*"):
			type = IE_SPELL_TYPE_WIZARD
		else:
			type = IE_SPELL_TYPE_PRIEST

	# FIXME: ugly, should be in Spellbook.cpp
	spell_hash = {}
	spell_list = []
	for level in range (1, 10):
		mem_cnt = GemRB.GetMemorizedSpellsCount (pc, type, level)
		for j in range (mem_cnt):
			ms = GemRB.GetMemorizedSpell (pc, type, level, j)

			# Spell was already used up
			if not ms['Flags']: continue
			
			if spell_hash.has_key (ms['SpellResRef']):
				spell_hash[ms['SpellResRef']] = spell_hash[ms['SpellResRef']] + 1
			else:
				spell_hash[ms['SpellResRef']] = 1
				spell_list.append( ms['SpellResRef'] )


	Button = GemRB.GetControl (Window, 15 + i)
	GemRB.SetButtonSprites (Window, Button, 'AMGENS', 0, 0, 1, 2, 3)


	if i + float_menu_index < len (spell_list):
		SpellResRef = spell_list[i + float_menu_index]
		GemRB.SetSpellIcon (Window, Button, '') # clear item sprites
		GemRB.SetSpellIcon (Window, Button, SpellResRef)
		GemRB.SetText (Window, Button, "%d" %spell_hash[SpellResRef])
		
		#	GemRB.SetEvent (Window, Icon, IE_GUI_BUTTON_ON_PRESS, "OpenPriestSpellUnmemorizeWindow")
		#else:
		#	GemRB.SetEvent (Window, Icon, IE_GUI_BUTTON_ON_PRESS, "OnPriestUnmemorizeSpell")
		#GemRB.SetEvent (Window, Icon, IE_GUI_BUTTON_ON_RIGHT_PRESS, "OpenPriestSpellInfoWindow")
		spell = GemRB.GetSpell (SpellResRef)
		GemRB.SetTooltip (Window, Button, spell['SpellName'])
		#PriestMemorizedSpellList.append (ms['SpellResRef'])
		#GemRB.SetVarAssoc (Window, Icon, "SpellButton", i)
		#GemRB.EnableButtonBorder (Window, Icon, 0, ms['Flags'] == 0)
		GemRB.SetButtonFlags (Window, Button, IE_GUI_BUTTON_NO_IMAGE, OP_NAND)
	else:
		GemRB.SetSpellIcon (Window, Button, '')
		GemRB.SetText (Window, Button, '')
		GemRB.SetTooltip (Window, Button, '')




def FloatMenuSelectNextPC ():
	sel = GemRB.GameGetFirstSelectedPC ()
	if sel == 0:
		OpenFloatMenuWindow ()
		return

	GemRB.GameSelectPC (sel % GemRB.GetPartySize () + 1, 1, SELECT_REPLACE)
	# NOTE: it invokes FloatMenuSelectAnotherPC() through selection change handler

def FloatMenuSelectAnotherPC ():
	global float_menu_mode, float_menu_index
	float_menu_mode = MENU_MODE_SINGLE
	float_menu_index = 0
	UpdateFloatMenuWindow ()


def FloatMenuSelectDialog ():
	GemRB.GameControlSetTargetMode (TARGET_MODE_ALL | TARGET_MODE_TALK)
	UpdateFloatMenuWindow ()

def FloatMenuSelectWeapons ():
	global float_menu_mode, float_menu_index
	float_menu_mode = MENU_MODE_WEAPONS
	float_menu_index = 0
	# FIXME: Force attack mode
	GemRB.GameControlSetTargetMode (TARGET_MODE_ALL | TARGET_MODE_ATTACK)
	UpdateFloatMenuWindow ()

def FloatMenuSelectItems ():
	global float_menu_mode, float_menu_index
	float_menu_mode = MENU_MODE_ITEMS
	float_menu_index = 0
	UpdateFloatMenuWindow ()

def FloatMenuSelectSpells ():
	global float_menu_mode, float_menu_index
	float_menu_mode = MENU_MODE_SPELLS
	float_menu_index = 0
	GemRB.GameControlSetTargetMode (TARGET_MODE_ALL | TARGET_MODE_CAST)
	UpdateFloatMenuWindow ()

def FloatMenuSelectAbilities ():
	global float_menu_mode, float_menu_index
	float_menu_mode = MENU_MODE_ABILITIES
	float_menu_index = 0
	UpdateFloatMenuWindow ()


def FloatMenuPreviousItem ():
	global float_menu_index
	if float_menu_index > 0:
		float_menu_index = float_menu_index - 1
		print "P", float_menu_index
		UpdateFloatMenuWindow ()

def FloatMenuNextItem ():
	global float_menu_index
	float_menu_index = float_menu_index + 1
	print "N", float_menu_index
	UpdateFloatMenuWindow ()


def FloatMenuDrag ():
	dx, dy = GemRB.GetVar ("DragX"), GemRB.GetVar ("DragY")
	GemRB.SetWindowPos (FloatMenuWindow, dx, dy, WINDOW_RELATIVE | WINDOW_BOUNDED)
