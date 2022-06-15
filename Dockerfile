FROM python

#Ambil File
ADD setup.py .

#Instal lewat file txt
COPY requirements.txt .
RUN pip install -r requirements.txt

CMD [ "python", "./setup.py" ]


############## TUTORIAL MENJALANKAN ##############

#Building requirements.txt
# docker build -t python-followers-scrab .

#Running
# docker run -t -i python-followers-scrab