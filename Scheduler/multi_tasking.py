#Multitasker (Final)
class MultiTask:
    """
    - id: Task Id   
    - description: Short description of the task   
    - duration: Duration in minutes   
    - priority: Priority level of a task (ranging from 0 to 100)  
    - multi: Boolan if multistasking the task is possible or not
    - status: Current status of the task:       
   
    """
    #Initializes an instance of Task
    def __init__(self,task_id,description,duration,dependencies,priority,multi,status="N"):
        self.id= task_id
        self.description=description
        self.duration=duration
        self.dependencies=dependencies
        self.priority = priority
        self.multi = multi
        self.status=status
        
    def __repr__(self):
        return f"{self.description} - id: {self.id}\n \tDuration:{self.duration}\n\tDepends on: {self.dependencies}\n\tStatus: {self.status}"

    def __lt__(self, other):
        return self.priority < other.priority    
    
class MultiTaskScheduler:
    """
    A Simple Daily Task Scheduler that allows Multitasking Using Priority Queues 
    
    This code uses a Max heap inside the function for the implementation
    """
    NOT_STARTED ='N'
    IN_PRIORITY_QUEUE = 'I'
    COMPLETED = 'C'
    
    def __init__(self, tasks):
        self.tasks = tasks
        self.priority_queue = [] 
        self.heap_size = 0
        
    def print_self(self):
        print('Input List of Tasks')
        for t in self.tasks:
            print(t)    

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
        sentinel = MultiTask(-1000, 'sentinel', 5, [],-1000,False)
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
        Output: list of tasks that are ready to execute (i.e. tasks with no pendending task dependencies)
        """
        for task in self.tasks:
            if task.status == self.NOT_STARTED and not task.dependencies: # If task has no dependencies and is not yet in queue
                task.status = self.IN_PRIORITY_QUEUE # Change status of the task
                ######## Push task into the priority queue (1line of code required)
                ####### your code here   
                self.heappush_max(task)
                #print(self.tasks)
                #print("push", self.priority_queue)
    
    def check_unscheduled_tasks(self):
        """
        Input: list of tasks 
        Output: boolean (checks the status of all tasks and returns True if at least one task has status = 'N'
        """
        for task in self.tasks:
            if task.status == self.NOT_STARTED:
                return True
        return False   
    
    def format_time(self, time):
        return f"{time//60}h {time%60:02d}"
    
    #Possible use of functions to shorten the code
    
    #def single_task(self, task):
     #   current_task = task
      #  current_time = starting_time
       # print(f"⏰Simple Scheduler at time {self.format_time(current_time)} started executing task {current_task.description} that takes {current_task.duration} mins")
       # current_time += current_task.duration            
        #print(f"✅ Completed Task {current_task.id} - '{current_task.description}' at time {self.format_time(current_time)}\n") 
        ####### if the task is completed, it cannot be a 
        #dependency on other tasks, so remove it from the dependency list (1 line of code required)
        #self.remove_dependency(current_task.id)
        #current_task.status = self.COMPLETED 
        #remove the task from the priority que
        #self.priority_queue.remove(i)
        #decrease the size of the arrey
        #self.heap_size-=1
        
    
    #def multi_task2(self, task, time):
        

    
    def run_task_scheduler(self, starting_time = 480):
        current_time = starting_time
        #Condition for multitasking
        while self.check_unscheduled_tasks() or self.priority_queue:
            #STEPs 1 and 2: Extract tasks ready to execute (those without dependencies) and push them into the priority queue
            self.get_tasks_ready()
            multi_round = []
            if len(self.priority_queue) > 0 :  #STEP 3: Check for tasks in the priority queue.      
                #store all the values of the priority que
                new_queue = []
                for i in self.priority_queue:
                    new_queue.append(i)
                for i in new_queue:
                    #Check the multitasking condition
                    #prioritize the first in the queu if it can be multitasked
                    #Satisfy condition if no multitasked and in queue must be perfrmed
                    if i.multi == False:
                        current_task = i
                        print(f"⏰Simple Scheduler at time {self.format_time(current_time)} started executing task {current_task.description} that takes {current_task.duration} mins")
                        current_time += current_task.duration            
                        print(f"✅ Completed Task {current_task.id} - '{current_task.description}' at time {self.format_time(current_time)}\n") 
                        ####### if the task is completed, it cannot be a 
                        self.remove_dependency(current_task.id)
                        current_task.status = self.COMPLETED
                    #I=Check if the activity can be multitasked
                    elif i.multi == True:
                        #If they can be multitasked and are in the priority que they will have priority
                        current_task = i
                        multi_round.append(current_task)
                        #remove the task from the priority que
                        self.remove_dependency(current_task.id)
                        current_task.status = self.COMPLETED
                #remove from que will mantaining the queue conditions
                    self.heappop_max()
                #reset the array for next round
                new_queue = []
                #Assumes people can only realistically multitask 2 tasks 
                #print("multi",multi_round)
                if len(multi_round) == 2:
                #Changes the order to have the one with the samllest duration first (finish first)
                    for i in range(len(multi_round)-1):
                        if multi_round[i].duration > multi_round[i+1].duration:
                            multi_round[i], multi_round[i+1] = multi_round[i+1],multi_round[i]
                    times_holder = []
                    #Necesary to call first that take less time and then the lonegre ones 
                    for i in range(len(multi_round)):
                    #prints that every task is being completed
                        print(f"⏰Simple Scheduler at time {self.format_time(current_time)} started executing task {multi_round[i].description} that takes {multi_round[i].duration} mins")
                        if len(times_holder) >= 1:
                        #appends the duration of the new task (longer) minus the duration of the privious one
                        #(shorter)
                            times_holder.append(multi_round[i].duration-multi_round[i-1].duration)
                        else:
                        #appends normal time (first round)
                            times_holder.append(multi_round[i].duration)
                #calculates the time for each one
                    for i in range(len(multi_round)):
                        current_time += times_holder[i]  
                        print(f"✅ Completed Task {multi_round[i].id} - '{multi_round[i].description}' at time {self.format_time(current_time)}")
                    multi_round = []
                    print("")
                #Only one value in the priority que means that it had to be performe alone (but also has priority over task that can not be multitasked)
                elif len(multi_round) == 1:
                    for i in range(len(multi_round)):
                        #prints that every task is being completed
                        print(f"⏰Simple Scheduler at time {self.format_time(current_time)} started executing task {multi_round[i].description} that takes {multi_round[i].duration} mins")
                        current_time += multi_round[i].duration
                        print(f"✅ Completed Task {multi_round[i].id} - '{multi_round[i].description}' at time {self.format_time(current_time)}\n")
                    multi_round = []
                #More than 2 tasks enters a while loop to repete the same until the list (multi_round) only has 2
                elif len(multi_round) > 2:
                    for i in range(len(multi_round)-1):
                        if multi_round[i].duration > multi_round[i+1].duration:
                            multi_round[i], multi_round[i+1] = multi_round[i+1],multi_round[i]
                    #stores the values to manipulate muliple_round
                    possible = []
                    #loop to perform only 2 values at the same time
                    while len(multi_round) > 2:
                        if len(possible) < 2: 
                            for i in multi_round:
                                possible.append(i)
                                multi_round.remove(i)
                        #print(possible)
                        times_holder = []
                        for i in range(len(possible)):
                            #prints that every task is being completed
                            print(f"⏰Simple Scheduler at time {self.format_time(current_time)} started executing task {possible[i].description} that takes {possible[i].duration} mins")
                            if len(times_holder) >= 1:
                                #appends the duration of the new task (longer) minus the duration of the privious one
                                #(shorter)
                                times_holder.append(possible[i].duration-possible[i-1].duration)
                            else:
                                #appends normal time (first round)
                                times_holder.append(possible[i].duration)
                        #calculates the time for each one
                        for i in range(len(possible)):
                            current_time += times_holder[i]  
                            print(f"✅ Completed Task {possible[i].id} - '{possible[i].description}' at time {self.format_time(current_time)}")
                    print(" ")
                    times_holder = []
                    for i in range(len(multi_round)):
                    #prints that every task is being completed
                        print(f"⏰Simple Scheduler at time {self.format_time(current_time)} started executing task {multi_round[i].description} that takes {multi_round[i].duration} mins")
                        if len(times_holder) >= 1:
                            #appends the duration of the new task (longer) minus the duration of the privious one
                            #(shorter)
                            times_holder.append(multi_round[i].duration-multi_round[i-1].duration)
                        else:
                            #appends normal time (first round)
                            times_holder.append(multi_round[i].duration)
                    for i in range(len(multi_round)):
                        current_time += times_holder[i]  
                        print(f"✅ Completed Task {multi_round[i].id} - '{multi_round[i].description}' at time {self.format_time(current_time)}")
                    print(" ")
                    multi_round = []
               
        
        #Prints total time to do tasks
        total_time = current_time - starting_time             
        print(f"🏁 Completed all planned tasks in {total_time//60}h {total_time%60:02d}min 😊")
