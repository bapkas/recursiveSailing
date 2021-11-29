import numpy as np
import ast
import math
import random
riktningar = [0,45,90,135,180,225,270,315]

class hav:

    def __init__(self, kolumner, rader):
        """ Init-metod som sätter kolumn och radargumenten från när vi skapar objektet att peka
        på sitt eget objekt. """
        self.kolumner = kolumner
        self.rader = rader

    def get_Vindinfo(self,file):
        """ Reads a text file containing information about our matrix we are sailing in."""
        vindInfo = [[] for x in range(self.rader)]
        temp=[]
        counter=0
        counter2=0
        with open(file,"r") as f:
            while True and counter < self.rader:
                line = f.readline()
                if not line.startswith("#"):
                    break
            while line and counter < self.rader:
                temp=line.split(" ")
                for item in temp:
                    if item!="\n" and counter2<self.kolumner:
                        counter2+=1
                        first,second=item.split(",")
                        vindInfo[counter].append((int(first),int(second)))
                line = f.readline()
                counter2=0
                counter+=1
        return vindInfo

class Paths:

    def __init__(self,plist):

        self.plist=plist

    def validPos(self,targetposi,path,hav,riktning,nonValid):

        if targetposi[0]<hav.rader and targetposi[1]<hav.kolumner and targetposi[0]>=0 and targetposi[1]>=0 and targetposi not in path.plist and ((targetposi,riktning)) not in nonValid:
            if get_Relativriktning(targetposi,riktning) == 180:
                nonValid.append((targetposi,riktning))
                return False
            else:
                return True
        else:
            return False

    def getRiktning(self,path,twoPoints):

        temp = []
        riktning = []
        diffs = {(1,0):0,(0,-1):90,(1,-1):45,(-1,-1):135,(-1,0):180,(-1,1):225,(0,1):270,(1,1):315}
        if twoPoints!="twoPoints":
            for item in path:
                temp.append(item)
                if len(temp)==2:
                    diff = ((temp[0][0]-temp[1][0]),(temp[0][1]-temp[1][1]))
                    for key in diffs:
                        if key == diff:
                            riktning.append(diffs[key])
                            temp.pop(0)
        else:
            for rikt in riktningar:
                key_list=list(diffs.keys())
                value_list=list(diffs.values())
                position=value_list.index(rikt)
                value=key_list[position]
                temp.append(((path[0]+(value[0]*-1)),(path[1]+(value[1]*-1))))
                riktning.append(rikt)
            return temp,riktning
        return riktning

    def getPathTime(self,plist, path, currentpos):



        tempRiktning = []
        tempTimeList = []
        copyOfPath = []
        tempTime1 = 0
        copyOfPath = plist.copy()
        copyOfPath.append(currentpos)
        tempRiktning = path.getRiktning(copyOfPath, "list")
        for i in range(len(tempRiktning)):
            relrik = get_Relativriktning(copyOfPath[i + 1], tempRiktning[i])
            speed = get_Speed(relrik, copyOfPath[i + 1])
            time = get_Time(speed, tempRiktning[i])
            tempTimeList.append(time)
        return sumTime(tempTimeList)

def get_Relativriktning(targetpos,båtriktning):
    """ Vi ger varje riktning en motsvarande vektor i R2 med storlek av standardbasvektorerna
    och räknar sedan ut med hjälp av koncept från linjalg vinkel mellan två vektorer och
    sedan returnerar vi denna vinkel. """
    dct = {"0":[0,1],"45":[1,1],"90":[1,0],"135":[1,-1],"180":[0,-1],"225":[-1,-1],"270":[-1,0],"315":[-1,1]}
    vindriktning = vind_forhallande[targetpos[0]][targetpos[1]][1]
    båtriktning = dct[str(båtriktning)]
    vindriktning = dct[str(vindriktning)]
    vektor1dist = np.sqrt((vindriktning[0])**2+(vindriktning[1])**2)
    vektor2dist = np.sqrt((båtriktning[0])**2+(båtriktning[1])**2)
    vektor1 = vindriktning
    vektor2 = båtriktning
    skalarprod = (vektor1[0]*vektor2[0]+vektor1[1]*vektor2[1])
    relativriktning = math.acos(skalarprod/(vektor1dist*vektor2dist))
    relativriktning = np.degrees(relativriktning)
    return relativriktning

