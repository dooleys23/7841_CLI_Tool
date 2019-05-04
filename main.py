import pexpect, code, time, threading, re

global phone_list
phone_list = []


class phone():
    def __init__(self, ip, dn):
        # Define self variables
        self._ip = ip
        self._dn = dn

    def create_session(self):
        # Setup SSH Session, cisco phones usually have username as root/admin
        self._child = pexpect.spawn('setup ssh connection, ie, username@x.x.x.x')
        self._child.expect('assword:*')
        self._child.sendline('send password')
        # 7841's have additional login, defaults are debug/debug
        self._child.expect('login:*')
        self._child.sendline('debug')
        self._child.expect('assword*')
        self._child.sendline('debug')
        # Regex check for initial prompt
        self._child.expect('[\w]*>') 
        
        # Allow test session to open
        # WARNING, THIS OCCURS OVER TELNET, key actions are easily readible,
        # It is not advised to send pins, directory numbers, or other sensitive info over telnet
        self._child.sendline('test open')
        self._child.expect(prompt)
        # cli prompt being assigned for child.expect statements
        self._prompt = self._child.after

    def call(self, called_party):
        if re.match('^[0-9]*$', called_party) and len(called_party) < 12:
            self._child.sendline('test key {0} spkr'.format(called_party))
            self._child.expect(self._prompt)
        else:
            print('That input was not acceptable. Please verify that:' \
                  '\nOnly 0-9 is used' \
                  '\nNo more than 11 digits are entered')


    def call_internal(self, remote_phone):
        self._child.sendline('test key {0} spkr'.format(remote_phone._dn))
        self._child.expect(self._prompt)
        time.sleep(7)
        remote_phone._child.sendline('test key spkr')
        remote_phone._child.expect(remote_phone._prompt)

    def unity(self, pin = 'default pin'):
        try:
            self._child.sendline('test key <unity dn> spkr')
            self._child.expect(self._prompt)
            time.sleep(5)
            self._child.sendline('test key {0}#'.format(pin))
            self._child.expect(self._prompt)
            time.sleep(5)
            self._child.sendline('test key spkr')
            self._child.expect(self._prompt)

        # CTRL C detected, cancel call and return to prompt
        except KeyboardInterrupt:
            self._child.sendline('test key spkr')
            self._child.expect(self._prompt)

    def unity_update(self, pin_default = 'default', pin_new = 'pin_new'):
        self._child.sendline('test key <unity dn> spkr')
        self._child.expect(self._prompt)
        time.sleep(5)
        self._child.sendline('test key {0}#'.format(pin))
        self._child.expect(self._prompt)
        time.sleep(5)
        # Navigate handler to change pin menu with 431 entry, may vary on unity config
        self._child.sendline('test key 431')
        self._child.expect(self._prompt)

        # Enter new pin
        time.sleep(3)
        self._child.sendline('test key {0}#'.format(pin_new))
        self._child.expect(self._prompt)

        # Enter new pin again
        time.sleep(5)
        self._child.sendline('test key {0}#'.format(pin_new))
        self._child.expect(self._prompt)

        # Terminate call
        time.sleep(8)
        self._child.sendline('test key spkr')
        self._child.expect(self._prompt)

    def voldown(self, presses = 10):
        # Default increase == 10, pass a number for set amount of increases
        self._child.sendline('test key {0}'.format(str('voldn ' * presses)))
        self._child.expect(self._prompt)

    def volup(self, presses = 10):
        # Default increase == 10, pass a number for set amount of decreases
        self._child.sendline('test key {0}'.format(str('volup ' * presses)))
        self._child.expect(self._prompt)

    def spkr(self):
        self._child.send('test key spkr')
        self._child.expect(self._prompt)

    def factory_reset(self, reset_type):
        if reset_type.lower() in ['factory', 'servicemode', 'soft', 'hard']:
            self._child.sendline('reset {0}'.format(reset_type.lower()))
            self._child.expect(self._prompt)
            print(self._child.before)
        else:
            print("Response not valid, please enter one of the following:\n'factory'\n'servicemode'\n'soft'\n'hard'")

    def custom(self, command):
        self._child.sendline('{0}'.format(command))
        self._child.expect(self._prompt)
        print(self._child.before)


class all_phones():
    def __init__(self):
        self._phone_list = phone_list

    def unity(self):
        for fon in phone_list:
            t = threading.Thread(target=fon.unity)
            t.start()

    def unity_update(self):
        for fon in phone_list:
            t = threading.Thread(target=fon.unity_update)
            t.start()

    def volup(self):
        for fon in phone_list:
            t = threading.Thread(target=fon.up)
            t.start()

    def voldown(self):
        for fon in phone_list:
            t = threading.Thread(target=fon.voldown)
            t.start()

    def factory_reset(self, reset_type):
        if reset_type.lower() in ['factory', 'servicemode', 'soft', 'hard']:
            for fon in phone_list:
                t = threading.Thread(target=fon.factory_reset, args = (reset_type))
                t.start()
        else:
            print("Response not valid, please enter one of the following:\n'factory'\n'servicemode'\n'soft'\n'hard'")


def main():
    # create a list of lab phones. Can confirm stable on 20+ phones.
    
    lab_phone1 = phone('ip_of_phone[x.x.x.x]', 'dn_of_phone')
    lab_phone2 = phone('ip_of_phone[x.x.x.x]', 'dn_of_phone')
    lab_phone3 = phone('ip_of_phone[x.x.x.x]', 'dn_of_phone')
    lab_phone4 = phone('ip_of_phone[x.x.x.x]', 'dn_of_phone')

    phone_list.append(lab_phone1)
    phone_list.append(lab_phone2)
    phone_list.append(lab_phone3)
    phone_list.append(lab_phone4)
    phone_list.append(hc)
    phone_list.append(osc)
    phone_list.append(ted)
    phone_list.append(ps)

    # Phone is a shadow reference, fon == phone
    for fon in phone_list:
        t = threading.Thread(target=fon.create_session)
        t.start()

    all = all_phones()

    print('Establishing ssh connections, cli access in 5 seconds')
    time.sleep(5)
    code.interact(local=locals())

main()
