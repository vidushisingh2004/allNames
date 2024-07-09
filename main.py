import string

#finds songs with a particular name and puts them in outputfile
def findName(name, outputFile):
  allNames = open("allNames.csv", "r")#opens file
  output = open(outputFile, "w")  #opens output file
  output.write("Artist,Song,Year\n")  #writes header in output file
  songlist = []  #creates an empty list to put songs with the name into
  next(allNames)  #skips header
  for aline in allNames:  #loops through allNames
    fields = (aline.strip()).split("\t") #breaks the string into a list
    if fields[-1] == name:  
      repeat = False    #the song is not repeated (initialized value)
      for i in songlist:
        if i == fields[1]:
          repeat = True   #the song is repeated
      if (repeat==False):   
        songlist.append(fields[1])   #adds songs that contain this name into 
        output.write(fields[0] + "," + fields[1] + "," + fields[3] + "\n")  #writes information in output file
  allNames.close()
  output.close()   #close files

#finds songs with names that are repeated a threshold number of times and puts them in outputfile
def findRepeatedNameSongs(threshold, outputfile):
  allNames = open("allNames.csv", "r")#opens files
  output = open(outputfile, "w")
  output.write("Name,Times,Artist,Song\n")   #writes header
  namedict = {}   #creates empty dictionary
  next(allNames)  #skips header
  for aline in allNames:
    fields = (aline.strip()).split("\t")   #breaks the string into list
    repeat = False    #repeat 
    for i in namedict:
      if fields[1]==i:  #fields[1]=song
        if (fields[-1]==namedict[i][0]) and (fields[0]==namedict[i][2]):   #if the song and name are already in namedict
          repeat = True  #it is a repeated name
          namedict[i][1] += 1   #adds one to count of repeats
    if (repeat==False):   #it is a new name
      namedict[fields[1]] = [fields[-1],1,fields[0],fields[1]]   #adds info into dictionary: key = song, values = name, times, artist, song
  for i in namedict.values():  #loops through values of namedict
    if i[1] >= threshold:    
      output.write(i[0] + "," + str(i[1]) + "," + i[2] + "," + i[3] + "\n")   #writes information into output file
  allNames.close()
  output.close()   #close files

# finds all the songs which contain at least threshold occurrences of distinct names (mentioned at least once)
def findUniqueNameSongs(threshold, outputfile):
  allNames = open("allNames.csv", "r") #opens file for reading purpose
  output = open(outputfile, "w") #opens an output file for writing purpose
  output.write("Number,Artist,Song\n")
  namedict = {} #creates an empty dictionary
  next(allNames)  #skips header
  for aline in allNames:
    fields = (aline.strip()).split("\t") #strips and splits the file into lines, which are lists
    repeatsong = False
    for i in namedict:
       if (fields[1]==i) and (fields[0]==namedict[i][1]):  #fields[1]=song(the kes of the dictionary are the song names)
          repeatsong = True
          if fields[-1] not in namedict[i][0]: #if the name is not in the list of all the names mentioned in the song
            namedict[i][0].append(fields[-1])  #add the name to the list       
    if (repeatsong==False):
      namedict[fields[1]] = [[fields[-1]],fields[0]]  #name, artist when only one name is mentioned
  for i in namedict:
    if len(namedict[i][0]) >= threshold: #if the length of the list containing all the mentioned names is >= to treshold
      output.write(str(len(namedict[i][0])) + "," + namedict[i][1] + "," + str(i) + "\n")      
  allNames.close()
  output.close()   #closes files

#counts the number of unique songs in a decade that include a specific name 
def countNameDecades(name, outputfile):
  output = open(outputfile, "w")
  output.write("number,decade\n")
  allNames = open("allNames.csv", "r")#opens file
  decade = {'1970s':0, '1980s':0,'1990s':0,'2000s':0,'2010s':0}
  songlist = [] #an empty list
  next(allNames) # skips header
  for aline in allNames:
    fields = (aline.strip()).split("\t")#string is converted to a list
    try:#The try block allows you to test a section of code for errors.
      year = int(fields[3]) # the years in field[3] are converted to an integer and assigned to the variable year
      repeat = False
    except ValueError: #some of the songs do not have a year so it skips those
      continue 
    if fields[-1] == name:  # the first from the right is the name
      for i in songlist:
        if (i==fields[1]): # i == song to check if the songs is already in the songlist
          repeat = True     
      if (repeat==False):  #if repeat== false follow the conditions below.
        songlist.append(fields[1]) #song is added to the list of songs
        if (year>=1970) and (year<=1979): 
          decade["1970s"] += 1 #adds 1 to the dictionary evertime the name occurs
        elif (year>=1980) and (year<=1989):
          decade["1980s"] += 1 #adds 1 to the dictionary evertime the name occurs
        elif (year>=1990) and (year<=1999):
          decade["1990s"] += 1#adds 1 to the dictionary evertime the name occurs
        elif (year>=2000) and (year<2010):
          decade["2000s"] += 1#adds 1 to the dictionary evertime the name occurs
        elif (year>=2010) and (year<=2019):
          decade["2010s"] += 1 #adds 1 to the dictionary evertime the name occurs
  for i in decade:
    output.write(str(decade[i])+ ","+ str(i) + "\n")
  output.close()
  allNames.close()   #closes files

