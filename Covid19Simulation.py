# I hereby certify that this program is solely the result of my own work and 
# is in compliance with the Academic Integrity policy of the course syllabus  
# and the academic integrity policy of the CS department.

# THE PROGRAM SHOULD BE RUN ON A MAC

# This program is a simulation of the spread of the Novel Coronavirus through 
# a population without any quarantine or social distance procedures. 
# It takes several conditions through user input and determines the spread of
# the infection based on these inputs, as well as a number of predermined 
# values based on real data on the coronavirus pandemic.

# Limitations on the accuracy of the simulation include, but are not limited to:
# 1. A cap on population size.
# 2. The population is completely isolated and has no influx of other, 
#    potentially infected, members.
# 3. The conditions which lead to a change in the status of an infected
#    member's infection are not completely accurate given the lack of 
#    research on Covid-19.
# 4. The simulation only considers possible spread when there is direct
#    physical contact between two members.
# 5. The size of the box in which the simulation takes place does not adjust
#    for larger populations. Thus, larger populations will spread Covid-19
#    more quickly.

# Work Cited:
#  1. Schimelpfening, Nancy. "How Long Does Immunity Last After
#     COVID-19? What We Know." 14 October 2020.
#     https://www.healthline.com/health-news/how-long-does-immunity-last-after-covid-19-what-we-know
#  2. 11 December 2020. https://www.cdc.gov/coronavirus/2019-ncov/covid-data/covidview/index.html
#  3. Stevens, Harry. "Why outbreaks like coronavirus spread exponentially, 
#     and how to “flatten the curve." 14 March 2020.
#     https://www.washingtonpost.com/graphics/2020/world/corona-simulator/?tid=a_classic-iphone&no_nav=true

import Draw
import random
import math
import ElasticCollision

# Population() creates a 2D List, whose rows represent members of a
# population. The columns represent the characteristics of each member,
# specficially: their x,y locations, their dx, dy, whether or not they
# are infected with Covid-19, how long their infection has lasted, whether or 
# not they are vaccinated, and whether or not they have antibodies and
# therefore are immune.

def population(numPop, infecRate, vaccRate):
    members=[]
    #set parameters
    for i in range(numPop):
        #set x and y coordinates
        x=random.random()*500
        y=random.uniform(20, 512)
        #calculate trajectory
        angle=random.uniform(0, 2*math.pi)
        dx=math.cos(angle)
        dy=math.sin(angle)
        #intialize infected to False
        infected=False
        #initialize infection length to zero
        timeSinceInfection=0
        #intialize vaccination to False
        vaccStatus=False
        #no members start immune
        immune=False

        #create 2D list of members of the population
        members+=[[x, y, dx, dy, infected, timeSinceInfection, \
                   vaccStatus, immune]]  
    
    #set the right amount of members infected and vaccinated based
    #on infecRate and vaccRate   
    
    #infecRate is taken in as a decimal, so multiply by numPop to find how 
    #many members should be infected
    infecRate=int(infecRate*numPop)
    #vaccRate is taken in as a whole number, so divide by 100 before multiplying
    vaccRate=int((vaccRate/100)*numPop)
    numInfected=0
    numVaccinated=0
    #when the number of infected members is less than it should be 
    #(based on the rate), randomly assign members to be infected
    while numInfected!=infecRate:
        infecMember=random.choice(members)
        infecMember[4]=True
        numInfected=0
        #count how many members are infected
        for x in members:
            if x[4]:
                numInfected+=1
    #when the number of vaccinated members is less than it should be 
    #(based on the rate), randomly assign members to be vaccinated    
    while numVaccinated!=vaccRate:
        vaccMember=random.choice(members)
        vaccMember[6]=True
        numVaccinated=0
        #count how many members are vaccinated
        for x in members:
            if x[6]:
                numVaccinated+=1
    return members

# drawKey() is a template for drawing the color coded squares that make up
# the key explaining what the color of each circle corresponds with. Pass in 
# to the function the color of the rectangle and its Y coordinate, and the key 
# is drawn.

def drawKey(color, y):
    #set color of the rectangle to the color passed in
    Draw.setColor(color)
    Draw.filledRect(522, y, 20 ,20)
    Draw.setColor(Draw.BLACK)
    Draw.rect(522, y, 20 ,20)    

# drawBoard() draws the background on which the simulation takes place.
# It creates a rectangle in which the members will interact. It also sets up
# the text of the controls, but not the buttons of the controls.

