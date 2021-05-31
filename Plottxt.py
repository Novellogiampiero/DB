import matplotlib.pyplot as plt


#plt.plot([1,2,3,4])
#plt.ylabel('some numbers')
#plt.show()

L = ["Geeks\n", "for\n", "Geeks\n"]
 
# Writing to a file
#file1 = open('test.txt', 'w')
#file1.writelines((L))
#file1.close()
 
# Using readline()
file1 = open('test.txt', 'r')
count = 0
AA=[]
BB=[]
while (count<600000):
    count += 1
    try: 
        # Get next line from file
        line = file1.readline()
        line1=line.strip()
        line2=line1.split("\t")
        a=float(line2[0])
        #b=float(line2[1])
        AA.append(a)
        #BB.append(b)
        #print(" a is ",type(a))
        #print(" b is ",type(b))
        # if line is empty
        # end of file is reached
        if not line:
            break
    except:
        print("Line{}: {}".format(count,line1))
plt.plot(AA)
#plt.plot(BB)
plt.ylabel('some numbers')
plt.show()
file1.close()
