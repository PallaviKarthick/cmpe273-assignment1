from flask import Flask
from github import Github
import sys
import re


app = Flask(__name__)
try:
    if (len(sys.argv) == 2):
        
        url = sys.argv[1]
        str_array = url.split('/')

        # repository name
        # print str_array[-1]
        repositoryName = str_array[-1]

       # Github credentials
        git = Github("pallavikarthick", "Github12#")
        repo = git.get_user().get_repo(repositoryName)
       
    else:
        sys.exit("Plase enter the Github Respository URL!!")
except IndexError:
    sys.exit("Plase enter the Github Respository URL!!")

@app.route("/", methods=['GET'])
def hello():
    return "Hello from Dockerized Flask App!!"

@app.route("/v1/<string:fileName>", methods=['GET'])
def v1(fileName):
    for file in repo.get_dir_contents('/'): 
        if file.type == "file":
            #temp variable to hold filename
            file_Name = file.name 
            jsonFormat = False

            if file_Name.endswith(".yml") or file_Name.endswith(".json") :
                #remove the .yml and .json extension for the file name from respository
                file_Name = re.sub(r'\..*',"",file_Name)
                
                tempFileName = fileName
                 #remove the .yml and .json extension for the file name from the URL
                tempFileName = re.sub(r'\..*',"",tempFileName)

                #check if the file name from URL matchs with the file name in the respository( apart from extensions)
                if file_Name == tempFileName:
                    if fileName.endswith(".json"):
                        jsonFormat = True
                        fileName = tempFileName + ".yml"

                    fileName = '/' + fileName
                    file =  repo.get_file_contents(fileName)
                    file_content = file.decoded_content
                    
                    if jsonFormat: 
                        jsonFormat = False
                        file_content = "{ \n" + file_content + "\n}"
                        return file_content

                    else:
                        return file_content
                        
                          

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')