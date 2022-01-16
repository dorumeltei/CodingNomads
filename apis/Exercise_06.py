import requests
from pprint import pprint

menu = '''
Please select from the following options (enter the number of the action you'd like to take):
1) Create a new account (POST)
2) View all your tasks (GET)
3) View your completed tasks (GET)
4) View only your incomplete tasks (GET)
5) Create a new task (POST)
6) Update an existing task (PATCH/PUT)
7) Delete a task (DELETE)
8) Exit
'''

base_url = "http://demo.codingnomads.co:8080/tasks_api/"

new_account = {
    "first_name": "doru",
    "last_name": "me",
    "email": "dome@gmail.com"
}

id = 591

def get_tasks(base_url, page):
    global id
    url = base_url + page
    response = requests.get(url)
    response = response.json()['data']  
    return [x for x in response if x['userId'] == id]

while True:
    ask_input = input(menu)
    if ask_input == '1':
        url = base_url + 'users'
        response = requests.post(url, new_account)
    elif ask_input == '2':
        response = get_tasks(base_url, 'tasks')     
    elif ask_input == '3':
        response = get_tasks(base_url, 'tasks')
        response = [task for task in response if task['completed'] == True]
    elif ask_input == '4':
        response = get_tasks(base_url, 'tasks')
        incomplete = [task for task in response if task['completed'] == False]
    elif ask_input == '5':
        url = base_url + 'tasks'
        name = input("Your name: ")
        task_description = input("Task description: ")
        task_completion = input("Is taks completed? Answer Yes or No: ")
        if task_completion.lower() == 'yes':
            task_completion = True
        elif task_completion.lower() == 'no':
            task_completion = False
        new_task = {'userId': id,
                    'name': name,
                    'description': task_description,    
                    'completed': task_completion}
        response = requests.post(url, json=new_task)
    elif ask_input == '6':
        response = get_tasks(base_url, 'tasks') 
        url = base_url + 'tasks'
        task_id = input('What task to modify?. Add task ID:\n')
        task_to_modify = [task for task in response if task['id'] == int(task_id)]
        task_to_modify = task_to_modify[0]
        print(f'You selected task {task_id}')
        task_description = input('New task description (hit Enter to keep current value):\n')
        task_completed = input('Is task completed? Yes or No?\n')
        bool_check = {'yes': True, 'no': False}
        if task_description:
            task_to_modify['description'] = task_description
        task_to_modify['completed'] = bool_check[task_completed.lower()]
        response = requests.put(url, json=task_to_modify)

    elif ask_input == '7':
        response = get_tasks(base_url, 'tasks') 
        task_id = input('What task to delete?. Add task ID:\n')
        url = base_url + 'tasks/'
        response = requests.delete(url + task_id)

    elif ask_input == '8':
        response = ''
        break
    pprint(response)
    ask_continue = input('Continue? Yes -> back to menu or No -> exit.\n')
    if ask_continue.lower() == 'yes':
        continue
    elif ask_continue.lower() == 'no':
        break