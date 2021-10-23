#All the code (heap and sheduler) based on the one seen (and PCW) on session [5.2]-Heaps and priority queues


#One task at the time sheduler

class Task:
    """
    - id: Task Id   
    - description: Short description of the task   
    - duration: Duration in minutes 
    - dependencies: what other tasks (id) have to be compleated before starting task
    - priority: Priority level of a task (ranging from 1 to 5)   
    - status: Current status of the task:       
   
    """
    #Initializes an instance of Task
    def __init__(self,task_id,description,duration,dependencies,priority,status="N"):
        self.id= task_id
        self.description=description
        self.duration=duration
        self.dependencies=dependencies
        self.priority = priority
        self.status=status
        
    #Transforms the class object as strings
    def __repr__(self):
        return f"{self.description} - id: {self.id}\n \tDuration:{self.duration}\n\tDepends\
        on: {self.dependencies}\n\tPriority: {self.priority}\n\tStatus: {self.status}"
     #The atribute used here will be the one that the priority que uses for the node
    def __lt__(self, other):
        return self.priority < other.priority    
    
class TaskScheduler:
    """
    A Simple Daily Task Scheduler Using Priority Queues
    Uses the objects created in Tasks
    This code uses a Max heap inside the function for the implementation

    """
    #Status of the tasks
    NOT_STARTED ='N'
    IN_PRIORITY_QUEUE = 'I'
    COMPLETED = 'C'
    
    #Initialize objects
    def __init__(self, tasks):
        self.tasks = tasks
        self.priority_queue = [] 
        self.heap_size = 0
        
    #Prints all the tasks that need to be completed
    def print_self(self):
        print('Input List of Tasks')
        for t in self.tasks:
            print(t)    
    #Given that it's a crucial part of the code I integraed the functions to build a heap
    #Max heap given how the priorities (value use for heap) are written
    def left(self, i):
        """
        Takes the index of the parent node
        and returns the index of the left child node

        Parameters
        ----------
        i: int
          Index of parent node

        Returns
        ----------
        int
          Index of the left child node

        """
        return 2 * i + 1

    def right(self, i):
        """
        Takes the index of the parent node
        and returns the index of the right child node
        
        Parameters
        ----------
        i: int
            Index of parent node

        Returns
        ----------
        int
            Index of the right child node

        """

        return 2 * i + 2
		
    def parent(self, i):
        """
        Takes the index of the child node
        and returns the index of the parent node
        
        Parameters
        ----------
        i: int
            Index of child node

        Returns
        ----------
        int
            Index of the parent node

        """

        return (i - 1)//2

        
    def maxk(self):     
        """
        Returns the highest key in the priority queue. 
        
        Parameters
        ----------
        None

        Returns
        ----------
        int
            the highest key in the priority queue

        """
        #equal to A[0]
        return self.priority_queue[0]     
    
  
    def heappush_max(self, key):  
        """
        Insert a key into a priority queue 
        
        Parameters
        ----------
        key: int
            The key value to be inserted

        Returns
        ----------
        None
        """
        #Creation of sentinel value to append to priority Queue
        #Need to call the class task 
        sentinel = Task(-1000, 'sentinel', 5, [],-1000,)
        #Append sentinel to increase the size of the queue
        self.priority_queue.append(sentinel)
        self.increase_key(self.heap_size,key)
        self.heap_size+=1
        
    def increase_key(self, i, key): 
        """
        Modifies the value of a key in a max priority queue
        with a higher value
        
        Parameters
        ----------
        i: int
            The index of the key to be modified
            #(in the code is usually the last one or A[A.lenght)
        key: int
            The new key value

        Returns
        ----------
        None
        """
        if key < self.priority_queue[i]:
            raise ValueError('new key is smaller than the current key')
        self.priority_queue[i] = key
        #parent as a function above  parent(self, i):
        #Takes the index of the child node
        #and returns the index of the parent node
        #parent is samller than current index
        while i > 0 and self.priority_queue[self.parent(i)] < self.priority_queue[i]:
            #creates the parent node (index)
            j = self.parent(i)
            #parent node
            holder = self.priority_queue[j]
            #makes the change the parent ins the child
            self.priority_queue[j] = self.priority_queue[i]
            #the new child was the parent
            self.priority_queue[i] = holder
            #the oriiginal number being eveluated is in the new position so the index news to be updates
            i = j    
            
    
    def heapify_max(self, i):
        """
        Creates a max heap from the index given
        
        Parameters
        ----------
        i: int
            The index of of the root node of the subtree to be heapify

        Returns
        ----------
        None
        """
        #same code as last heap class
        l = self.left(i)
        r = self.right(i)
        priority_queue = self.priority_queue
        if l <= (self.heap_size-1) and priority_queue[l]> priority_queue[i]:
            largest = l
        else:
            largest = i
        if r <= (self.heap_size-1) and priority_queue[r] > priority_queue[largest]:
            largest = r
        if largest != i:
            priority_queue[i], priority_queue[largest] = priority_queue[largest], priority_queue[i]
            self.heapify_max(largest)
            
    def heappop_max(self):
        """
        returns the largest key in the max priority queue
        and remove it from the max priority queue
        
        Parameters
        ----------
        None

        Returns
        ----------
        int
            the max value in the heap that is extracted
        """
        if self.heap_size < 1:
            raise ValueError('Heap underflow: There are no keys in the priority queue ')
        maxk = self.priority_queue[0]
        self.priority_queue[0] = self.priority_queue[-1]
        self.priority_queue.pop()
        #decrese the heap size
        self.heap_size-=1
        self.heapify_max(0)
        return maxk
            
    def remove_dependency(self, task_id):
        """
        Input: list of tasks and task_id of the task just completed
        Output: lists of tasks with t_id removed
        """
        for t in self.tasks:
            if t.id != task_id and task_id in t.dependencies:
                t.dependencies.remove(task_id)           
            
    def get_tasks_ready(self):
        """ 
        Implements step 1 of the scheduler
        Input: list of tasks
        Output: list of tasks that are ready to execute (i.e. tasks with no pendending task 
        dependencies and the highest priority)
        """
        for task in self.tasks:
            # If task has no dependencies and is not yet in queue
            if task.status == self.NOT_STARTED and not task.dependencies: 
                task.status = self.IN_PRIORITY_QUEUE # Change status of the task
                ######## Push task into the priority queue (1line of code required)  
                #calls the push function inside the class
                self.heappush_max(task)
    
    def check_unscheduled_tasks(self):
        """
        Input: list of tasks 
        Output: boolean (checks the status of all tasks and returns 
        True if at least one task has status = 'N'
        """
        for task in self.tasks:
            if task.status == self.NOT_STARTED:
                return True
        return False   
    
    def format_time(self, time):
        return f"{time//60}h {time%60:02d}"
    
    #Starts the time at 8:00 am
    def run_task_scheduler(self, starting_time = 480):
        current_time = starting_time
        while self.check_unscheduled_tasks() or self.priority_queue:
            #STEPs 1 and 2: Extract tasks ready to execute (those without dependencies)
            #and push them into the priority queue
            #Inside the priority que they will the max will be the one with the higgest priority 
            self.get_tasks_ready()
            if len(self.priority_queue) > 0 :  #STEP 3: Check for tasks in the priority queue.      
                # STEP 4: get the tasks on top of the priority queue (1 line of code required)
                current_task = self.heappop_max() #highest priority
                print(f"⏰Simple Scheduler at time {self.format_time(current_time)} started executing task {current_task.description} that takes {current_task.duration} mins")
                current_time += current_task.duration            
                print(f"✅ Completed Task {current_task.id} - '{current_task.description}' at time {self.format_time(current_time)}\n") 
                ####### if the task is completed, it cannot be a 
                #dependency on other tasks, so remove it from the dependency list (1 line of code required)
                self.remove_dependency(current_task.id)
                current_task.status = self.COMPLETED
        total_time = current_time - starting_time             
        print(f"🏁 Completed all planned tasks in {total_time//60}h {total_time%60:02d}min 😊")

