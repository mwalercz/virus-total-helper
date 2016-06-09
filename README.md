# virus-total-helper

Jak uruchomić serwer
-------------------
1. ściagamy pythona 3 dla ubuntu oraz pip dla pythona3
    * sudo apt-get install python3
    * sudo apt-get install python3-pip
3. ściągamy gita, dla ubuntu: 
    * sudo apt-get install git
4. ściagamy projekt
    * tworzymy nowy folder, w ktorym bedzie projekt:
        * mkdir tin
        * cd tin
    * klonujemy repozytorium
        * git clone https://github.com/mwalercz/virus-total-helper
5. instalujemy biblioteki pythona3, ktore bedą nam potrzebne (jesli nie uzywamy virtualenvwrappera to trzeba dac sudo, 
jesli uzywamy wrappera to należy upewnić się że jesteśmy na srodowisku wirtualnym (w konsoli z lewej strony powinien widnieć napis (tin) - jeśli nie, wpisujemy: workon tin))
    * cd virus-total-helper
    * [sudo] pip3 install -r requirements.txt
6. żeby odpalić serwer wchodzimy do katalogu bin (uwaga, istotne jest żeby zrobić to z katologu bin, inaczej nie będzie działać):
    * ./virustotal
    * możliwe, że trzeba plikowi virustotal nadać uprawnienia do wykonywania, w takim wypadku
    * chmod +x bin/virustotal
7. domyślnie serwer jest widoczny pod localhost:5005
8. w pliku config.ini możemy zmienić nazwę hosta, port, miejsce przechowywania logów oraz miejsce do którego będą zapisywane pliki html.
9. po zmianie pliku config należy wyłączyć i ponownie włączyć aplikacje -> aplikacja reaguje na SIGINT (ctrl+c) i ładnie robi dump kolejki (można podejrzeć w pliku dump w głównym folderze)

UWAGA;
Jeśli nie chcemy, żeby stare żądania ostały się po ponownym odpaleniu serwera należy usunąć plik dump z głównego katalogu projektu

Prezentacja
-----------
W katalogu presentation są dwa skrypty pythona, w celu wypróbowania ich działania należy najpierw włączyć serwer 
(i ew. zmienić porty w skryptach, jeśli są inne od domyślnych)
1. skrypt make_single_vt_request uderza do metody /api/singleVirusTotal serwera i jako argument podaje sha256 z plików umieszczonych w locky.txt i crypto.txt
    * w celu włączenia skryptu: ./make_single_vt_request_py
2. skrypt make_virus_info_request uderza do metody /api/virus i pyta o takie same sha256 jak wyżej, wyniki zapisuje w results (należy stworzyć ten katalog jeśli wyskoczy błąd)

UWAGA
Należy pamiętać, że w celu uniknięcia uznania nas za bota przez serwis VirusTotal nasz serwer robi 
co najwyżej jednego requesta na [VtDelay] sekund (domyślnie 10), można zmienić w config.ini.
Natomiast pozostałe żądania są kolejkowane do FIFO.


# virustotalparser standalone

1. Należy przeprowadzić instalację jak dla serwera
2. wchodzimy do katalogu bin i wywołujemy komendę
    * ./vtparser html_dir
    
Przykłady użycia vtparser:
--------------------------
./vtparser html_dir json_dir

./vtparser html_dir

gdzie dir to ścieżka bezwzględna lub względna do plików html/json.

np. ./vtparser test/vt.html test/list.json

Więcej informacji o sposobie działania programu otrzymamy wpisując w konsoli

vtparser




    
 
    
    