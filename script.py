"""
ENSIAS C Project Code Generator: Conceived and implemented by: ALAOUI Mehdi. 2016. All Rights Reserved.
"""
import sys
import re
#Class to define colors in Terminal
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
#Function that prints help
def printHelp():
    print(bcolors.WARNING+bcolors.BOLD+"Notes:"+bcolors.ENDC+" - Works only with python 3.3 or later version")
    print("       - The input file is a header file that should contain all structures used in your project")
    print("\n"+bcolors.OKGREEN+bcolors.BOLD+"Execution Command:"+bcolors.ENDC+" pythonVersion script.py input_header_file")
    print("\n\t"+bcolors.UNDERLINE+"Example:"+bcolors.ENDC+" python3.5 script.py test.h")
    print("\n"+bcolors.FAIL+bcolors.BOLD+"IMPORTANT:"+bcolors.ENDC+" - Structures must contain no pointers inside")
    print("\t     (even the pointer into the next structure, it will be added automatically)")
    print("\t   - Delete all comments before processing")
    print("\t   - Delete all spaces between Structure name and brackets ({,})")
    print("\t     (typedef struct Player{ not typedef struct Player {)")
    print("\n"+bcolors.OKGREEN+bcolors.BOLD+"Input Header Content Example:"+bcolors.ENDC)
    print("\n\ttypedef struct Player{\n")
    print("\t\tchar Name[30];\n")
    print("\t\tint Age;\n")
    print("\t\tint TotalScore;\n")
    print("\t}Player;\n\n")

#Functions that parse input file
def checkArgument(): #Function that checks script arguments
    try:
        if(str(sys.argv[1]) in ["-h","--help"]):
            printHelp()
        elif ("h" not in (str(sys.argv[1]).split(".")[1:])):
            print(bcolors.FAIL+bcolors.BOLD+"Error: "+bcolors.ENDC +"The argument given is not a header file\n")
            print("For help, run the script with -h or --help as input\n\n")
        else:
            try:
                fileContent = "".join(open(str(sys.argv[1]), "r").readlines()).split("typedef struct ")[1:]
                return fileContent
            except:
                print(bcolors.FAIL+bcolors.BOLD+"Error: "+bcolors.ENDC +"File unreadable\n\n")
                print("For help, run the script with -h or --help as input\n\n")

    except:
        print(bcolors.FAIL+bcolors.BOLD+"Error: "+bcolors.ENDC +"Give an argument to the script\n\n")
        print("For help, run the script with -h or --help as input\n\n")

def getStructures(fileContent): #Function that returns a structured list of input structures
    structures=[]
    for i in range(0, len(fileContent)):
        name = fileContent[i].split("{")[0]
        fileContent[i] = ([name, (fileContent[i].split(name + ";")[0]).split(name)[1]])
        structures.append([fileContent[i][0], [getField(i) for i in fileContent[i][1].split(";")[:-1]]])
    return structures

def getField(INPUT_STR):#We use Regex to filter field name and field type from a string
    INPUT_STR = str(INPUT_STR)
    exp2="((\n)|(\t)| |(\r))*([a-z]{3,5}((\**)))((\n)|(\t)| |(\r))*([A-Za-z][A-Za-z0-9_]*)(\[[0-9]*\])*((\n)|(\t)| |(\r))*"
    result=re.search(exp2, INPUT_STR)
    if(result):
        type=result.group(5)
        nom=result.group(12)
        if(result.group(13) != None):
            type+="*"
        return (nom,type)
#=====================================================================================================
#Functions that generate content for functions

def initStructure(structureName):
    content=structureName + "* init" + str(structureName).capitalize() + "(){\n\n\t" + structureName + "* new_pointer=(" + structureName + " *)malloc(sizeof(" + structureName + "));\n\tnew_pointer->next=NULL;\n\treturn new_pointer;\n}\n"
    return content

