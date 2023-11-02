# Left to do (in no particular order):

- Add password hashing and salting
- Server/Client Communication encryption
- Encourage users to use strong passwords - password minimum length, maybe also password complexity, etc.
- Add a way to change password? (maybe) - if we do, we will need to add a way to verify the user's identity? - e.g.: send an email to the user's email address
- Add a way to change email? (maybe) - if we do, we will need to add a way to verify the user's identity? - e.g.: send an email to the user's email address
- Ticket Dashboard - all tickets for sale (implement pagination?)
- Ticket Dashboard - user's current tickets (implement pagination?)
  - ~~Allow users to view their tickets~~
  - ~~Allow user to buy and sell tickets~~
- Admin functionality
  - Allow admins to create new tickets
  - Allow admins to update existing tickets
  - Allow admins to delete existing tickets
  - more?
- Error handling
- Add tests
- Add vulnerabilities
  - currently have plaintext password
  - we already have SQL Injection patched currently, so maybe add the vulnerability only for the users table?

- Update frame after every ticket purchase (to show the updated ticket count)
- Add user's current currency to buy ticket frame
- Add user's current currency to sell ticket frame
- When selling a ticket, fix the price not being updated correctly