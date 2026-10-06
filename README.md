# BarberBook
Prototip educațional Python pentru aplicația de programări la frizerie din laboratorul 1, Roșca Sergiu, AAW-231.
Laboratorul 2 demonstrează Git și GitHub. Datele sunt în memorie; autentificarea web, baza de date și interfața sunt etape viitoare.
## Run
Python 3.10+; fără biblioteci externe.
```sh
python3 -m barberbook.demo
python3 -m unittest discover -s tests -v
```
## Rules
O programare include un serviciu; intervalele sunt [start, end). Prețul și durata se păstrează la rezervare.
Clientul poate anula numai rezervarea proprie, înainte de început. Frizerul poate marca propria programare completed/no_show după început.
Serviciile inactive, suprapunerile, indisponibilitățile și depășirea orarului sunt respinse. Rezervările concurente sunt protejate cu RLock.
