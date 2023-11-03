# Left to do (in no particular order):

- Add password hashing and salting
- Server/Client Communication encryption
- ~~Encourage users to use strong passwords - password minimum length, maybe also password complexity, etc.~~ - added min & max len, may add complexity later, such as number of special characters, etc.


- Add a way to change password? (maybe) - if we do, we will need to add a way to verify the user's identity? - e.g.: send an email to the user's email address
- Add a way to change email? (maybe) - if we do, we will need to add a way to verify the user's identity? - e.g.: send an email to the user's email address
- ~~Ticket Dashboard - all tickets for sale~~ (implement pagination?) - decided not to add pagination, instead LIMIT of 15.
- ~~Ticket Dashboard - user's current tickets (implement pagination?)~~ - decided not to add pagination for now
  - ~~Allow users to view their tickets~~
  - ~~Allow user to buy and sell tickets~~


- Admin functionality
  - Allow admins to create new tickets
  - Allow admins to update existing tickets
  - Allow admins to delete existing tickets


- Error handling
- Add tests
- ~~Update frame after every ticket purchase (to show the updated ticket count)~~
- ~~Add user's current currency to buy ticket frame~~
- ~~Add user's current currency to sell ticket frame~~
- ~~When selling a ticket, fix the price not being updated correctly~~

### Vulnerabilities
- plaintext password (not hashed or salted)
- unsecure TCP connection (no encryption)
- SQL injection (not using prepared statements) ? Currently using prepared statements so we'd need to remove this
