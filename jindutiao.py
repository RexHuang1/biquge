import time
import sys
for i in range(10):
    sys.stdout.write('\r')
    sys.stdout.write("%s%% |%s" %(int(i%10), int(i%10)*'#'))
    sys.stdout.flush()
    time.sleep(0.1)
print('\n' + 'finish!')
 
sys.stdout.write('\n')
