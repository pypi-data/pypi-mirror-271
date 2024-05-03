# Epate
## Install
Install by pip(Recommend)

`pip install epaste`

## Guide
### 1.Login Function
Epate.login()
#### Parameters
| Parameters Name             | Type  |
|-----------------|------|
| username    | str  |
| password    | str  |
| print       | str  |
#### Example
```python
import Epate
a = Epate.login('yourusername','yourpassword','no')
print(a)
```
If it's successful,it will print'200'.

If it's failed,it will print error code.

### 2.Logout Function
Epate.logout()
#### Parameters
| Parameters Name             | Type  |
|-----------------|------|
| print       | str  |
#### Example
```python
import Epate
a = Epate.login('no')
print(a)
```
If it's successful,it will print'204'.

If it's failed,it will print error code.

### 3.UserInfo Change Function
Epate.usrinfo()
#### Parameters
| Parameters Name             | Type  |
|-----------------|------|
| kind    | str  |
| inputstr    | str  |
| inpuint    | int  |
| print       | str  |
##### Kind
| Kinds Name             | Type  |
|-----------------|------|
| nick    | str  |
| full    | str  |
| desc    | int  |
| sex       | str  |
| birth       | str  |
| avat       | str  |

#### Example
```python
import Epate
a = Epate.usrinfo('nick','Xiaoxiao','no')
print(a)
```
If it's successful,it will print'204'.

If it's failed,it will print error code.

### 4.Password Change Function
Epate.psc()
#### Parameters
| Parameters Name             | Type  |
|-----------------|------|
| old_password    | str  |
| new_password    | str  |
| print       | str  |

#### Example
```python
import Epate
a = Epate.psc('aa123456','bb234567','no')
print(a)
```
If it's successful,it will print'204'.

If it's failed,it will print error code.

### 5.Work Function
Epate.like()
Epate.coll()
Epate.fork()
#### Parameters
| Parameters Name             | Type  |
|-----------------|------|
| workid    | str  |
| print       | str  |

#### Example
```python
import Epate
a = Epate.like('1234567','no')
print(a)
```
If it's successful,it will print'201'.

If it's failed,it will print error code.
### If you want more, please wait for update or join us and commit your code!