def drawBoard(vaccEffective, infecRate, vaccRate, numPop, members, \
              transmissionRate, immunityRate, hour, day):
    
    #display time elapsed since start of simulation
    Draw.setFontSize(12)
    Draw.setColor(Draw.BLACK)
    Draw.line(512, 0, 512, 512)
    Draw.line(0, 20, 512, 20)
    Draw.string("DAY: "+str(day), 5, 5)
    #if hour is single digit, draw a '0' next to the hour
    if int(hour)<10:
        Draw.string("HOUR: 0"+str(hour)[0], 55 , 5)
    else:
        Draw.string("HOUR: "+str(hour)[0:2], 55 , 5)
            
    #draw parameters
    Draw.setFontSize(24)
    Draw.string("Infection Rate: "+str(infecRate*100)[0:4] +"%", 552, 20)
    Draw.string("Population Size: " + str(numPop), 552, 60)
    Draw.string("Vaccination Rate: "+str(vaccRate)[0:4]+"%", 552, 100)
    Draw.string("Vaccination Effective: "+str(vaccEffective)[0:4]+"%", \
                552, 140)
    Draw.string("Transmission Rate: "+str(transmissionRate)[0:4]+"%", \
                552, 180)
    Draw.string("Immunity Rate: "+str(immunityRate)[0:4]+"%", 552, 220)
    
    #draw key explaining what each color represents
    #draw red square using the function that has a template for the squares 
    drawKey(Draw.RED, 300)
    
    #draw orange square using the function that has a template for the squares 
    drawKey(Draw.ORANGE, 330)
    
    #draw green square using the function that has a template for the squares 
    drawKey(Draw.GREEN, 360)

    #draw purple square using the function that has a template for the squares 
    drawKey(Draw.VIOLET, 390)

    
    #next to each square, explain what that color circle represents
    Draw.setFontSize(18)
    Draw.setColor(Draw.BLACK)
    Draw.string("INFECTED, CONTAGIOUS", 550, 300)
    Draw.string("INFECTED, NOT CONTAGIOUS", 550, 330)
    Draw.string("HEALTHY", 550, 360)
    Draw.string("IMMUNE", 550, 390)

# instructionPage() draws an instruction page, explaining to the user how to 
# set parameters of the simulation, the purpose of the simulation, and what
# each parameters represents.

def instructionPage():
    Draw.setColor(Draw.BLACK)
    
    #draw text box
    Draw.rect(69, 99, 387, 382)
    Draw.rect(70, 100, 385, 380)
    Draw.line(70, 220, 455, 220)
    Draw.line(70, 370, 455, 370)
    
    #Title of Program
    Draw.setFontSize(36)
    Draw.setColor(Draw.BLUE)
    Draw.string("COVID-19 SIMULATION", 63, 50)
    
    #Draw instructions and explanation of the program
    Draw.setFontSize(24)
    Draw.setColor(Draw.BLACK)
    Draw.string("A SIMULATION OF THE SPREAD\nOF THE NOVEL CORONAVIRUS\nTHROUGH"\
                + " A POPULATION \nWITHOUT ANY QUARANTINE OR \nSOCIAL DISTANCE"\
                +" PROCEDURE", 75, 225)
    Draw.string("USE CONTROL CENTER TO SET \nSIMULATION PARAMETERS", 75, 100)
    Draw.string("PRESS START TO BEGIN", 75, 175)
    
    #In smaller font, explain each parameter
    Draw.setFontSize(12)
    Draw.string("Infection Rate: percentage of the population infected.",\
                75, 375)
    Draw.string("Population Size: number of people in the population.", \
                75, 390)
    Draw.string("Vaccination Rate: percentage of the population vaccinated.",\
                75, 405)
    Draw.string("Vaccination Effective: effectiveness of the vaccine.", 75, 420)
    Draw.string("Transmission Rate: likelihood of contracting the virus after"\
                +"\ncontact with an infected person.", 75, 435)
    Draw.string("Immunity Rate: likelihood of developing antibodies after"\
                +" infection.", 75, 462)    

# closingPage() draws a closing page to display when the simulation ends,
# displaying the total simulation time.

