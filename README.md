# Filed JSON

JSON distributed by file system

JSON распределенный по файлам.
Вы можете представить свои данные ни в одном, а в нескольких json файлах, в рамках одной директории с любым уровнем вложенности директорий. 
Класс FiledJson объединит все файлы из директории в одну единую структуру, с сохранением файловой структуры. 

Пример:

### Countries

директория examples/countries включает 4 файла:

- afghanistan.json
```json
{
	"name": "Afghanistan",
    "city": "Kabul",
	"continent": "Asia"
}
```
- albania.json
```json
{
	"title": "Albania",
	"city": "Tirana",
	"continent": "Europe"
}
```
- algeria.json
```json
{
	"title": "Algeria",
	"city": "Alger",
	"continent": "Africa"	
}
```
- andorra.json
```json
{
	"country": "Andorra",
	"city": "Andorra la Vella",
	"continent": "Europe"	
}
```

Python

``` phyton
from filedjson import FiledJson

fj = FiledJson("examples/countries")
print(fj)
print(fj.structure)
```

Вывод:

```
. afghanistan:
. . city: Kabul
. . continent: Asia
. albania:
. . title: Albania
. . city: Tirana
. . continent: Europe
. algeria:
. . title: Algeria
. . city: Alger
. . continent: Africa
. andorra:
. . country: Andorra
. . city: Andorra la Vella
. . continent: Europe

{'': {'_type': 'directory', '_fn': '', 'name': '', 'afghanistan': {'name': 'afghanistan', 'city': 'Kabul', 'continent': 'Asia', '_type': 'file', '_ext': 'json', '_fn': 'afghanistan.json'}, 'albania': {'title': 'Albania', 'city': 'Tirana', 'continent': 'Europe', '_type': 'file', '_ext': 'json', '_fn': 'albania.json', 'name': 'albania'}, 'algeria': {'title': 'Algeria', 'city': 'Alger', 'continent': 'Africa', '_type': 'file', '_ext': 'json', '_fn': 'algeria.json', 'name': 'algeria'}, 'andorra': {'country': 'Andorra', 'city': 'Andorra la Vella', 'continent': 'Europe', '_type': 'file', '_ext': 'json', '_fn': 'andorra.json', 'name': 'andorra'}}}
```

Все файлы были объединены в одну структуру

Свойство structure предоставляет доступ к сформированной структуре

Если ключу сформирован на основе файла или директории, то к соответствующему узлу добавляются дополнительные свойства:

- _type: - ['file' , 'directory']
- _ext: - расширение файла
- _fn - имя файла