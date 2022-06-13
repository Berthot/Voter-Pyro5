#!/usr/bin/env python3

# Matheus Bertho Tavares

from sys import argv
import Pyro5.api
import Pyro5.errors


def configure_client():
    if len(argv) < 2:
        print(f"USO: {argv[0]} <file>")
        print(f"USO: {argv[0]} <server-name>")
        print(f"USO: {argv[0]} <message>")
        print('try: python3 <file>.py <server-name> <message>')
        exit(1)
    nome = argv[1]
    ref = Pyro5.api.Proxy(f"PYRONAME:{nome}")  # get ref to obj
    print("ns ok")
    return ref


def get_message():
    argv.append('')
    mss = argv[2]
    if mss == '':
        return 'default message'
    return argv[2]


if __name__ == "__main__":
    eco = configure_client()
    try:
        print("Call operation...", flush=True)
        message = get_message()
        print("Response :=", eco.send(message))
        print("Counter  :=", eco.counter())
    except Pyro5.errors.CommunicationError as e:
        print("crash failure detected")
        print(e)
    except Pyro5.errors.NamingError as ne:
        print("name not found on server-names")
        print(ne)
