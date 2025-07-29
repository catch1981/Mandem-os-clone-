import argparse
import os
import requests

SERVER_URL = os.getenv('CLONE_SERVER_URL', 'http://localhost:5000')
CLONE_ID = os.getenv('CLONE_ID', os.uname().nodename)


def send_message(message: str):
    resp = requests.post(f"{SERVER_URL}/send", json={'id': CLONE_ID, 'message': message})
    if resp.ok:
        print('message sent')
    else:
        print('error:', resp.text)


def read_messages():
    resp = requests.get(f"{SERVER_URL}/read")
    if resp.ok:
        print(resp.text)
    else:
        print('error:', resp.text)


def remember_fact(fact: str):
    resp = requests.post(f"{SERVER_URL}/remember", json={'id': CLONE_ID, 'fact': fact})
    if resp.ok:
        print('fact stored')
    else:
        print('error:', resp.text)


def get_memories():
    resp = requests.get(f"{SERVER_URL}/memories")
    if resp.ok:
        print(resp.text)
    else:
        print('error:', resp.text)


def fetch_task():
    resp = requests.get(f"{SERVER_URL}/task/assign", params={'id': CLONE_ID})
    if resp.ok:
        data = resp.json()
        task = data.get('task')
        print(task if task else '(no task)')
    else:
        print('error:', resp.text)


def submit_result(result: str):
    resp = requests.post(f"{SERVER_URL}/task/result", json={'id': CLONE_ID, 'result': result})
    if resp.ok:
        print('result stored')
    else:
        print('error:', resp.text)


def get_results():
    resp = requests.get(f"{SERVER_URL}/results")
    if resp.ok:
        print(resp.text)
    else:
        print('error:', resp.text)


def list_tasks():
    resp = requests.get(f"{SERVER_URL}/tasks")
    if resp.ok:
        data = resp.json()
        for t in data.get('tasks', []):
            print(t)
    else:
        print('error:', resp.text)


def main():
    parser = argparse.ArgumentParser(description='Interact with a clone server')
    sub = parser.add_subparsers(dest='cmd')

    send_p = sub.add_parser('send', help='broadcast a message')
    send_p.add_argument('message')

    sub.add_parser('read', help='read all messages')

    remember_p = sub.add_parser('remember', help='store a shared fact')
    remember_p.add_argument('fact')

    sub.add_parser('memories', help='read shared facts')

    sub.add_parser('fetch-task', help='request a queued task')
    sub.add_parser('list-tasks', help='list queued tasks without consuming them')

    result_p = sub.add_parser('submit-result', help='report task result')
    result_p.add_argument('result')

    sub.add_parser('results', help='retrieve stored task results')

    args = parser.parse_args()

    if args.cmd == 'send':
        send_message(args.message)
    elif args.cmd == 'read':
        read_messages()
    elif args.cmd == 'remember':
        remember_fact(args.fact)
    elif args.cmd == 'memories':
        get_memories()
    elif args.cmd == 'fetch-task':
        fetch_task()
    elif args.cmd == 'list-tasks':
        list_tasks()
    elif args.cmd == 'submit-result':
        submit_result(args.result)
    elif args.cmd == 'results':
        get_results()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