def loadWriteFile(structureName):
    content = structureName + "* load" + str(structureName).capitalize() + "FromFile(char* FileName){\n\n"
    content+="\tFILE * fichier = NULL;\n\t"+structureName+"* Liste = NULL;\ntfichier = fopen(FileName, \"rb\"); \n"
    content+="\tif (fichier == NULL){ \n\t\tprintf(\"Le fichier  est inexistant\\n\");\n\t}\n\telse{\n\t\tprintf(\" Chargement des données réussi \\n\");\n\t\t"+structureName+"* pointer=NULL, * previous=NULL;\n"
    content+="\t\tif (feof(fichier) == 0){\n\t\t\tpointer=("+structureName + " * )malloc(sizeof("+structureName+"));\n"
    content+="\t\t\tfread (pointer, sizeof("+structureName+ "), 1, fichier);\n\t\t\tprevious=pointer;\n\t\t\tListe=pointer;\n\t\t}\n\t\twhile (pointer->next != NULL){\n\t\t\tpointer=("+structureName +" * )malloc(sizeof("+structureName +"));\n"
    content+="\t\t\tfread (pointer, sizeof("+structureName +"), 1, fichier);\n\t\t\tprevious->next=pointer;\n\t\t\tprevious=pointer;\n\t\t}\n\t\tpointer->next = NULL;\n"
    content+="\t\tfclose(fichier);\n\t}\n\treturn Liste;\n}\nvoid write" + str(structureName).capitalize() + "InFile(char *fileName," + structureName + "* liste){\n\n\tFILE *fichier=fopen(fileName,\"wb\");\n\n"
    content+="\t" + structureName + " *pointer=liste;\n\n\twhile(pointer!=NULL){\n\t\tfwrite (pointer, sizeof(" + structureName + "),1, fichier);\n\t\tpointer=pointer->next;\n\t}\n\tprintf(\"Modifications enregistrées\\n\");\n\tfclose(fichier);\n}\n"
    return content

def insertTopEndReverse(structureName):
    content=structureName+"* insert"+str(structureName).capitalize()+"Top("+structureName+"* List, "+structureName+"* element){\n\n\telement->next=List;\n\treturn element;\n}\n"
    content+=structureName+"* insert"+str(structureName).capitalize()+"End("+structureName+"* List, "+structureName+"* element){\n\n\tif(List==NULL)\n\t\treturn element;\n\n\t"+structureName+"* Pointer=List;\n\twhile(Pointer->next!=NULL)\n\t\tPointer=Pointer->next;\n\tPointer->next=element;\n\treturn List;\n}\n"
    content+=structureName+"* reverse"+str(structureName).capitalize()+"List("+structureName+"* List){\n\n\t"+structureName+" *ptr=List,*pivot=List,*head=List;\n\twhile(head->next!=NULL){\n\t\tpivot=head->next;\n\t\thead->next=pivot->next;\n\t\tpivot->next=NULL;\n\t\tList=insert"+str(structureName).capitalize()+"Top(List,pivot);\n\t}\n\treturn List;\n}\n"
    return content

def insertByField(structureName,fieldName,fieldType):
    content = structureName + " * insert" + str(structureName).capitalize() + "By" + str(fieldName).capitalize() + "(" + structureName + " * List, " + structureName+" * element, int order){\n\n"
    content += "\tif(List == NULL)\n\t\treturn element;\n\n"
    content += "\tif(!order){ // Descending order\n\t\tList = reverse"+str(structureName).capitalize()+"List(List);\n\t}\n"
    if(fieldType in ["char*","char *"]):
        content += "\tif(strcmp(element->" + fieldName + ", List->" + fieldName + ")<=0){"" "
    else:
        content += "\tif(element->" + fieldName + " <= List->" + fieldName + "){"" "
    content+="\n\t\tList = insert" + str(structureName).capitalize() + "Top(List, element);\n\t}\n"
    content += "\telse{\n\t\t" + structureName + " * pointer = List, *previous = List;\n"
    content += "\t\twhile(pointer != NULL && "
    if (fieldType in ["char*", "char *"]):
        content+="strcmp(pointer->" + fieldName + ", element->" + fieldName + ") < 0)"
    else:
        content += "pointer->" + fieldName + " < element->" + fieldName + ")"
    content+="{\n\t\t\tprevious = pointer;\n\t\t\tpointer = pointer->next;\n\t\t}\n"
    content += "\t\tif(pointer == NULL){\n\t\t\tprevious->next = element;\n\t\t}\n"
    content += "\t\telse{\n\t\t\telement->next = pointer;\n\t\t\tprevious->next = element;\n\t\t}\n\t}\n"
    content += "\tif(!order){ // Descending order\n\t\tList = reverse"+str(structureName).capitalize()+"List(List);\n\t}\n\treturn List;\n}\n"
    return content