def closingPage(day, hour):
    #clear the simulation so only the closing will display
    Draw.clear()
    #tell user simulation ended
    Draw.setColor(Draw.BLACK)
    Draw.setFontSize(24)
    Draw.string("SIMULATION COMPLETE", 300, 100) 
    #display total time of simulation
    Draw.string("SIMULATION TIME", 340.5, 150)   
    Draw.string(str(int(day))+str(hour/24)[1:4]+" DAYS", \
                390-(len(str(day))+3), 185)
    #draw boxes around the text'
    Draw.rect(298, 99, 292, 27)
    Draw.rect(299, 100, 290, 25)    
    Draw.rect(338.5, 149, 217, 27)
    Draw.rect(339.5, 150, 215, 25)
    Draw.rect(338.5, 149, 217, 82)
    Draw.rect(339.5, 150, 215, 80)
    Draw.show()
 
# drawPeople() draws the members, represented as circles.
# The color of their circles is indicative of their infection status, per 
# the key in drawBoard().

def drawPeople(members):
    #For reference:
        #p[4] = infected
        #p[5] = timeSinceInfec
        #p[7] = immune
    
    #loop through each member of the population
    for p in members:
            #if member is infected
            if p[4]:
                #if under 10 days, not contagious, represent as orange circle
                if p[5]<=240:
                    Draw.setColor(Draw.ORANGE)
                    Draw.filledOval(p[0], p[1], 10, 10)
                #after 10 days (240 loops), contagious, represent as red circle
                else:
                    Draw.setColor(Draw.RED)
                    Draw.filledOval(p[0], p[1], 10, 10) 
                #increment timeSinceInfection by 0.5 each loop 
                #because in each loop, the time increases by 0.5 hours
                p[5]+=0.5
            #if member not infected
            else:
                #if immune, represent as purple circle
                if p[7]:
                    Draw.setColor(Draw.VIOLET)
                    Draw.filledOval(p[0], p[1], 10, 10) 
                #if healthy but not immune, represent as green circle
                else:
                    Draw.setColor(Draw.GREEN)
                    Draw.filledOval(p[0], p[1], 10, 10)                     

# movePeople() moves the members by their trajectories and accounts for
# reflecting off the side of the box.

def movePeople(members):
    for p in members:
        #increment x,y by dx,dy
        p[0]+=p[2]
        p[1]+=p[3]  
    
        #if circles hit edge, reflect off the side
        
        #if hit right border, reflect
        if p[0]>=502: 
            p[2]*=-1
            p[0]-=1
        #if hit left border, reflect
        elif p[0]<=0:
            p[2]*=-1
            p[0]+=1
        #if hit bottom border, reflect
        elif p[1]>=502:
            p[1]-=1
            p[3]*=-1
        #if hit top border, reflect
        elif p[1]<21:
            p[1]+=1
            p[3]*=-1     

# checkCollisions() checks whether any members came in contact with one another.
# If they did, store in a 2D list to be dealt with later and display elastic
# collision between the two members.

def checkCollisions(members):
    #initalize local variables
    collisions=[]
    x=0
    y=0
    
    #loop through members
    for row in range(len(members)):
        #store center x coordinate in x1
        x1=members[row][0]+10
        #store center y coordinate in y1
        y1=members[row][1]+10
        for i in range(row+1, len(members)):
            #find center of each circle
            x2 = members[i][0]+10
            y2 = members[i][1]+10
            #use Euclidian distance to check if two members are in contact
            if abs(math.sqrt((x2-x1)**2+(y2-y1)**2))<=10+0.0001:
                #collisions is a 2D list of members that collided
                collisions+=[[row,i]]
                ElasticCollision.collide(members[row], members[i])

    return collisions

# updateStatus() loops through the list of which members came in contact. 
# Based on the infection status of the members in contact with one another,
# assess if the infection will spread to one of the members.

def updateStatus(collisions, members, transmissionRate, vaccEffective):
    #since transmissionRate and vaccEffective are taken in as whole numbers,
    #divide by 100 to get values that are easier to work with
    transmissionRate=transmissionRate/100
    vaccEffective=vaccEffective/100
    
    #loop through collisions to access which members collided
    for row in range(len(collisions)):
        for col in range(0, len(collisions[row]), 2):
            x=collisions[row][col]
            y=collisions[row][col+1]
            #if first infected and not the second
            if members[x][4] and members[x][5]>=240 and \
               not(members[y][4]) and not(members[y][7]):
                #if not vaccinated, become infected
                if  not members[y][6] and random.random()<=transmissionRate:
                    members[y][4]=True
                #if vaccinated, randomly decide based on vaccEffective if the
                #member will be infected despite being vaccinated                
                elif members[y][6] and random.random()>vaccEffective \
                     and random.random()<=transmissionRate:
                    members[y][4]=True
            #now check if the second is infected but not the first
            elif not(members[x][4]) and  members[y][4] and members[y][5]>=240 \
                 and not(members[x][7]):
                #if not vaccinated, become infected
                if not members[x][6] and random.random()<=transmissionRate:
                    members[x][4]=True
                #if vaccinated, randomly decide based on vaccEffective if the
                #member will be infected despite being vaccinated
                elif members[x][6] and random.random()>vaccEffective \
                     and random.random()<=transmissionRate:
                    members[x][4]=True                    