#creates a dictionary with keys as the letters in the alphabet and values of zero
def createletterdict():
  dict = {}    
  for i in string.ascii_uppercase:   #loops through all uppercase letters
    dict[i]=0
  return dict
  
#counts the number of unique names that start with each letter and compares percentages of names between names that appear in songs and names used in the US
def countStartLetter(outputfile):
  allNames = open("allNames.csv","r")  #open files
  onlyNames = open("onlyNames.csv","r")
  output = open(outputfile,"w")
  songdict = createletterdict()  #creates initial dictionaries
  usdict = createletterdict()
  output.write("letter,proportion\n")  #writes headers in output file
  namelist = []    #creates empty list for names
  next(allNames)   #skips header
  for aline in allNames:
    fields = (aline.strip()).split("\t")   #splits line into list
    startletter = (fields[-1][0]).upper()   #start letter = first letter of name
    repeatname = False   
    for name in namelist:
      if fields[-1]==name:  #checks if name is in namelist already
        repeatname = True    
    if repeatname == False:    #if it is not a repeated name
      songdict[startletter]+=1   #increases count for start letter of the name
      namelist.append(fields[-1])   #adds name to namelist
  next(onlyNames)    #skips header
  countlines = 0     #initializes count of lines at zero
  for aline in onlyNames:
    fields = (aline.strip()).split("\t")   #splits line into list
    startletter = (fields[0][0]).upper()   #start letter = first letter of name
    usdict[startletter]+=1    #increases count for start letter of the name
    countlines +=1    #counts the number of names
  for akey in songdict:
    songpercent = (songdict[akey]/len(namelist))*100    #(number of names with start letter/number of unique names)*100 to make it a percentage
    uspercent = (usdict[akey]/countlines)*100 
    output.write(akey + "," + str(songpercent-uspercent)+"\n") #negative proportion means start letter appears more in names than songs, positive means start letter appears more in songs than names
  allNames.close()
  onlyNames.close()  #close files


#counts the number of unique names that end with each letter and compares percentages of names between names that appear in songs and names used in the US
def countEndLetter(outputfile):
  allNames = open("allNames.csv","r")   #opens files
  onlyNames = open("onlyNames.csv","r")
  output = open(outputfile,"w")
  songdict = createletterdict()    #creates initial dictionaries
  usdict = createletterdict()
  output.write("letter,proportion\n")   #writes headers in output file
  namelist = [] 
  next(allNames)
  for aline in allNames:
    fields = (aline.strip()).split("\t")   #splits line into list
    endletter = (fields[-1][-1]).upper()    #endletter = last letter of name
    repeatname = False
    for name in namelist:   
      if fields[-1]==name:    #checks if name is in namelist already
        repeatname = True
    if repeatname == False:   #if it is not a repeated name
      songdict[endletter]+=1     #increases count for last letter of the name
      namelist.append(fields[-1])   #adds the new name to namelist
  next(onlyNames)   #skips header
  countlines = 0    #initializes count of lines at zero
  for aline in onlyNames:
    fields = (aline.strip()).split("\t")  #splits line into list
    endletter = (fields[0][-1]).upper()     #endletter = last letter of name
    usdict[endletter]+=1     #increases count for last letter of the name
    countlines +=1   #counts the number of names
  for akey in songdict:
    songpercent = (songdict[akey]/len(namelist))*100   #(number of names with start letter/number of unique names)*100 to make it a percentage
    uspercent = (usdict[akey]/countlines)*100
    output.write(akey + "," + str(songpercent-uspercent)+"\n") #negative proportion means end letter appears more in names than songs, positive means end letter appears more in songs than names
  allNames.close()
  onlyNames.close()
  output.close()   #closes files

#main function that tests functions
def main():
  #tests for findName function
  findName("Jack", "tests/jack.csv")
  findName("Mary", "tests/mary.csv")
  findName("Peter", "tests/peter.csv")
  #tests for findRepeatedNameSongs function
  findRepeatedNameSongs(40,"tests/repeat.40.csv")
  findRepeatedNameSongs(30,"tests/repeat.30.csv")
  findRepeatedNameSongs(20,"tests/repeat.20.csv")
  #tests for findUniqueNameSongs function
  findUniqueNameSongs(15, "tests/unique.15.csv")
  findUniqueNameSongs(20, "tests/unique.20.csv")
  #tests for countNameDecades function
  countNameDecades("Mary", "tests/mary.decade.csv")
  countNameDecades("Joe", "tests/joe.decade.csv")
  countNameDecades("Mary Anne", "tests/name_of_choice.decade.csv")
  #tests for countStartLetter and countEndLetter functions
  countStartLetter("tests/names.start.csv")
  countEndLetter("tests/names.end.csv")

#runs main function
main()