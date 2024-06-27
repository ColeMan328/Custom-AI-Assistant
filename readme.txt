############################## Installation ##############################

This project REQUIRES python to be installed to the user's account. It
also requires the user to have an active API key to access openai's models
and to have the API key saved to a txt file. It is also recomended that 
you install your desired png files for the assistant, user, and page icons
and a jpg file for the background of the site (defaults to solid gray). Do
note that the site icon will also be the desktop icon.

Start by running downloading and running "setup_wizard.py"
This will open a setup UI that will guide you through the following steps

Select desired install location:
It is best to save the main directory in "C:-Users-(your user)" but it
can be saved anywhere.

Select your API key:
Before proceeding further, you will have to select your API key file.
THIS IS REQUIRED TO PROCEED ANY FURTHER

Customize the theme:
Here is where you will be able to change the UI header color, the 
background image, and icons for the assistant, user, and webpage/desktop

The script will then run the install.bat file to install all application 
requirements and set up AI model. You will be able to set the desired 
model to use, the temperature (creativity) of the model, and set a prompt 
to determine the model's personality.

When the installation is complete there will be a new shortcut on your
desktop named "Custom AI" and at this point the setup is complete and the
AI is ready to use!

##########################################################################

######################## File uploading explained ########################

All uploaded files are saved to the uploads folder. To upload a file use
the upload button in the UI. This will save the file to the uploads folder
and it will simultaneously run a function to read all the text in the file
and append it to the "documents_content.txt" file. When you want to delete
a file you will need to delete the file from the uploads folder and all of
its related contents from the "documents_content.txt" file. (This is
planned to be fixed in a later version). Once uploaded the assistant will
be able to read through the uploaded documents and answer questions that
are directly related to them.

##########################################################################
##########################################################################

####################### Modify basic UI appearance #######################

To change desktop icon and the icon that appears at the top-left of the 
page start by navigating to the main directory, then to the static folder.
In the folder you will need to delete the two images named icon. Then 
upload the .png image you would like to use to the folder and rename it to
icon. After making sure the name has been changed you will need to go back
to the main directory and open (run) "convert_icon.py)" to create a copy
of your icon file as a .ico.

To change the icons that appear in the message window for the user and or 
the assistant you will need to replace the user.png and or the assist.png
images respectively
