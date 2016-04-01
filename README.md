# virus-total-helper

Jak odpalić projekt
-------------------
1. ściagamy pythona 3.4, dla ubuntu: 
    * sudo apt-get install python3.4
2. (opcjonalny) ściagamy virtualenv i virtualenvwrapper:
    * pip install virtualenv
    
    * pip install virtualenvwrapper
    * export WORKON_HOME=~/Envs
    * mkdir -p $WORKON_HOME
    * source /usr/local/bin/virtualenvwrapper.sh
    * mkvirtualenv tin
    * żeby odpalic wirtualne srodowisko o nazwie tin:
        * workon tin
  
3. ściągamy gita, dla ubuntu: 
    * sudo apt-get install git
4. (opcjonalny) ściagamy gui do gita np smartgit: http://www.syntevo.com/smartgit/download
w środku jest smartgit.sh ktory sluzy do odpalania aplikacji
5. ściagamy projekt
    * tworzymy nowy folder, w ktorym bedzie projekt:
        * mkdir tin
        * cd tin
    * klonujemy repo:
        * git clone https://github.com/mwalercz/virus-total-helper
6. instalujemy biblioteki pythona3.4, ktore bedą nam potrzebne (jesli nie uzywasz virtualenvwrappera to trzeba dac sudo, 
jesli uzywasz wrappera to upewnij sie ze pracujesz na srodowisku wirtualnym: workon tin)
    * cd virus-total-helper
    * [sudo] pip install -r requirements
7. żeby sprawdzic czy dziala:
   * z virtualenvwrapperem:
       * python -m unittest
   * bez virtualenvwrappera:
       * python3.4 -m unittest       
   * Powinno powiedziec nam ze co najmniej jeden test zostal odpalony
8. żeby odpalić aplikacje:
 * python/python3.4 app
 * Odpala nam to co jest w app.__main__.py
 
Praca nad projektem
-------------------
Bedąc w glownym folderze projektu
1. pullujemy z gita nowości:
* git pull
2. uruchamiamy testy jw - jak cos nie dziala to sprawdzamy kto ostatnio commitowac i kazemy mu poprawic
3. dla kazdej nowej klasy tworzymy folder w app
4. kodzimy wg oficjalnego stylu pythona https://www.python.org/dev/peps/pep-0008/
5. dla kazdej stworzonej przez nas klasy piszemy testy!!!
6. uruchamiamy testy
7. jesli wsjo dziala to robimy commit i push
    
Jak pisać testy
---------------
Testy piszemy w katalogu test, korzystamy z podstawowej biblioteki pythona unittest. Dla kazdego modulu tworzymy nowy plik.
Wszystkie nazwy plików testowych musza zaczynac sie na "test", np "test_default.py".
Jesli w app stworzymy modul o nazwie "scheduler.py" to w test tworzymy plik o nazwie "test_scheduler.py".
Zeby odpalić wszystkie testy musimy byc w glownym folderze (virus-total-helper):
* python -m unittest
    lub
* nose2
    
Mozna sobie to wszystko ustawic w pycharmie w edit configurations: python test

    
 
    
    