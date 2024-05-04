# Fancy Translator
![Downloads](https://pepy.tech/badge/pyfancytranslator)
![Downloads](https://pepy.tech/badge/pyfancytranslator/week)
![Downloads](https://pepy.tech/badge/pyfancytranslator/month)  
This library allow you to run setup a translator with ease. Just provide it the translations files and access them when ever you need them

### Having an issue?
You can always find someone on our discord server here:
> https://discord.gg/m8ajAQUput

### Wiki
The official wiki of this library will be available at GitHub
> https://github.com/AGM-Studio/FancyTranslator/wiki

## How to install
To install just use following command
```shell
pip install PyFancyTranslator
```
This library will have dev/beta builds on the GitHub, to install them you can use

```shell
pip install --upgrade git+https://github.com/AGM-Studio/FancyTranslator.git
```
# Example

```python
from FancyTranslator import Translator

# All language files must be in .ini format and be placed in a folder to be accessed
translator = Translator("./translations/")

# To access a language with name "en.ini" just call the method below
language = translator.get('en')

# To get a translation for "MyKey" in section "MySection"
translation = language.translate("MySection", "MyKey")

# To use placeholder:
class MyClass:
    def __init__(self, obj):
        self.obj = obj

my_class = MyClass({"name": "Nested"})

# In file: "This is an example with a normal placeholder: %%value%%"
trans1 = translator.get('en').translate("Target", "trans1", value="My Value")
# returns "This is an example with a normal placeholder: My Value"

# In file: "This is an example with a nested placeholder: %%nested.obj.name%%"
trans2 = translator.get('en').translate("Target", "trans2", nested=my_class)
# returns "This is an example with a nested placeholder: Nested"
```

[![Mine Crypto for FREE](https://static.rollercoin.com/static/img/ref/gen2/w970h90.gif)](https://rollercoin.com/?r=jo4ens5n)