def findByField(structureName,fieldName,fieldType):
    content=structureName+"* find"+str(structureName).capitalize()+"By"+str(fieldName).capitalize()+"("+structureName+"* List, "+fieldType+" ValueToFind){\n\n"
    content+="\t"+structureName+"* pointer=List;\n"
    content+="\twhile(pointer!=NULL && "
    if (fieldType in ["char*", "char *"]):
        content += "strcmp(pointer->" + fieldName + ",ValueToFind)!=0"
    else:
        content += "pointer->" + fieldName + "!=ValueToFind"
    content+="){\n"
    content+="\t\tpointer=pointer->next;\n"
    content+="\t}\n"
    content+="\treturn pointer;\n}\n"
    return content

def delete(structureName):
    content=structureName+"* delete"+str(structureName).capitalize()+"FromList("+structureName+"* List,"+structureName+"* element){\n\n"
    content+="\tif(element==NULL)\n"
    content+="\t\treturn List;"
    content+="\tif(element==List){\n\t\tList=List->next;\n\t\tfree(List);\n\t}\n"
    content+="\telse{\n"
    content+="\t\t"+structureName+"* pointer=List;\n"
    content+="\t\twhile(pointer!=NULL && pointer->next!=element){\n\t\t\tpointer=pointer->next;\n\t\t}\n"
    content+="\t\tif(pointer!=NULL){\n\t\t\tpointer->next=element->next;\n\t\t\tfree(element);\n\t\t}\n\t}\n"
    content+="\treturn List;\n}\n"
    return content
#======================================================================================================

#Main Program

