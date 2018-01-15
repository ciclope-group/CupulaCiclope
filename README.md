![](http://mercurio.datsi.fi.upm.es/wp-content/uploads/2015/11/logo-grupo-ciclope-e1448887578240.png)
# CupulaCiclope

## Purpose of the project

In this project we wil develop several aplications and utilities to use in a real observatory located in the CEI Montegancedo - Universidad Politécnica de Madrid.
We are developing several controlers for the dome, the telescope and a meteor station.

## Progress

It is done a beta version from the messaging between the linux based controllers using [RabitMQ](https://www.rabbitmq.com/) and [python 2.7](https://www.python.org)

## API REST
- `GET /api/cupula/montegancedo`
- `GET /api/cupula/montegancedo/tasks/<task ID>`
- `POST /api/cupula/montegancedo/task`
- `POST /login`

### `GET /api/cupula/montegancedo`
Get information about the dome status.
Response:
~~~py
{
    'lat'   : "40 24 22 N",
    'long'  : "3 50 19 O",
    'name'  : "Observario Montegancedo",
    'status':{
            'Azimut'   : <azimut in degrees>,
            'Laps'     : <number of laps>,
            'Voltage'  : <dome motor power supply voltage>,
            'Direction': <direction which the dome follows>
        }
}
~~~
### `GET /api/cupula/montegancedo/tasks/<task ID>`
Get information about a specific task status.
Response:
~~~py
{
    'id'     : <task ID>,
    'command': <command the task executes>,
    'time'   : <time the task was received>,
    'status' : <completed | non-completed>
}

~~~ 

### `POST /api/cupula/montegancedo/task`
Create a new task. It's mandatory to be logged in.
Request:
~~~py
{
    'command':<command for the new task>
}
~~~
Response:
~~~py
{
    'id'     : <task ID>,
    'command': <command the task executes>,
    'time'   : <time the task was received>,
    'status' : non-completed
}
~~~
#### Commands
* SZ : TODO
* H  : Go home.
* followOn  : Start following the telescope mount.
* followOff : Stop following the telescope mount.
* Dx : Go to azimut x.
* ON : Enable dome.
* OFF: Disable dome.
### `POST /login`
Fields:
* `'username'`
* `'password'`

