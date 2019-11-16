from PIL import Image
import time
#first start with getting name of file
filename = input("Please input name of file desired. IN PNG FORMAT BECAUSE ALL OTHER FORMATS ARE INFERIOR: ")


im = Image.open(filename).convert("RGBA")

pixels = im.load()
width,height = im.size

#must get user input as to start of vector from which fade will start
print("Image size is " + str(width) + "x" + str(height) + "\nNow you will input the point of the image from which all pixels perpendicular to the direction of travel specified will be faded.")
xstr = input("Please Input the x coordinate of the initial vector position: ")
ystr = input("Please Input the y coordinate of the initial vector position: ")
initial = [int(xstr),int(ystr)]

if(not(0 <= initial[0] < width) or not(0 <= initial[1] < height)):
    print("Yeah... That position is not really within the image itself buddy.")
    quit()

#now for direction
print("Please repeat the same process for the direction of fade, which will be starting from the initial position you have just entered.")
xstr = input("Please Input the X coordinate of the direction. Only inputs of -1, 0, and 1 are allowed: ")
ystr = input("Please Input the Y coordinate of the direction. Only inputs of -1, 0, and 1 are allowed: ")
#check for stupid people giving stupid input
if(not(-1 <= int(xstr) <= 1) or not(-1 <= int(ystr) <= 1)):
    print("Illegal input for direction found. Please do be aware that since this direction must be an integer, floating directions after normalizations may have caused unwanted results. We are only thinking for you here so do cooperate. Terminating program.")
    quit()
direction = [int(xstr), int(ystr)]
#now get the alpha factor
finalalphafactor = input("Almost there! Now please enter, by the end of the run, what percentage opaque you would like the final pixel to be:")
if(not(0<= int(finalalphafactor) < 100)):
    print("You do realize that percentages are... well... percentages?")
    quit()

#now get the name of the file we shall create in the end.
finalfilename = input("Finally, enter the name of the file you would like created: ")
if(len(finalfilename) < 5):
    finalfilename += ".png"
if(not(finalfilename[len(finalfilename) - 4:] is ".png")):
    finalfilename += ".png"

#now we shall start the process!

def image_within_dir(point, direc, timeout):
    while timeout > 0:
        timeout -= 1
        point = [point[0] + direc[0], point[1] + direc[1]]
        if((0 <= point[0] < width) and (0 <= point[1] < height)):
            return True
    return False

def is_within_image(point):
    return ((0 <= point[0] < width) and (0 <= point[1] < height))

#find the two perpendiculars
if direction[0] is 0:
    perp1 = [1,0]
    perp2 = [-1,0]
elif direction[1] is 0:
    perp1 = [0,1]
    perp2 = [0,-1]
else:
    perp1 = [direction[0], -direction[1]]
    perp2 = [-direction[0], direction[1]]



#find length of our traversion and thus gradient.
traversion_left = 0



chosperp = perp1
for i in range(0,2):
    if(i is 1):
        chosperp = perp2
    timeout = 1
    startpoint = [initial[0] - direction[0], initial[1] - direction[1]]
    while is_within_image(startpoint):
        startpoint = [startpoint[0] - direction[0], startpoint[1] - direction[1]]
    while image_within_dir(startpoint, chosperp, timeout):
        timeout += 1
        traversion_left += 1
        startpoint = [startpoint[0] - direction[0], startpoint[1] - direction[1]]

initial_traversion_end = traversion_left

current = [initial[0], initial[1]]
while (0 <= current[0] < width) and (0 <= current[1] < height):
    traversion_left += 1
    current = [current[0] + direction[0], current[1] + direction[1]]

alphalayer = Image.new("L", [width,height])
alayer = alphalayer.load()
current = [initial[0], initial[1]]

#now extend traversion left, because image is not a box.
curperp = perp1

proper_traversion = traversion_left

print(proper_traversion)

for i in range(0,2):
    if(i is 1):
        curperp = perp2
    test_point = [initial[0] + direction[0] * (traversion_left - initial_traversion_end), initial[1] + direction[1] * (traversion_left - initial_traversion_end)]
    timeout = 1
    while is_within_image(test_point):
        test_point = [test_point[0] + direction[0], test_point[1] + direction[1]]
    while image_within_dir(test_point, curperp, timeout):
        traversion_left += 1
        timeout += 1
        test_point = [test_point[0] + direction[0], test_point[1] + direction[1]]

print(traversion_left)

floating_alpha_gradient = ((int(finalalphafactor) - 100)/100 *255)/(traversion_left - initial_traversion_end)
floating_current_alpha = 255

print(initial_traversion_end)

#now the fun part!
timeout = initial_traversion_end
for i in range(0, traversion_left):
    #print("-----------------------------------------------")
    current = [initial[0] + (i - initial_traversion_end) * direction[0], current[1]]
    if(i is 0):
        floating_current_alpha += floating_alpha_gradient * initial_traversion_end
        floating_alpha_gradient = -floating_alpha_gradient

    if(i is not 0):
        floating_current_alpha += floating_alpha_gradient
    currentalpha = int(floating_current_alpha)
    #print(currentalpha)
    for d in range(0,2):
        if(i is 0):
            current = [current[0], initial[1] + (i - initial_traversion_end) * direction[1]]
        if(d is 1):
            if((direction[1] is 0) or (i is 0)):
                break
            current = [current[0], initial[1] + (i - initial_traversion_end) * direction[1]]
            if(i < initial_traversion_end):
                timeout -= 1
        for j in range(0,2):
            if(j is 0):
                currentperp = perp1
            else:
                currentperp = perp2
            moving = [current[0], current[1]]
            runwhile = True
            if not is_within_image(moving):
                if (not(image_within_dir(current, currentperp, timeout))):
                    currentperp = perp2
                moving = [moving[0] + currentperp[0] * timeout, moving[1] + currentperp[1] * timeout]
            #print(str(moving) + ":" + str(currentalpha)
            while runwhile:
                alayer[moving[0],moving[1]] = currentalpha
                #print(str(moving) + ":" + str(currentalpha))
                moving = [moving[0] + currentperp[0], moving[1] + currentperp[1]]
                if (not((0 <= moving[0] < width) and (0 <= moving[1] < height))):
                    runwhile = False
            if ((i is initial_traversion_end) and (d is 0) and (j is 0)):
                floating_alpha_gradient = -floating_alpha_gradient
                timeout = 1
            if not is_within_image(current):
                break
    if(i >= proper_traversion):
        timeout += 1

im.putalpha(alphalayer)
#save the file and terminate.
print("------------------------------------------------------------")
print("Thanks for choosing Questry Software!")
time.sleep(1)
im.save(finalfilename)
