# **Scorpii**

## How To Use

1: Install Scorpii by running `pip install Scorpii`

2: Use `import Scorpii` in your code

3: Your all set and ready to use **Scorpii**


## Functions

### `Scorpii.file2`


`file2.read(name)`

Returns the contents of the file with directory 'name'(string)


`file2.write(name,text)`

Writes 'text'(string,int,float) to the file with directory 'name'(string)


`file2.append(name,text)`

Appends 'text'(string,int,float) to the file with directory 'name'(string)


`file2.table_read(name)`

Returns the contents of the file with directory 'name'(string) as a list

**IMPORTANT** Data must have been saved with `table_write()`


`file2.table_write(name,list)`

Writes 'list'(list) to the file with directory 'name'(string) using specific list file formatting


`file2.table_append(name,list)`

Appends 'list'(list) to the file with directory 'name'(string) using specific list file formatting


`file2.remove(file)`

Removes the file with directory 'file'(string)


### `Scorpii.number`


`number.root(num,root)`

Returns the 'root'(int, float) root of 'num'(int,float)

E.g: 

>print(root(8,3)):

> 2


`number.prime(num)`

Returns 'True' if 'num'(int) is a prime number and 'False' if it is not


`number.prime_list(start_num,end_num)`

Returns a list of prime numbers between 'start_num'(int) and 'end_num'(int) inclusive


`number.factorial(num)`

Returns the factorial of 'num'(int)


### `Scorpii.time2`


`time2.wait(num)`

Pauses the program for 'num'(int,float) amount of seconds


`time2.stopwatch_start(id)`

Starts a stopwatch with id = 'id'(int) -- If is unique to each running stopwatch


`time2.stopwatch_stop(id)`

Returns the time on the stopwatch with id = 'id'(int) -- Can be used multiple times


`time2.timer(time,func)`

Asynchronously waits for `time`(int,float) seconds before calling the 'func'(funciton) function

