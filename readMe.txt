1.
open terminal on system root
docker-compose up --build

if any issue use :
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker-compose up --build

2.
open another ternminal :
cd frontend
npm install
npm run dev

3.Go to in browser 
http://localhost:5175/

login

admin
email: chathura@gmail.com
password: 1234

student
email: kalana@gmail.com
password: 1234

faculty
email: sewmini@gmail.com
password: 1234


check this for more
https://github.com/Kalana2/NexusEnroll.git