## BackUp Alice Skill

Nothing you need to do with this skill other than install it.

### Principle of operation:

Every hour Alice will check to see if you have a backed up version of ProjectAlice.

The back up is stored in the home directory under a folder called "AliceBackUp"
The frequency of the back ups is set in the skill settings. 
Choose the amount of days between backups and click Save. 

- <i>Make it a whole number and above 0</i>
 
The default value is 7. So Alice will update the backed up folder every 7 days in that case

If you want to invoke a back up you can say "back yourself up" or similar but to be honest 
that's not really necessary unless its a initial back up, as she will do it automatically herself anyway.

However, if you want to force a back up, ask alice to "force a back up" and she will make a back up regardless
of the date of the existing backup.

### Restore feature

There is now a option in the skills settings to restore a file or directory from a previous backup to your 
current ProjectAlice folder. To achieve this ....

- Open the skill's "settings" screen from the webUi
- In the field called "path of restore file" add the path of the file or directory that you want to restore
  - examples are
    - skills/AliceVolume <-- This will be the whole AliceVolume Directory
    - skills/Reminder/Sounds/Alarm/Alarm.wav <-- This will be the Alarm.wav from reminder skill
    - config.json <-- This will be the config file from ~/ProjectAlice directory
- Enable the "Enable File Restore" switch.

Once "Enable File Restore" is enabled and you have a valid path written in "path of restore file" 
within one minute you will see in the syslog that the copy process has happend from the backup directory 
to the active ProjectAlice folder. It will then disable the "Enable File Restore" switch 
(refresh UI to see the updated state). 
