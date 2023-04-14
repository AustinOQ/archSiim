'''Convert File.simpleAsm to memory representation.
    Legal instructions-->
        add  intReg1 intReg2 destinationReg
        mult intReg1 intReg2 destinationReg
        and  intReg1 intReg2 destinationReg
        not  intReg1 destinationReg
        store sourceReg destinationMemAddress
        load sourceMemAddress destinationReg
        branch condition newPC
        out register
'''

from cmpl import *
from executionUnit import *
from outFormatted import *
from branchPredictor import *

#branch predictor says always taken.
#no reordering.
#no dependency handling. Leave that to the programmer.
#programs start at address 0 
#jump to end of memory or address 9999 to quit. 
#fetch, decode, execute, save all use unique components. 
#all instructions take 4 cycle.
#branch resolved in store phase
#cpu is pipelined and forwarded.
def processing():
    clock=0
    pc=0 #points to next instruction to start.
    r0,r1,r2,r3,r4,r5,r6=0,0,0,0,0,0,0

    statequeue=[]#used to flash back to last known legal state. 
   
    file=input("Enter assembly file name:")
    #mem=[[address, [instruction], flag array]...]. flag=1 when execution is speculative.
    prog=cmpl(file)
    dataArea=[0]*(100-len(prog))
    mem=prog+dataArea
    
    fetch,decode,execute=None,None,None
    fetchTemp,decodeTemp,executeTemp,storeTemp=None,None,None,None

    #START MAIN EVENT LOOP
    while(pc!=len(prog)+3 and pc!=9999):

        output=''

        #fetch unit
        if(pc<len(prog)):
            output+="fetch"+ mem[pc][1], "from memory location",pc,'.','At time:',clock,'#'
            fetchTemp=mem[pc]
            

        #decode unit
        if(fetch!=None and pc<len(prog)+1):
            output+="decode",fetch[1], "from memory location",fetch[0],'.','At time:',clock
            decodeTemp=fetch
            #if this is a branch, save all running data in case mispredict. 
                #running data is registers
            if(decodeTemp[1][0]=='branch'):
                statequeue=statequeue+[[r0,r1,r2,r3,r4,r5,r6]]
            

        #execute unit
        if(decode!=None and pc<len(prog)+2):
            output+=("execute",decode[1], "from memory location",decode[0],'.','At time:',clock)
            executeTemp=decode
            #this is where out command is executed.
            if(executeTemp[1][0]=='out'):
                print(eval(executeTemp[1][1]))
            elif(executeTemp[1][0]=='add'):
                if(executeTemp[1][3]=='r0'):
                    r0=eval(executeTemp[1][1])+eval(executeTemp[1][2])
                elif(executeTemp[1][3]=='r1'):
                    r1=eval(executeTemp[1][1])+eval(executeTemp[1][2])
                elif(executeTemp[1][3]=='r2'):
                    r2=eval(executeTemp[1][1])+eval(executeTemp[1][2])
                elif(executeTemp[1][3]=='r3'):
                    r3=eval(executeTemp[1][1])+eval(executeTemp[1][2])
                elif(executeTemp[1][3]=='r4'):
                    r4=eval(executeTemp[1][1])+eval(executeTemp[1][2])
                elif(executeTemp[1][3]=='r5'):
                    r5=eval(executeTemp[1][1])+eval(executeTemp[1][2])
                elif(executeTemp[1][3]=='r6'):
                    r6=eval(executeTemp[1][1])+eval(executeTemp[1][2])
                else:
                    print("Error durring additions at memory location:", executeTemp[0])
                    quit()

            elif(executeTemp[1][0]=='mult'):
                if(executeTemp[1][3]=='r0'):
                    r0=eval(executeTemp[1][1])*eval(executeTemp[1][2])
                elif(executeTemp[1][3]=='r1'):
                    r1=eval(executeTemp[1][1])*eval(executeTemp[1][2])
                elif(executeTemp[1][3]=='r2'):
                    r2=eval(executeTemp[1][1])*eval(executeTemp[1][2])
                elif(executeTemp[1][3]=='r3'):
                    r3=eval(executeTemp[1][1])*eval(executeTemp[1][2])
                elif(executeTemp[1][3]=='r4'):
                    r4=eval(executeTemp[1][1])*eval(executeTemp[1][2])
                elif(executeTemp[1][3]=='r5'):
                    r5=eval(executeTemp[1][1])*eval(executeTemp[1][2])
                elif(executeTemp[1][3]=='r6'):
                    r6=eval(executeTemp[1][1])*eval(executeTemp[1][2])
                else:
                    print("Error durring additions at memory location:", executeTemp[0])
                    quit()

            elif(executeTemp[1][0]=='and'):
                if(executeTemp[1][3]=='r0'):
                    r0=eval(executeTemp[1][1])^eval(executeTemp[1][2])
                elif(executeTemp[1][3]=='r1'):
                    r1=eval(executeTemp[1][1])^eval(executeTemp[1][2])
                elif(executeTemp[1][3]=='r2'):
                    r2=eval(executeTemp[1][1])^eval(executeTemp[1][2])
                elif(executeTemp[1][3]=='r3'):
                    r3=eval(executeTemp[1][1])^eval(executeTemp[1][2])
                elif(executeTemp[1][3]=='r4'):
                    r4=eval(executeTemp[1][1])^eval(executeTemp[1][2])
                elif(executeTemp[1][3]=='r5'):
                    r5=eval(executeTemp[1][1])^eval(executeTemp[1][2])
                elif(executeTemp[1][3]=='r6'):
                    r6=eval(executeTemp[1][1])^eval(executeTemp[1][2])
                else:
                    print("Error durring additions at memory location:", executeTemp[0])
                    quit()

            elif(executeTemp[1][0]=='not'):
                if(executeTemp[1][2]=='r0'):
                    r0=~eval(executeTemp[1][1])
                elif(executeTemp[1][3]=='r1'):
                    r1=~eval(executeTemp[1][1])
                elif(executeTemp[1][3]=='r2'):
                    r2=~eval(executeTemp[1][1])
                elif(executeTemp[1][3]=='r3'):
                    r3=~eval(executeTemp[1][1])
                elif(executeTemp[1][3]=='r4'):
                    r4=~eval(executeTemp[1][1])
                elif(executeTemp[1][3]=='r5'):
                    r5=~eval(executeTemp[1][1])
                elif(executeTemp[1][3]=='r6'):
                    r6=~eval(executeTemp[1][1])
                else:
                    print("Error durring additions at memory location:", executeTemp[0])
                    quit()

            
        #store unit
        if(execute!=None):
            output+=("store",execute[1], "from memory location",execute[0],'.','At time:',clock)
            storeTemp=execute
            #if branch fails,
                #delete all temp files, clear components, set pc to branch specified
                #reload registers with saved data. 
            if(storeTemp[1][0]=='branch'):
                if(eval(storeTemp[1][1])):
                    #print('branch true####################################')
                    #pop saved state since it wont be needed
                    statequeue=statequeue[1:]
                else:
                    #print("branch false, roleback starting.############")
                    r0,r1,r2,r3,r4,r5,r6=statequeue[0][0],statequeue[0][1],statequeue[0][2],statequeue[0][3],statequeue[0][4],statequeue[0][5],statequeue[0][6]
                    pc=eval(storeTemp[1][2])-1
                    fetch,decode,execute=None,None,None

            elif(storeTemp[1][0]=='store'):
                address=int(storeTemp[1][2])
                print(address)
                mem[address]=eval(executeTemp[1][1])
                print(mem[address])

            elif(storeTemp[1][0]=='load'):
                address=eval(storeTemp[1][1])
                if(storeTemp[1][2]=='r0'):
                    r0=str(eval(mem[int(address)]))
                elif(executeTemp[1][3]=='r1'):
                    r1=str(eval(mem[int(address)]))
                elif(executeTemp[1][3]=='r2'):
                    r2=str(eval(mem[int(address)]))
                elif(executeTemp[1][3]=='r3'):
                    r3=str(eval(mem[int(address)]))
                elif(executeTemp[1][3]=='r4'):
                    r4=str(eval(mem[int(address)]))
                elif(executeTemp[1][3]=='r5'):
                    r5=str(eval(mem[int(address)]))
                elif(executeTemp[1][3]=='r6'):
                    r6=str(eval(mem[int(address)]))
                
                

        
        #clock ticks and everything moves forward in exe cycle unless branch.
        pc+=1
        clock+=1
        fetch=fetchTemp
        decode=decodeTemp
        execute=executeTemp
        output+=('r0=',r0,', r1=',r1,', ,r2=',r2,', r3=',r3,', r4=',r4,', r5=',r5,', r6=',r6)

        #####OUTPUT TO FILE HERE#######

processing()
