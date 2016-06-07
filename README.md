# virus-total-helper

Jak odpalić projekt
-------------------
1. ściagamy pythona 3.4, dla ubuntu: 
    * sudo apt-get install python3.4
2. (opcjonalny) ściagamy virtualenv i virtualenvwrapper i tworzymy wirtualne środowiska dla pythona:
    * sudo pip install virtualenv
    * sudo pip install virtualenvwrapper
    * export WORKON_HOME=~/Envs
    * mkdir -p $WORKON_HOME
    * source /usr/local/bin/virtualenvwrapper.sh
    * mkvirtualenv tin --python=python3.4
    * żeby odpalic wirtualne srodowisko o nazwie tin:
        * workon tin
  
3. ściągamy gita, dla ubuntu: 
    * sudo apt-get install git
4. ściagamy projekt
    * tworzymy nowy folder, w ktorym bedzie projekt:
        * mkdir tin
        * cd tin
    * klonujemy repozytorium
        * git clone https://github.com/mwalercz/virus-total-helper
5. instalujemy biblioteki pythona3.4, ktore bedą nam potrzebne (jesli nie uzywamy virtualenvwrappera to trzeba dac sudo, 
jesli uzywamy wrappera to należy upewnić się że jesteśmy na srodowisku wirtualnym (w konsoli z lewej strony powinien widnieć napis (tin) - jeśli nie, wpisujemy: workon tin))
    * cd virus-total-helper
    * [sudo] pip3.4 install -r requirements.txt
6. żeby odpalić serwer wywołujemy:
    * ./bin/virustotal
    * możliwe, że trzeba plikowi virustotal nadać uprawnienia do wykonywania, w takim wypadku
    * chmod +x bin/virustotal
7. domyślnie serwer jest widoczny pod localhost:5005
8. w pliku config.ini możemy zmienić nazwę hosta, port, miejsce przechowywania logów oraz miejsce do którego będą zapisywane pliki html.
9. po zmianie pliku config należy wyłączyć i ponownie włączyć aplikacje -> aplikacja reaguje na SIGINT (ctrl+c)



    
 
    
    