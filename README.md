What are query parameters?
Query parameter is the key value pair added at the end of the URL After a ?
It is used for filtering ,searchong and sorting 

Difference between query parameters and path parameters?

The primary difference between the two is that path parameters are used to identify a 
specific, unique resource, while query parameters are used to filter, sort, or modify a collection of resources


How do you make a query parameter optional?
in FastAPI, you simply need to assign it a default value in your function definition.
If you want it to be completely empty by default, assign it None


How do you set a default value?

 assign the value using the = operator directly inside the path operation function's arguments

How do you handle multiple query parameters?


Real-world use cases — search, filters, and pagination (e.g. price/category filters on e-commerce sites).