def get_Speed(relativriktning,targetpos):
    """ Funktion för att få farten givet en relativriktning och en plats vi ska till
    använder helt enkelt funktioner från uppgiftsbeskrivningen. """
    vindStyrka = vind_forhallande[targetpos[0]][targetpos[1]][0]
    speed=1
    if abs(relativriktning-45)<=1:
            if vindStyrka >= 5:
                speed = 0
                return speed
            else:
                speed = vindStyrka
                return speed
    if abs(relativriktning-90)<=1:
        if vindStyrka >= 7:
            speed = vindStyrka*0.25
            return speed
        else:
            speed = vindStyrka*0.5
            return speed
    if abs(relativriktning-135)<=1:
        speed = vindStyrka * 0.3
        return speed
    if abs(relativriktning-0)<=1:
        if vindStyrka >= 9:
            speed = speed * 0.5
            return speed
        else:
            speed = speed * 0.25
            return speed
    if abs(relativriktning-180)<=1:
        speed = 0
        return speed
    return speed

def get_Time(speed,riktning):

    if riktning == 45 or 135 or 225 or 315:
        distance = np.sqrt(2)
    else:
        distance = 1
    time = distance / speed
    return time

def sumTime(timeList):

    total_time=0
    for item in timeList:
        total_time+=item
    return total_time

def recursive(currentpos,path,finalpos,t_paths,hav,nonValid,minTimeList):


    #basfall
    if currentpos == finalpos and path.getPathTime(path.plist,path,currentpos)<=(min(minTimeList)):
        tempRiktning=[]
        tempRelRik=[]
        tempTimeList=[]
        speedList=[]
        copyOfPath=[]
        tempTime1=0
        copyOfPath = path.plist.copy()
        copyOfPath.append(currentpos)
        tempRiktning=path.getRiktning(copyOfPath,"list")
        tempRelRiktning=get_Relativriktning(currentpos,tempRiktning[-1])
        tempSpeed=get_Speed(tempRelRiktning,currentpos)
        if tempSpeed != 0:
            tempTime1=get_Time(tempSpeed,tempRiktning[-1])
        tempPoints,tempRiktning2=path.getRiktning(copyOfPath[-2],"twoPoints")
        for point in tempPoints:
            riktIndex=tempPoints.index(point)
            riktning = tempRiktning2[riktIndex]
            if path.validPos(point,path,hav,riktning,[]) and currentpos != point:
                tempRelRiktning=get_Relativriktning(point,riktning)
                tempSpeed=get_Speed(tempRelRiktning,point)
                if tempSpeed != 0:
                    tempTime=get_Time(tempSpeed,riktning)
                    tempTimeList.append(tempTime)
                    if min(tempTimeList) >= tempTime1:
                        if (point,riktning) not in nonValid:
                            nonValid.append((point,riktning))
        for i in range(len(copyOfPath)-1):
            relrik=get_Relativriktning(copyOfPath[i+1],tempRiktning[i])
            tempRelRik.append(relrik)
            speed=get_Speed(relrik,copyOfPath[i+1])
            speedList.append(speed)
            time=get_Time(speed,tempRiktning[i])
            tempTimeList.append(time)
        if 0 not in speedList:
            minTimeList.append(sumTime(tempTimeList))
            t_paths.append(copyOfPath)


    path.plist.append(currentpos)

    #riktning0 vi kollar också om pathen vi ska till inte tar mer tid än den optimala pathen vi har
    if path.validPos((currentpos[0]-1,currentpos[1]),path,hav,0,nonValid) and ((path.getPathTime(path.plist,path,(currentpos[0]-1,currentpos[1])))<min(minTimeList)):
        recursive((currentpos[0]-1,currentpos[1]),path,finalpos,t_paths,hav,nonValid,minTimeList)

    #riktning45 vi kollar också om pathen vi ska till inte tar mer tid än den optimala pathen vi har
    if path.validPos((currentpos[0]-1,currentpos[1]+1),path,hav,45,nonValid) and (path.getPathTime(path.plist,path,(currentpos[0]-1,currentpos[1]+1))<min(minTimeList)):
        recursive((currentpos[0]-1,currentpos[1]+1),path,finalpos,t_paths,hav,nonValid,minTimeList)

    #riktning90 vi kollar också om pathen vi ska till inte tar mer tid än den optimala pathen vi har
    if path.validPos((currentpos[0],currentpos[1]+1),path,hav,90,nonValid) and (path.getPathTime(path.plist,path,(currentpos[0],currentpos[1]+1))<min(minTimeList)):
        recursive((currentpos[0],currentpos[1]+1),path,finalpos,t_paths,hav,nonValid,minTimeList)

    #riktning135 vi kollar också om pathen vi ska till inte tar mer tid än den optimala pathen vi har
    if path.validPos((currentpos[0]+1,currentpos[1]+1),path,hav,135,nonValid) and (path.getPathTime(path.plist,path,(currentpos[0]+1,currentpos[1]+1))<min(minTimeList)):
        recursive((currentpos[0]+1,currentpos[1]+1),path,finalpos,t_paths,hav,nonValid,minTimeList)

    #riktning180 vi kollar också om pathen vi ska till inte tar mer tid än den optimala pathen vi har
    if path.validPos((currentpos[0]+1,currentpos[1]),path,hav,180,nonValid) and (path.getPathTime(path.plist,path,(currentpos[0]+1,currentpos[1]))<min(minTimeList)):
        recursive((currentpos[0]+1,currentpos[1]),path,finalpos,t_paths,hav,nonValid,minTimeList)

    #riktning225 vi kollar också om pathen vi ska till inte tar mer tid än den optimala pathen vi har
    if path.validPos((currentpos[0]+1,currentpos[1]-1),path,hav,225,nonValid) and (path.getPathTime(path.plist,path,(currentpos[0]+1,currentpos[1]-1))<min(minTimeList)):
        recursive((currentpos[0]+1,currentpos[1]-1),path,finalpos,t_paths,hav,nonValid,minTimeList)

    #riktning270 vi kollar också om pathen vi ska till inte tar mer tid än den optimala pathen vi har
    if path.validPos((currentpos[0],currentpos[1]-1),path,hav,270,nonValid) and (path.getPathTime(path.plist,path,(currentpos[0],currentpos[1]-1))<min(minTimeList)):
        recursive((currentpos[0],currentpos[1]-1),path,finalpos,t_paths,hav,nonValid,minTimeList)

    #riktning315 vi kollar också om pathen vi ska till inte tar mer tid än den optimala pathen vi har
    if path.validPos((currentpos[0]-1,currentpos[1]-1),path,hav,315,nonValid) and (path.getPathTime(path.plist,path,(currentpos[0]-1,currentpos[1]-1))<min(minTimeList)):
        recursive((currentpos[0]-1,currentpos[1]-1),path,finalpos,t_paths,hav,nonValid,minTimeList)

    path.plist.pop()

