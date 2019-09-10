def func(): # define a function
   func.y = 4 # here y is a local variable, which I want to access; func.y defines 
              # a method for my example function which will allow me to access 
              # function's local variable y
   x = func.y + 8 # this is the main task for the function: what it should do
   return x

func() # now I'm calling the function
a = func.y # I put it's local variable into my new variable
print(a) # and print my new variable