# updateInfec() uses the infection status of each member to determine if they
# will die, become immune, return to a normal, healthy status, or if their 
# infection status will not change.

def updateInfec(members, deathRate, numPop, immunityRate):
    immunityRate=immunityRate/100
    for p in members:
        #after twenty days of infection, there is potential for a change in
        #infecStatus
        if p[5]>=480:
            x=random.random()
            #based on death rate, decide if die
            if x*.01<=deathRate:
                members.remove(p)
                numPop-=1
            #members who do not die each day have a 20% chance of recovery;
            #if they do not recover, nothing happens to their infection status 
            elif random.random()>.20:
                break
            #if member does not die but does change infecStatus, they recover.
            #must assess if they develop antibodies to the virus or return
            #to regular status with the potential to be infected again            
            elif x<=immunityRate:
                p[7]=True
                p[4]=False
                p[5]=0
            elif x>immunityRate:
                p[4]=False
                p[5]=0
    return numPop 

# setParameters() draws the buttons next to the parameters displayed on the 
# instructions page. Allows user to adjust the simulation parameters. Draws the
# START button - when the user presses START, the simulation begins and
# parameters can no longer be adjusted.

def setParameters(members, infecRate, numPop, vaccRate, vaccEffective, \
                  immunityRate, transmissionRate, start):
    start=False
    day=0
    hour=0
    #as long as the user has not pressed start, the instructions show
    while not start:     
        Draw.clear()
        #Display the instructions page
        instructionPage()
        
        #Draw the board
        drawBoard(vaccEffective, infecRate, vaccRate, numPop, members, \
                  transmissionRate, immunityRate, hour, day)
        
        #draw START button, disappears after pressing start
        Draw.setColor(Draw.GREEN)
        Draw.filledRect(522, 440, 80, 30)
        Draw.setColor(Draw.BLACK)
        Draw.setFontSize(24)
        Draw.string("START", 522, 440)
        Draw.rect(522, 440, 80, 30)        
        
        #Draw + and - signs to dissapear after pressing start
        for i in range(6):
            #draw boxes around + and - signs
            Draw.rect(522, 16+40*i, 14, 14)
            Draw.rect(522, 36+40*i, 14, 14)
    
            #draw + signs
            #horizontal lines
            Draw.line(522, 23+40*i, 535, 23+40*i)
            Draw.line(522, 23+40*i+1, 535, 23+40*i+1)
            Draw.line(522, 23+40*i-1, 535, 23+40*i-1)
            
            #vertical lines
            Draw.line(530, 16+40*i, 530, 16+40*i+13)
            Draw.line(529, 16+40*i, 529, 16+40*i+13)
            Draw.line(528, 16+40*i, 528, 16+40*i+13)
           
            #draw minus signs
            Draw.line(522, 43+40*i, 535, 43+40*i)
            Draw.line(522, 42+40*i, 535, 42+40*i)
            Draw.line(522, 44+40*i, 535, 44+40*i)        
        
        #check for user input and adjust parameters based on input
        if Draw.mousePressed():
            #check if user pressed start
            newX = Draw.mouseX()
            newY = Draw.mouseY()
            #is user presses START, begin simulation
            if newX>=522 and newX<=602:
                if newY>=440 and newY<=470:
                    start=True
            #the following block of code asses if the user has clicked any
            #of the buttons that adjust parameters, and adjusts the respective
            #parameter. Each parameter has an upper and lower bound. None of
            #them can be negative, no rates can be higher than 1 (aka 100%), and
            #due to limitations on the use of the ElasticCollisions code that
            #is used, the population size (numPop) cannot be greater than 120.
            if newX>=522 and newX<=536:
                #infecRate must be a whole number to start,
                #because there can't be a fraction of a person infected,
                if newY>=16 and newY<=30 and infecRate<1:
                    infecRate+=.01
                elif newY>=36 and newY<=50 and infecRate-.01>=0:
                    infecRate-=.01              
                elif newY>=56 and newY<=70 and numPop<120:
                    numPop+=1
                elif newY>=76 and newY<=90 and numPop>0:
                        numPop-=1 
                elif newY>=96 and newY<=110 and vaccRate<=100:
                    vaccRate+=.1
                elif newY>=116 and newY<=130 and vaccRate-1>=0:
                    vaccRate-=.1
                elif newY>=136 and newY<=150 and vaccEffective<100:
                    vaccEffective+=.1
                elif newY>=156 and newY<=170 and vaccEffective-1>=0:
                    vaccEffective-=.1
                elif newY>=176 and newY<=190 and transmissionRate<100:
                    transmissionRate+=.1
                elif newY>=196 and newY<=210 and transmissionRate-1>=0:
                    transmissionRate-=.1
                elif newY>=216 and newY<=230 and immunityRate<100:
                    immunityRate+=.1
                elif newY>=236 and newY<=250 and immunityRate-1>=0:
                    immunityRate-=.1               
        #reinitialize the population based on new parameters
        members=population(numPop, infecRate, vaccRate)
        Draw.show()   
        
        #return a tuple of the adjusted parameters
        return members, infecRate, numPop, vaccRate, vaccEffective, \
               immunityRate, transmissionRate, start