print("\n\n\n")
print(bcolors.BOLD+bcolors.OKBLUE+"ENSIAS C Project Code Generator"+bcolors.ENDC)
print("Conceived and implemented by: "+bcolors.OKGREEN+"ALAOUI Mehdi."+bcolors.ENDC)
print(bcolors.UNDERLINE+"Copyright 2016. ENSIAS. All Rights Reserved."+bcolors.ENDC)
print("\n")
fileContent=checkArgument()
if(fileContent):
    print(">> Reading structures..")
    structures = getStructures(fileContent)
    structureNameArray=[]
    mainFile = open("main.c","w")
    structureFile = open("structures.h", "w")
    makeFile=open("makefile","w")
    mainFile.write("#include \"structures.h\"\n")
    structureFile.write("#include <stdio.h>\n")
    structureFile.write("#include <stdlib.h>\n")
    structureFile.write("#include <string.h>\n\n\n")
    for element in structures:

        structureName=element[0]
        print(">>\t",structureName,"structure..")
        structureNameArray.append(structureName)
        file=open(structureName+".c","w")
        headerFile = open(structureName + ".h", "w")
        file.write("#include \"" + structureName + ".h\"\n\n\n")
        headerFile.write("#include \"structures.h\"\n\n")
        headerFile.write("#define DESC 0\n#define ASC 1\n\n\n")
        headerFile.write("/*\n\n")
        headerFile.write("> La fonction init" + str(structureName).capitalize() + "() alloue la mémoire et retourne l'adresse correspondante (initialise la structure\n\n")
        headerFile.write("> La fonction load" + str(structureName).capitalize() + "FromFile() charge les données  dans une liste chainée depuis le fichier donné en paramètre\n\n")
        headerFile.write("> La fonction write" + str(structureName).capitalize() + "InFile() stock la liste chainée passée en paramètre dans le fichier passé en paramètre\n\n")
        headerFile.write("> La fonction insert"+str(structureName).capitalize()+"Top() insère l'élément voulu au début de la liste\n\n")
        headerFile.write("> La fonction insert" + str(structureName).capitalize() + "End() insère l'élément voulu à la fin de la liste\n\n")
        headerFile.write("> La fonction delete" + str(structureName).capitalize() + "FromList() supprime l'élément donné en paramètre de la liste\n\n")
        headerFile.write("> Les fonctions insert" + str(structureName).capitalize() + "ByX() insère l'élément dans la liste par ordre selon le champ X, le paramètre order accepte ASC et DESC comme valeur (ASC: a->z et 0->9 et DESC: z->a et 9->0)\n\n")
        headerFile.write("> Les fonctions find" + str(structureName).capitalize() + "ByX() recherche un élément dans la liste donnée, la recherche se fait par le champ X. Si l'élément se trouve, la fonction retourne son adresse, sinon NULL\n\n")
        headerFile.write("P.S: Il y'a autant de fonctions find" + str(structureName).capitalize() + "ByX() et insert" + str(structureName).capitalize() + "ByX() que de champs de la structure\n\n")
        headerFile.write("*/\n\n")
        headerFile.write(structureName + "* init" + str(structureName).capitalize() + "();\n")
        headerFile.write(structureName + "* load" + str(structureName).capitalize() + "FromFile(char* FileName);\n")
        headerFile.write("void write" + str(structureName).capitalize() + "InFile(char *fileName," + structureName + "* liste);\n")
        headerFile.write(structureName+"* insert"+str(structureName).capitalize()+"Top("+structureName+"* List, "+structureName+"* element);\n")
        headerFile.write(structureName+"* insert"+str(structureName).capitalize()+"End("+structureName+"* List, "+structureName+"* element);\n")
        headerFile.write(structureName+"* reverse"+str(structureName).capitalize()+"List("+structureName+"* List);\n")
        headerFile.write(structureName + "* delete" + str(structureName).capitalize() + "FromList(" + structureName + "* List," + structureName + "* element);\n")
        file.write(loadWriteFile(structureName))
        file.write(initStructure(structureName))
        file.write(insertTopEndReverse(structureName))
        file.write(delete(structureName))
        for field in element[1]:
            (fieldName,fieldType)=field
            print(">>\t\tfield:",fieldName,fieldType)
            headerFile.write(structureName + " * insert" + str(structureName).capitalize() + "By" + str(fieldName).capitalize() + "(" + structureName + " * List, " + structureName + " * element, int order);\n")
            headerFile.write(structureName + "* find" + str(structureName).capitalize() + "By" + str(fieldName).capitalize() + "(" + structureName + "* List, " + fieldType + " ValueToFind);\n")
            file.write(insertByField(structureName,fieldName,fieldType))
            file.write(findByField(structureName, fieldName, fieldType))


        headerFile.close()
        file.close()

    makeFile.write("executable: bin/main.o ")
    for e in structureNameArray:
        makeFile.write("bin/"+e+".o ")
    makeFile.write("\n\tgcc bin/main.o ")
    for e in structureNameArray:
        makeFile.write("bin/"+e+".o ")
    makeFile.write("-o executable\n")
    makeFile.write("bin/main.o: main.c structures.h\n\tgcc -c main.c -o bin/main.o\n")
    for e in structureNameArray:
        makeFile.write("bin/"+e + ".o: " + e + ".c " + e + ".h structures.h\n\tgcc -c " + e + ".c -o bin/"+e + ".o\n")
    makeFile.close()
    mainFile.write("\n\nint main(){\n\n\tprintf(\"Hello, ENSIAS!\\n\");\n\n\treturn 0;\n}")
    mainFile.close()
    print(">> Generating Files..")
    print(">> Generating Main File..")
    print(">> Generating Structures Files..")
    print(">> Generating Makefile File..")

    structures=("".join(open(str(sys.argv[1]), "r").readlines())).split("\n")
    structureFile.write("#define DESC 0\n#define ASC 1\n\n\n")
    structureName=""
    for element in structures:
        if(element=="" or element=="\n"):
            None
        elif(element[0:7]=="typedef"):
            structureName=(element.split("typedef struct ")[1]).split("{")[0]
            structureFile.write("\n\n")
        elif(element[0]=="}"):
            structureFile.write("struct "+structureName+"* next;\n")
        structureFile.write(element+"\n")
    structureFile.close()
