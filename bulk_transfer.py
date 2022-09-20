import time
import subprocess

input("Start Drop? Press Any Key.\n"
     "WARNING! Existing success and failed log files will be overwritten")
input("Press Any Key Again To Commence")


fingerprint = 199829636
fee = 0
amount = 2000
wallet_id = 2
batch_size = 5


# Set to 'a' if you don't want logs to overwrite
success = open('success.txt', 'w')
failed = open('failed.txt', 'w')
address_file = open('drop_list.txt', 'r')

addresses = []
dr = address_file.readlines()

for line in dr:
    addresses.append(line.rstrip())

for i in range(0, len(addresses)):

    gen = subprocess.Popen(
        ['chia', 'wallet', 'send', "-f", str(fingerprint), "-i", str(wallet_id), "-a", str(amount), "-m", str(fee), "-t", addresses[i]], 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    time.sleep(2)

    if "Exception" in str(gen.communicate()):
        failed.write(addresses[i] + '\n')
        print('Failed On:', addresses[i])

    else:
        success.write(addresses[i] + '\n')
        print('Success On:', addresses[i])

    if i % batch_size == 0:
        success.flush()
        failed.flush()
        print('Waiting 120 seconds...')
        j = 0
        while j < 120:
            if  j % batch_size == 0:
                print(j,'/120 seconds...')
            time.sleep(1)
            j += 1