def printSea(fastestPath,hav):

    row=[]
    mat=[]
    n=hav.kolumner
    for i in range(hav.rader):
        row=list(n*[""])
        mat.append(row)
    for i in range(hav.rader):
        for j in range(hav.kolumner):
            if (i,j) in fastestPath:
                mat[i][j]=fastestPath.index((i,j))

    for item in mat:
        print("\n",item)

def createTxt():
    txtpath="vindfil.txt"
    f= open("vindfil.txt","w")
    f.write("#Format: vindstyrka(m/s),vindriktning(grader)")
    for i in range(100):
        f.write("\n")
        for j in range(100):
            randomint1=random.randint(0,7)
            randomint2=random.randint(1,10)
            f.write(str(randomint2)+","+str(riktningar[randomint1]))
            f.write(" ")
    f.close()
    return txtpath

def main():
    
    t_paths=[]
    nonValid=[]
    minTimeList=[100]
    p=hav(5,5)
    file=createTxt()
    global vind_forhallande
    vind_forhallande=p.get_Vindinfo(file)
    path=Paths([])
    #startingpoint = ast.literal_eval(input("Skriv dina startkoordinater i formen (x,y) och mellan (0,0)-(4,4): "))
    #finalpoint = ast.literal_eval(input("Skriv slutkoordinaterna i formen (x,y) och mellan (0,0)-(4,4): "))
    recursive((0,0),path,(4,4),t_paths,p,nonValid,minTimeList)
    if t_paths:
        min_index = minTimeList.index(min(minTimeList))
        if min_index == 1:
            min_index+=-1
        printSea(t_paths[min_index],p)
        print(min(minTimeList), " fastest time,")
        print(" Siffrorna representerar i vilken ordning vi seglade, 0 först, 1 andra, osv.")
    else:
        print("No paths to point")

if __name__ == "__main__":
    main()
