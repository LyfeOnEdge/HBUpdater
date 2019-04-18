#format.py

#offset from left in listbox
lbcolumnoffset = 10

#width infoframe takes up
infoframewidth = 200

#Height of searhbox
searchboxheight=45

#Height of the frames holding the column titles
columtitlesheight= 25 

#secondary column relwidth
column_relwidth = .20

#Image for when there is an author image incompatible with tkinter
notfoundimage = "notfound.png"

##Text Styles
#Normal Text
smalltext = ("Trebuchet MS",10)
mediumtext = ("Trebuchet MS",12)
largetext = ("Trebuchet MS",14,)
#Bold
smallboldtext = ("Trebuchet MS",10,"bold")
mediumboldtext = ("Trebuchet MS",12,"bold")
largeboldtext = ("Trebuchet MS",14,"bold")

##Main colors:
#background color
light_color = "#1f1f1f"
#Color for most user-interactable items
dark_color = "#121212"
#White
w = "#ffffff"
#Black
b = "#000000"
#ash
ash = "#c4c4c4"
#lgray (used for author / priject title / description
lgray = "#acadaf"

listboxselectionbackground =  "#c4c4c4",
listboxselectionforeground = b

import platform




#column label 
columnlabelcolor = w
columnlabelfont = mediumboldtext

#Text in listbox
listbox_font  = mediumtext
listbox_font_color = w
tags_listbox_font = mediumtext
dark_listbox_font_color = "#777777"

#Text in settings menu
settings_font = largetext
settings_font_color = w

#Font when typing in search box
search_font = mediumtext
search_font_color = w

#font for placeholder in search bar
place_holder_font = mediumboldtext
place_holder_color = "gray"
place_holder_text = "Type and press enter to search"



#font color of hilighted text in versions details
selectedtextforeground = w

##text for details view
#version number listbox colors
version_number_color = w
version_number_font = mediumboldtext
version_number_column_background = dark_color
#version detail colors
version_notes_color = w
version_notes_font = smalltext
version_notes_column_background = dark_color
#color of hightlight when selecting text in version notes
version_notes_selection_foreground = b
version_notes_selection_background = ash

#Info column 
info_author_color= lgray
info_author_font = smallboldtext

info_softwarename_color = w
info_softwarename_font = largeboldtext

info_description_color = w
info_description_font = smalltext

#Main selesction and version selection highlight color
selectioncolor = "#595959"

#other:
checkmark = u'\u2713'


#Width of nav button box
navboxwidth = infoframewidth
navbuttonheight = 40
navbuttonfont = mediumboldtext
navbuttonspacing = 4
etcbuttonwidth = navbuttonheight

#Spacing for buttons in line with search bar
icon_and_search_bar_spacing = navbuttonspacing

guidetext = smalltext
guidetextcolor = lgray
RCMGUIDETEXT = """INSTRUCTIONS:

- Enter RCM on your Nintendo Switch.

- Select the payload you wish to inject.

- Inject payload.

If you receive an error it likely means your Nintendo Switch is not in RCM.
You can ensure you have turned your switch off by holding the power button for 13 seconds.
"""



##Injector Page
consoletext = smalltext