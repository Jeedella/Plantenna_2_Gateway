filename = 'localfile.csv'
rc = False #did not connect
if rc == False:
    f = open(filename, 'a')
    f.write('current,data\n')
    f.close()

else:
    f = open(filename,'r')
    text = f.read()
    text_divided = text.split('\n')
    for i in range(len(text_divided)):
                   print(text_divided[i])
                   #send data to AWS
    f.close()
    f = open(filename, 'w')
    #f.truncate(0)
    f.close()
