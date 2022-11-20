# Sea Battle

This is a console sea battle game.

The main idea of the implementation: to build a game based on sockets.

## Start Server Application

```bash
python3 main.py --host 127.0.0.1 --port 11000 --server
``` 

## Start Client Application

```bash
python3 main.py --host 127.0.0.1 --port 11000 --client
``` 

## Ideas and bugs

### Bugs
- In rare cases opponent_addr = user_addr
- I think application have problem with sync threads in server mode

### Feature
- Add UI for game
- It is necessary to optimize data transfer between peers
