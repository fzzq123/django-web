# start from an official image
FROM djangobase
  
# arbitrary location choice: you can change the directory
RUN mkdir -p /opt/services/djangoapp/src
WORKDIR /opt/services/djangoapp/src

ADD requirements.txt /opt/services/djangoapp/src/
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
ADD . /opt/services/djangoapp/src/
 
# expose the port 8000
EXPOSE 8000

# define the default command to run when starting the container
CMD ["gunicorn", "--chdir", "djangoProject", "--bind", "0.0.0.0:8000", "djangoProject.wsgi:application", "--reload"]
