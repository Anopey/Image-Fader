from PIL import Image
import time

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, x,y):
        self.x += x
        self.y += y

    def add2DVector(self, vector2d):
        self.x += vector2d.x
        self.y += vector2d.y

    def __add__(self, o):
        if(isinstance(o, Vector2D)):
            self.add(o.x, o.y)
        else:
            self.x += o
            self.y += o
        return self

    def __sub__(self, o):
        if(isinstance(o, Vector2D)):
            self.add(-o.x, -o.y)
        else:
            self.x -= o
            self.y -= o
        return self

    def __str__(self):
        return "( " + self.x + ", " + self.y + ")"

    def __mul__(self, o):
        if(isinstance(o, Vector2D)):
            self.x *= o.x
            self.y *= o.y
        else:
            self.x *= o
            self.y *= o
        return self

    def __truediv__(self, o):
        if(isinstance(o, Vector2D)):
            self.x /= o.x
            self.y /= o.y
        else:
            self.x /= o
            self.y /= o
        return self

    def __isub__(self, o):
        return self - o


    def __iadd__(self, o):
        return self + o

    def __imul__(self,o):
        return self * o

    def __idiv__(self,o):
        return self / o



while(True):
#get user input.
    initialInput = input("Please input one of the following for different services: 'quit', 'pixelFade', 'gradualColorer' - ")
    if(initialInput == "quit"):
        quit()

    if(initialInput == "pixelFade" or initialInput == "gradualColorer"):
        filename = input("Please input URL of file desired in PNG or JPG/JPEG format: ")
        im = Image.open(filename).convert("RGBA")
    #PIXEL FADE---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #PIXEL FADE---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #PIXEL FADE---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #PIXEL FADE---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #PIXEL FADE---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #PIXEL FADE---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if(initialInput == "pixelFade"):
        pixels = im.load()
        width,height = im.size
        #must get user input as to start of vector from which fade will start
        print("Image size is " + str(width) + "x" + str(height) + "\nNow please input the point of the image from which all pixels perpendicular to the direction of travel specified will be faded.")
        xstr = input("Please Input the x coordinate of the initial vector position: ")
        ystr = input("Please Input the y coordinate of the initial vector position: ")
        initial = [int(xstr),int(ystr)]

        if(not(0 <= initial[0] < width) or not(0 <= initial[1] < height)):
            print("Yeah... That position is not really within the image itself.")
            continue;

        #now for direction
        print("Please repeat the same process for the direction of fade, which will be starting from the initial position you have just entered.")
        xstr = input("Please Input the X coordinate of the direction. Only inputs of -1, 0, and 1 are allowed: ")
        ystr = input("Please Input the Y coordinate of the direction. Only inputs of -1, 0, and 1 are allowed: ")
        #check for bad input
        if(not(-1 <= int(xstr) <= 1) or not(-1 <= int(ystr) <= 1)):
            print("Illegal input for direction. Terminating.")
            continue;
        direction = [int(xstr), int(ystr)]
        #now get the alpha factor
        finalalphafactor = input("Almost there! Now please enter, by the end of the run, what percentage opaque you would like the final pixel to be: ")
        if(not(0<= int(finalalphafactor) <= 100)):
            print("percentages are... well... percentages")
            continue;

        #deal with backwards symmetry
        symmetryBackwards = ""
        while(symmetryBackwards != "Y" and symmetryBackwards != "N"):
            symmetryBackwards = input("Would you like the image to have a symmetric backwards alpha gradient applied as well?[Y/N]: ")
        symmetryBackwards = (symmetryBackwards == "Y")

        #now get the name of the file we shall create in the end.
        finalfilename = ""
        while (len(finalfilename) < 1):
            finalfilename = input("Finally, enter the URL of the file you would like created: ")
        if(len(finalfilename) < 5):
            finalfilename += ".png"
        if(not(finalfilename[len(finalfilename) - 4:] == ".png")):
            finalfilename += ".png"

        #now we shall start the process!
        def is_within_image(point):
            return ((0 <= point[0] < width) and (0 <= point[1] < height))

        def image_within_dir(point, direc, timeout):
            timeout += 1
            while timeout > 0:
                timeout -= 1
                point = [point[0] + direc[0], point[1] + direc[1]]
                if(is_within_image(point)):
                    return True
            return False


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
        initimeout = 0
        startpoint = [initial[0] - direction[0], initial[1] - direction[1]]
        while is_within_image(startpoint):
                startpoint = [startpoint[0] - direction[0], startpoint[1] - direction[1]]
                traversion_left +=1
        for i in range(0,2):
            if(i is 1):
                chosperp = perp2
            while image_within_dir(startpoint, chosperp, initimeout):
                initimeout += 1
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

        #now extend traversion left, because image may not be a box.
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
        print(initimeout)
        #now the fun part!
        timeout = initimeout
        for i in range(0, traversion_left):
            #print("-----------------------------------------------")
            current = [initial[0] + (i - initial_traversion_end) * direction[0], current[1]]
            if(i is 0):
                if(symmetryBackwards):
                    floating_current_alpha += floating_alpha_gradient * initial_traversion_end
                else:
                    floating_current_alpha = 255;
                floating_alpha_gradient = -floating_alpha_gradient

            if(i != 0 and not(i <= floating_current_alpha and not symmetryBackwards)):
                floating_current_alpha += floating_alpha_gradient
            currentalpha = int(floating_current_alpha)
            for d in range(0,2):
                if(i is 0):
                    current = [current[0], initial[1] + (i - initial_traversion_end) * direction[1]]
                if(d is 1):
                    if((direction[1] == 0) or (i == 0)):
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
                    #print(str(moving) + ":" + str(currentalpha))
                    while runwhile:
                        #print(str(moving) + ":" + str(currentalpha))
                        alayer[moving[0],moving[1]] = currentalpha
                        moving = [moving[0] + currentperp[0], moving[1] + currentperp[1]]
                        if (not((0 <= moving[0] < width) and (0 <= moving[1] < height))):
                            runwhile = False
                    if ((i == initial_traversion_end) and (d == 0) and (j == 0)):
                        floating_alpha_gradient = -floating_alpha_gradient
                        timeout = 1
                    if not is_within_image(current):
                        break
            if(i >= proper_traversion):
                timeout += 1

        im.putalpha(alphalayer)
        im.save(finalfilename)
    #GRADUAL COLORER----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #GRADUAL COLORER----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #GRADUAL COLORER----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #GRADUAL COLORER----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #GRADUAL COLORER----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    elif(initialInput == "gradualColorer"):
        pixels = im.load()
        width,height = im.size
        frames_left = 0
        while(frames_left < 1):
            frames_left = int(input("How many instance images would you like to be produced? Please input an integer >= 1: "))
        #must get user input as to start of vector from which coloring will start
        print("Image size is " + str(width) + "x" + str(height) + "\nNow please input the starting point - point of the image from which all pixels perpendicular to the direction of travel specified will be colored.")
        xstr = input("Please Input the x coordinate of the initial vector position: ")
        ystr = input("Please Input the y coordinate of the initial vector position: ")
        initial = Vector2D(int(xstr),int(ystr))

        if(not(0 <= initial.x < width) or not(0 <= initial.y < height)):
            print("Yeah... That position is not really within the image itself.")
            continue;

        #get direction
        print("Please repeat the same process for the direction of colouring, which will be starting from the initial position you have just entered.")
        xstr = input("Please Input the X coordinate of the direction. Only inputs of -1, 0, and 1 are allowed: ")
        ystr = input("Please Input the Y coordinate of the direction. Only inputs of -1, 0, and 1 are allowed: ")
        #check for bad input
        if(not(-1 <= int(xstr) <= 1) or not(-1 <= int(ystr) <= 1)):
            print("Illegal input for direction. Terminating.")
            continue;
        direction = Vector2D(int(xstr), int(ystr))
        #get final point
        print("Image size is " + str(width) + "x" + str(height) + "\nNow please input the end point. Input -1 if you would like this to be whenever the image itself ends.")
        xstr1 = input("Please Input the x coordinate of the final vector position: ")
        ystr1 = input("Please Input the y coordinate of the final vector position: ")
        final = (int(xstr),int(ystr))
         
        if(final.x == -1 or final.y == -1):
            #deduce final point
            while(not(0 <= final.x < width) or not(0 <= final.y < height)):
                final += direction
            final -= direction
        if(not(0 <= final.x < width) or not(0 <= final.y < height)):
            print("Yeah... That position is not really within the image itself.")
            continue;

        #get color

        print("Now please enter the color in RGB format.")
        R = -1
        G = -1
        B = -1
        while(R < 0 or R > 255):
            R = int(inpt("R value (0-255): "))
        while(G < 0 or G > 255):
            G = int(inpt("G value (0-255): "))
        while(B < 0 or B > 255):
        B = int(inpt("B value (0-255): "))


        #now get the name of the file we shall create in the end.
        finalfilename = ""
        while (len(finalfilename) < 1):
            finalfilename = input("Finally, enter the URL of the file you would like created. The number of the frame of each image will be attached as a suffix to the name: ")
        if(len(finalfilename) < 5):
            finalfilename += ".png"
        if(not(finalfilename[len(finalfilename) - 4:] == ".png")):
            finalfilename += ".png"

        #now we shall start the process!
        def is_within_image(point):
            return ((0 <= point.x < width) and (0 <= point.y < height))

        def image_within_dir(point, direc, timeout):
            while timeout > 0:
                timeout -= 1
                point += direc
                if(is_within_image(point)):
                    return True
            return False


        #find the two perpendiculars
        if direction.x is 0:
            perp1 = Vector2D(1,0)
            perp2 = Vector2D(-1,0)
        elif direction.y is 0:
            perp1 = Vector2D(0,1)
            perp2 = Vector2D(0,-1)
        else:
            perp1 = Vector2D(direction.x, -direction.y)
            perp2 = Vector2D(-direction.x, direction.y)

    #find length of our traversion and thus gradient.
        traversion_left = 0

        current = Vector2D(initial.x, initial.y)
        while (is_within_image(current)):
            traversion_left += 1
            current += direction

        current = [initial[0], initial[1]]

        #now extend traversion left, because image may not be a box.
        curperp = perp1

        proper_traversion = traversion_left

        print(proper_traversion)

        validperp = curperp

        for i in range(0,2):
            if(i == 1 and traversion_left == proper_traversion):
                curperp = perp2
                validperp = perp2
            test_point = (initial + direction * (traversion_left + 1))
            timeout = 1
            while image_within_dir(test_point, curperp, timeout):
                traversion_left += 1
                timeout += 1
                test_point = [test_point[0] + direction[0], test_point[1] + direction[1]]

        print(traversion_left)

        #now the fun part :)

        for i in range(0, traversion_left + 1):
            for j in range(0 , 2):
                if(j == 0)
                    current = Vector2D(initial.x + direction.x * i, initial.y)
                else:
                    current = Vector2D(initial.x, initial.y + direction.x * i)

            if :

            else:



    #END----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #END----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #END----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #END----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #END----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #END----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #save the file and reiterate.
    print("------------------------------------------------------------")
    print("Thanks for choosing us! Restarting from the start of the program")
