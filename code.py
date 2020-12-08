#%% Import
import os
os.chdir('/home/raki/wd/repos/checkers/mails/')
import mailconnect

### File History ###

#   Filename                                URL                                     Valid/Total
# 'yahoo_normal.txt'    https://buyaccs.com/getaccs.php?token=bukG1KJGG72Ls             0/15
# 'yahoo_normal2.txt'   https://buyaccs.com/download/38_dCdDqDX2h6s.txt                 15/15
# 'yahoo_pop.txt'       https://buyaccs.com/getaccs.php?token=bu8SfsIDsMZhU&lang=en     8/15
# 'hotmail_basic.txt'   https://buyaccs.com/getaccs.php?token=buE8GukuS7HYc             2/50
# 'hotmail_basic2.txt'  https://buyaccs.com/download/169_tc1akno7rcG4.txt               0/50
# 'outlook_pop.txt'     https://buyaccs.com/getaccs.php?token=buJLMYGb.Mwnk&lang=en     7/30
# 'outlook_pop2.txt'    https://buyaccs.com/download/209_Xoom3pt7G48.txt                30/30

#%% File testing
filenames = ['outlook_pop2.txt']   # If you want to test just one file

combos = mailconnect.combo_extract(filenames) # importing combolists to a dict
mailconnect.check_combos(filenames, combos, save=False) # checking working combos

#%%
print('Count: '+str(mailconnect.valid()))

#%%
mailconnect.valid_to_csv()