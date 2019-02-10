# carrental
An exercise in building REST API with Django

Basic functionality of the system:
- add and remove cars
- make reservations of a car for a given period of time
- cancel reservation before it starts
- keep history of reservations
- while a reservation is valid another reservation of the same car is not allowed
- query for a car answers if the car is available;
  if not, gives information on the existing reservation
- maximum time of a reservation is 72h
- paging of results 
- add pictures of cars
- generate PDF for each reservation: 
   (Lorem ipsum + registration number + reservation period + space for signature)
- user with flag is\_staff has access to all endpoints, others only to reservations
- project should contain basic tests

To simplify the task:
- no user registration needed
- car management reduced to add/remove/list, car attributes: make, model, registration number
