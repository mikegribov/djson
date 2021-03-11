# Distributed JSON

JSON distributed by file system

**[Documentation](https://mikegribov.github.io/djson/)**

JSON распределенный по файловой структуре.
Этот модуль позволяет одну и ту же структуру, которая представима в формате JSON представить как в одном json файле, 
так и в нескольких, распределив части структуры по нескольким файлам и директориям.

### Пример:

Countries

``` single_file.json```

### JSON-файл со структурой географических объектов

```json
{	
		"afghanistan": {
			"title": "Afghanistan",
			"city": "Kabul",
			"continent": "Asia"
		},
		"albania": {
			"title": "Albania",
			"city": "Tirana",
			"continent": "Europe"
		},
		"algeria": {
			"title": "Algeria",
			"city": "Alger",
			"continent": "Africa"
		},
		"andorra": {
			"title": "Andorra",
			"city": "Andorra la Vella",
			"continent": "Europe"
		},
		"belarus": {
			"title": "Belarus",
			"city": "Minsk",
			"continent": "Europe",
			"regions":{
				"minsk": {
					"title": "Minskiy region",
					"city": "Minsk",
					"cities": {
						"minsk": {
							"title": "Minsk"
						},
						"shack": {
							"title": "Shack"
						},
						"uzda": {
							"title": "Uzda"
						}
					}
				}
			}
		},
		"russia": {
			"title": "Russia",
			"city": "Moscow",
			"continent": "Europe",
			"regions": {
				"moscow": {
					"title": "Moscow region",
					"city": "Moscow",
					"cities": {
						"moscow": {
							"title": "Moscow"
						},
						"abramcevo": {
							"title": "Abramcevo"
						},
						"alabino": {
							"title": "Alabino"
						}
					}
				}
			}
		}
}
```

### Этот файл можно разбить на несколько файлов, размещенные в отдельной директории:

- ``` index.json``` - корневой файл директории
- ``` belarus.json``` - файл, описывающий стуктуру ключа __belarus__
- ``` russia.json``` - файл, описывающий стуктуру ключа __russia__


Содержимое файлов:

#### index.json
```json
{	
	"afghanistan": {
		"title": "Afghanistan",
		"city": "Kabul",
		"continent": "Asia"
	},
	"albania": {
		"title": "Albania",
		"city": "Tirana",
		"continent": "Europe"
	},
	"algeria": {
		"title": "Algeria",
		"city": "Alger",
		"continent": "Africa"
	},
	"andorra": {
		"title": "Andorra",
		"city": "Andorra la Vella",
		"continent": "Europe"
	},
	"belarus": {
		"title": "Belarus",
		"city": "Minsk",
		"continent": "Europe"
	}
}
```

#### belarus.json
```json
{
	"title": "Belarus",
	"city": "Minsk",
	"continent": "Europe",
	"regions":{
		"minsk": {
			"title": "Minskiy region",
			"city": "Minsk",
			"cities": {
				"minsk": {
					"title": "Minsk"
				},
				"shack": {
					"title": "Shack"
				},
				"uzda": {
					"title": "Uzda"
				}
			}
		}
	}
}

```
#### russia.json
```json
{
	"title": "Russia",
	"city": "Moscow",
	"continent": "Europe",
	"regions": {
		"moscow": {
			"title": "Moscow region",
			"city": "Moscow",
			"cities": {
				"moscow": {
					"title": "Moscow"
				},
				"abramcevo": {
					"title": "Abramcevo"
				},
				"alabino": {
					"title": "Alabino"
				}
			}
		}
	}
}
```
Если при создании объекта класса Djson указать директорию, в которой собраны эти файлы, то будет сформирована та же структуру, 
что была описана в исходном файле ```single_file.json```

### Ничто не мещает сделать еще более глубокое разбиение, в котором содержимое ключа описывается ни одним файлом, а директорией:


```index.json``` с содержимым:
```json
{	
		"afghanistan": {
			"title": "Afghanistan",
			"city": "Kabul",
			"continent": "Asia"
		},
		"albania": {
			"title": "Albania",
			"city": "Tirana",
			"continent": "Europe"
		},
		"algeria": {
			"title": "Algeria",
			"city": "Alger",
			"continent": "Africa"
		},
		"andorra": {
			"title": "Andorra",
			"city": "Andorra la Vella",
			"continent": "Europe"
		},
		"belarus": {
			"title": "Belarus",
			"city": "Minsk",
			"continent": "Europe"
		}
}
```
в нем частично описана Беларусь, структура этого ключа будем составлена из содержимого в этом файле и из содержимого в директории ```belarus``` с приоритетом.

Ключ __russia__ представим директорией ```russia```, в которой лежит файл ```index.json``` содержащий:

```json
{
	"title": "Russia",
	"city": "Moscow",
	"continent": "Europe",
	"regions": {
		"moscow": {
			"title": "Moscow region",
			"city": "Moscow",
			"cities": {
				"moscow": {
					"title": "Moscow"
				},
				"abramcevo": {
					"title": "Abramcevo"
				},
				"alabino": {
					"title": "Alabino"
				}
			}
		}
	}
}
```


## Использование
```python
from djson import DJson

dj = DJson(os.path.join("countries", "dir_several_level")) # Загружаем данные из директории

print(dj.dump()) 		# Визуализация структуры
print(dj.structure) 		# отображение структуры

```

Вывод:

```
afghanistan:
. title: Afghanistan
. city: Kabul
. continent: Asia
albania:
. title: Albania
. city: Tirana
. continent: Europe
algeria:
. title: Algeria
. city: Alger
. continent: Africa
. _info:
. . c_time: 1615286632.520336
. . fn: examples\countries\dir_several_level\algeria.json
. . size: 69
. . type: file
. . ext: json
andorra:
. title: Andorra
. city: Andorra la Vella
. continent: Europe
. _info:
. . c_time: 1615286585.7477758
. . fn: examples\countries\dir_several_level\andorra.json
. . size: 80
. . type: file
. . ext: json
belarus:
. title: Belarus
. city: Minsk
. continent: Europe
. regions:
. . minsk:
. . . title: Minskiy region
. . . city: Minsk
. . . cities:
. . . . minsk:
. . . . . title: Minsk
. . . . shack:
. . . . . title: Shack
. . . . uzda:
. . . . . title: Uzda
. . . _info:
. . . . c_time: 1615286846.780374
. . . . fn: examples\countries\dir_several_level\belarus\regions\minsk.json
. . . . size: 190
. . . . type: file
. . . . ext: json
. . _info:
. . . c_time: 1615286837.3603652
. . . fn: examples\countries\dir_several_level\belarus\regions
. . . type: directory
. _info:
. . c_time: 1615286556.0513194
. . fn: examples\countries\dir_several_level\belarus
. . type: directory
russia:
. title: Russia
. city: Moscow
. continent: Europe
. regions:
. . moscow:
. . . title: Moscow region
. . . city: Moscow
. . . cities:
. . . . moscow:
. . . . . title: Moscow
. . . . abramcevo:
. . . . . title: Abramcevo
. . . . alabino:
. . . . . title: Alabino
. _info:
. . c_time: 1615286564.1888194
. . fn: examples\countries\dir_several_level\russia
. . type: directory
_info:
. c_time: 1615272379.9731324
. fn: examples\countries\dir_several_level
. type: directory

{'afghanistan': {'title': 'Afghanistan', 'city': 'Kabul', 'continent': 'Asia'}, 'albania': {'title': 'Albania', 'city': 'Tirana', 'continent': 'Europe'}, 'algeria': {'title': 'Algeria', 'city': 'Alger', 'continent': 'Africa', '_info': {'c_time': 1615286632.520336, 'fn': 'tests\\examples\\countries\\dir_several_level\\algeria.json', 'size': 69, 'type': 'file', 'name': 'algeria', 'ext': 'json'}}, 'andorra': {'title': 'Andorra', 'city': 'Andorra la Vella', 'continent': 'Europe', '_info': {'c_time': 1615286585.7477758, 'fn': 'tests\\examples\\countries\\dir_several_level\\andorra.json', 'size': 80, 'type': 'file', 'name': 'andorra', 'ext': 'json'}}, 'belarus': {'title': 'Belarus', 'city': 'Minsk', 'continent': 'Europe', 'regions': {'minsk': {'title': 'Minskiy region', 'city': 'Minsk', 'cities': {'minsk': {'title': 'Minsk'}, 'shack': {'title': 'Shack'}, 'uzda': {'title': 'Uzda'}}, '_info': {'c_time': 1615286846.780374, 'fn': 'tests\\examples\\countries\\dir_several_level\\belarus\\regions\\minsk.json', 'size': 190, 'type': 'file', 'name': 'minsk', 'ext': 'json'}}, '_info': {'c_time': 1615286837.3603652, 'fn': 'tests\\examples\\countries\\dir_several_level\\belarus\\regions', 'type': 'directory', 'name': 'regions'}}, '_info': {'c_time': 1615286556.0513194, 'fn': 'tests\\examples\\countries\\dir_several_level\\belarus', 'type': 'directory', 'name': 'belarus'}}, 'russia': {'title': 'Russia', 'city': 'Moscow', 'continent': 'Europe', 'regions': {'moscow': {'title': 'Moscow region', 'city': 'Moscow', 'cities': {'moscow': {'title': 'Moscow'}, 'abramcevo': {'title': 'Abramcevo'}, 'alabino': {'title': 'Alabino'}}}}, '_info': {'c_time': 1615286564.1888194, 'fn': 'tests\\examples\\countries\\dir_several_level\\russia', 'type': 'directory', 'name': 'russia'}}, '_info': {'c_time': 1615272379.9731324, 'fn': 'tests\\examples\\countries\\dir_several_level', 'type': 'directory', 'name': 'dir_several_level'}}

```

### ключ _info
к значению каждого ключа, который был получен из файла или директориюю добавляется дополнительная структура с ключом ___info__, которая содержит информацию о своем источнике - файле или директории, пример:
```json
{
	'c_time': 1615286846.780374, 
	'fn': 'tests\\examples\\countries\\dir_several_level\\belarus\\regions\\minsk.json', 
	'size': 190, 
	'type': 'file', # или directory
	'name': 'minsk', 
	'ext': 'json'
}
```