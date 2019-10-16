# logicboi
Bada tautologiczność zdań; operuje w ramach KRZ

## __Ważne uwagi składniowe__
 1. System __wymaga__ użycia nawiasów dla każdego funktora
 2. Znaki języka KRZ __muszą__ być oddzielone od siebie spacjami (z wyjątkiem nawiasów)
 3. Dopuszczalne jest używanie dla zmiennych nazw wieloliterowych.
 4. Tak samo dopuszczalne jest używanie nazw spójników zamiast ich znaków

## Lista spójników
 - Negacje - `(not _)` - `(nie _)` - `(~ _)`
 - Koniunkcja - `(_ and _)` - `(_ i _)` - `(_ & _)`
 - Alternatywa - `(_ or _)` - `(_ lub _)` - `(_ + _)`
 - Implikacja - `(_ imp _)` - `(_ > _)`

## Komendy:
 - `logicboi help` - wyświetla pomoc #TODO
 - `logicboi tautotest` - sprawdza tautologiczność zdań #TODO
 - `logicboi contrtest` - sprawdza kontrtautologiczność zdań #TODO
 - `logicboi check` - sprawdza prawdziwość zdania dla danych argumentów, wymagane `--with` #TODO

## Opcje uruchamiania:
 - `--with(...)` - pozwala na założenie wartości zmiennej (ex. `--with(p=True)`) #TODO
 - `--printtable` - generuj wyświetla w konsoli tabelę prawdziwościową #TODO
 - `--savetable` - zapisuje tabelę prawdziwościową jako plik #TODO