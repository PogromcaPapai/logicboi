# logicboi
Bada tautologiczność zdań; operuje w ramach KRZ

## __Ważne uwagi składniowe__
 1. Zdanie __musi__ być umieszczone w cudzysłowiu, jeśli podawane jako argument w konsolii
 2. System __wymaga__ użycia nawiasów dla każdego funktora
 3. Znaki języka KRZ __muszą__ być oddzielone od siebie spacjami (z wyjątkiem nawiasów)
 4. Dopuszczalne jest używanie dla zmiennych nazw wieloliterowych.
 5. Tak samo dopuszczalne jest używanie nazw spójników zamiast ich znaków

## Lista spójników
 - Negacje - `(not _)` - `(nie _)` - `(~ _)`
 - Koniunkcja - `(_ and _)` - `(_ i _)` - `(_ & _)`
 - Alternatywa - `(_ or _)` - `(_ lub _)` - `(_ + _)`
 - Implikacja - `(_ imp _)` - `(_ > _)`

## Komendy:
 - `logicboi help` - wyświetla pomoc #TODO
 - `logicboi tautotest` - sprawdza tautologiczność zdań
 - `logicboi contrtest` - sprawdza kontrtautologiczność zdań #TODO
 - `logicboi check` - sprawdza prawdziwość zdania dla danych argumentów, wymagane `--with` #TODO

## Opcje uruchamiania:
 - `--with(...)` - pozwala na założenie wartości zmiennej (ex. `--with(p=True)`) #TODO
 - `--printtable` - generuj wyświetla w konsoli tabelę prawdziwościową #TODO
 - `--savetable` - zapisuje tabelę prawdziwościową jako plik #TODO
 - `--debug` - plox nie używać, włącza funkcjonalności do debugowania