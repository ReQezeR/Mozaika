# Mozaika

Usługa generująca mozaikę dla danej kolekcji obrazków pobieranych z określonych adresów URL.

## Opis:

* Usługa dysponuje endpointem:
**[GET]** 
```
http://adres-uslugi/mozaika?losowo=Z&rozdzielczosc=XxY&zdjecia=URL1,URL2,URL3...
```
gdzie:
* **losowo** - parametr opcjonalny, jeśli wartość parametru Z ustawiona na 1 to kolejność zdjęć w mozaice
jest losowa, w każdym innym przypadku zachowuje kolejność podaną w parametrze "zdjecia";
* **rozdzielczosc** - definiuje oczekiwany rozmiar wyjściowy mozaiki w rozdzielczości **X** (szerokość) na **Y**(wysokość),
parametr opcjonalny, jeśli nie zdefiniowany przyjmuje 2048x2048;
* **URL1,URL2,URL3...** - URLe kolejnych zdjęć, które powinny znaleźć się w mozaice, oddzielone przecinkami,
minimum 1, maksymalnie 8 adresów.
* Wyjściowy format obrazu - **JPEG**.

## Język implementacji: 

Python

## Wykorzystano biblioteki:

* bottle
* openCV
* urllib

## License

This project is licensed under the **MIT License** - see the [LICENSE.md](LICENSE.md) file for details
