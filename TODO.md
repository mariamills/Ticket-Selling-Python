# Left to do (in no particular order):

- Add password hashing and salting
- Server/Client Communication encryption
- ~~Encourage users to use strong passwords - password minimum length, maybe also password complexity, etc.~~ - added min & max len, may add complexity later, such as number of special characters, etc.


- Add a way to change password? (maybe) - if we do, we will need to add a way to verify the user's identity? - e.g.: send an email to the user's email address - probably not going to do this due to time constraints
- Add a way to change email? (maybe) - if we do, we will need to add a way to verify the user's identity? - e.g.: send an email to the user's email address - probably not going to do this due to time constraints
- ~~Ticket Dashboard - all tickets for sale~~ (implement pagination?) - decided not to add pagination, instead LIMIT of 15.
- ~~Ticket Dashboard - user's current tickets (implement pagination?)~~ - decided not to add pagination for now
  - ~~Allow users to view their tickets~~
  - ~~Allow user to buy and sell tickets~~


- Admin functionality
  - ~~Allow admins to create new tickets~~ - Maybe limit the number of tickets an admin can create? or change display limit to 10?
  - Allow admins to update existing tickets
  - Allow admins to delete existing tickets


- Error handling - For the most part, I think errors are handled well, need to go over code and test to be sure. __Needs double-checking__.
- Add tests - May not have time to do this before due date, but that is ok, this is not a requirement for the project.
- ~~Update frame after every ticket purchase (to show the updated ticket count)~~
- ~~Add user's current currency to buy ticket frame~~
- ~~Add user's current currency to sell ticket frame~~
- ~~When selling a ticket, fix the price not being updated correctly~~

### Bugs
- Logout was changed to Exit because it was causing a 'bug' where when you logout, 
it closes the client socket connection (which is wanted) BUT,
the server will not expect/accept anymore client socket connections from the same client  (which is NOT wanted).
  - So, as a temporary fix, I changed logout to exit, which will close the client socket connection, 
  - but will also close the client program. This is not ideal, but it works for now. 

We will need to eventually come up with a better solution.

### Vulnerabilities
- plaintext password (not hashed or salted)
- unsecure TCP connection (no encryption)
- SQL injection (not using prepared statements) ? Currently using prepared statements so we'd need to remove this