# countHealthy() counts how many members are healthy and how many are infected.
# Returns the number of healthy members in order to determine if simulation 
# should continue. Calculates the updated infecRate based on number of infected 
# members and number of people remaining in the population.

def countHealthy(members):
    #initialize both variables
    infec=0
    healthy=0
    #loop through and check if infected or healthy
    for p in members:
        #if healthy, increment healthy by 1
        if not(p[4]):
            healthy+=1
        #if infected, increment infec by 1
        else:
            infec+=1
        #calculate updated infecRate
        infecRate=(infec/len(members))
    #return values in a tuple
    return healthy, infecRate

# time() keeps track of the time since the start of the simulation. Each loop
# represents 0.5 hours, and 24 hours make up one day. Time returns a tuple
# with the updated time.

def time(day, hour):
    #after 24 hours, increment days by one and set hours to 0
    if int(hour)==24:
        day+=1
        hour=0
    #2 loops = one "hour"
    hour+=0.5 
    return day, hour

# main() executes the functions in the correct manner to run the simulation.

def main():
    #set canvas size
    Draw.setCanvasSize(900, 512)       

    #initialize parameters to default
    numPop=100
    infecRate=0.50
    vaccRate=10.0
    vaccEffective=50.0
    immunityRate=50.0
    transmissionRate=10.0
    #death rate cannot be changed by the user
    deathRate=0.00026
    
    #initialize the population
    members=population(numPop, infecRate, vaccRate)
    
    #set time to 0 days, 0 hours
    day=0
    hour=0  
    
    #before user presses START, allow modification of simulation parameters
    start=False
    while not start:
        #run setParameters() so that user can modify parameters 
        #and unpack the tuple that is returned
        members, infecRate, numPop, vaccRate, vaccEffective, immunityRate,\
        transmissionRate, start=setParameters(members, infecRate, \
        numPop, vaccRate, vaccEffective, immunityRate, transmissionRate, start)
    
    # While their are members alive and there are members who are infected,
    # run the simulation
    healthy=0
    while numPop>0 and healthy!=numPop:
        #calculate the time since beginning of simulation          
        day, hour = time(day, hour)
        
        #clear the board to remove controls and start button
        Draw.clear()
        
        #redraw the board
        drawBoard(vaccEffective, infecRate, vaccRate, numPop, members, \
                  transmissionRate, immunityRate, hour, day)
        
        #draw the members of the population
        drawPeople(members)
        
        #animate the population
        movePeople(members)
        
        #assess if any members have been in contact
        collisions=checkCollisions(members)
        
        #based on contact, assess if more members are infected
        updateStatus(collisions, members, transmissionRate, vaccEffective)
        
        #based on infections, assess if infected members will die, become
        #immune, become healthy, or remain infected
        numPop=updateInfec(members, deathRate, numPop, immunityRate)
        
        #show the simulation
        Draw.show()
        
        #check whether to continue simulation, and update infecRate
        healthy, infecRate=countHealthy(members)
    
    #display closing page
    closingPage(day, hour)

main()