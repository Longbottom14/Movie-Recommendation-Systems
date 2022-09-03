#base image from dockerhub .the base image is python 3.8 ,debian based , 
#slim because its optimised and small sized
FROM python:3.8.13-slim

#install pipenv on the image
RUN pip install pipenv

#create an 'app' directory is if it doesnt exist and cd there so that its the working directory
WORKDIR /app

#copy the 'pipfile' ,'pipfile.lock' files into the present directory i.e 'app'
COPY ["Pipfile", "Pipfile.lock", "./"]

#install all libary in pipfile.lock file but do not create virtual environment
RUN pipenv install --system --deploy

#copy 'streamlit_app.py' ,"shawshank.jpg" files into working directory i.e 'app' 
COPY ["streamlit_app.py","shawshank.jpg", "./"]

#used to download package information from all configured sources
#“apt-get update” updates the package sources list to get the latest list of available
# packages in the repositories 
# “apt-get upgrade” updates all the packages presently installed in our 
#Linux system to their latest versions.
RUN apt-get update

#during test..i got an error
#OSError: libgomp.so.1: cannot open shared object file: No such file or directory
#RUN  apt-get install libgomp1

#copy artifacts folder to artifacts folder on the container
COPY ["artifacts", "./artifacts/"]

#expose port '8501' of the container to the local system/machine
EXPOSE 8501

#entrypoint is the default command that is executed when we do docker run
#>> streamlit run app.py
ENTRYPOINT ["streamlit", "run"]

# run app.py with gunicorn
CMD ["streamlit_app.py"]




#++++++++++++++++++++++++++cmd:+++++++++++++++++++++++++++++++++++++++++++
#build dockerfile
#>> docker build -t "image_name" .
# the dot specifies that the dockerfile is in the directory

#run dockerfile
#>> docker run -it --rm -p 8501:8501 "image_name" 
#-it : tell docker we wanna access the termianal
#--rm : remove image after running / we dont wanna keep it
#-p : p means port and it is used for port mapping
#9696:9696 : the first 9696 is the port exposed on the container
#             the second 9696 is the port to be running on the local machine i.e localhost/9696

#check running containers
#>> docker ps

#+++++++++++++++++++++++important docker commands on command promt++++++++++++++++++++++


#>> docker run -it --rm python:3.8.13-slim
#-it : tell docker we wanna access the termianal
#--rm : remove image after running / we dont wanna keep it
#the default entry point is python i.e a python shell is created
#entrypoint is the default command that is executed when we do docker run

#>> docker run -it --rm --entrypoint=bash python:3.8.13-slim
#-it : tell docker we wanna access the termianal
#--rm : remove image after running / we dont wanna keep it
#entry point is bash i.e bash kernel is created
#entrypoint is the default command that is executed when we do docker run


