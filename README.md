**Activate the virtual enviroment**

```
source Curso_udemy-env/bin/activate
```

**Install all packages**

```
pip3 install -r requirements.txt
```

**Run the tests** 

Make sure to activate the virtual enviroment.

It's necessary the test.py name begin with "test_".
```
python3 -m pytest Backend/Tests
```

It will run all the tests inside the Tests package (Blockchain and Util)

**Run the application and API** 

Make sure to activate the virtual enviroment. 

```
python3 -m Backend.App
```# blockchain-python
