# Welcome to the Pan-Am airlines flight-booking application
I created this web application, along with its Pan-Am API, as my full-stack capstone project to complete my certification in the Nashville Software School full-stack web development bootcamp. Note that this project is actively being updated with new feature additions.

## About Pan-Am app
Pan-Am airlines unfortunately ceased service in the early 90's, yet it will always be iconic. This project serves as a mock flight-booking application for the airline had it continued to exist into the age of the World Wide Web. 

## Features
* User account data/authentication
* Search for and "purchase" nonstop and 1 stop flights
* One way and roundtrip booking
* Manage bookings (change/cancel)
* Store and add new payment types to user account
* Manage user account

### Useage Notes: 
To simulate the logic that a server might use to create routing for real airline bookings, this application pulls available flights from a finite list stored in its own Pan-Am database, which has been populated with flights through **July 2024**. If you attempt to search for flights beyond then, there will be none available.

!!! FAN-AM 
 When you run/navigate to this application, it will appear as "FAN-AM" rather than "PAN-AM" to avoid any potential issues with trademark/copyright

## Built With
![Next.js](https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![MUI](https://img.shields.io/badge/Material--UI-0081CB?style=for-the-badge&logo=material-ui&logoColor=white)
![NODE.js](	https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node.js&logoColor=white)
![CSS](	https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white)
![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![DJANGO](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![PYTHON](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLITE](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

## Installations
#### API
First, you will need to clone the Pan-Am API to your local machine. This Django application uses Poetry to manage dependencies/virtual environment

In your terminal:
1. Follow installation guide for installing [pipx](https://pipx.pypa.io/stable/installation/).
2. Run `pipx install poetry`.
3. Now clone the following SSH and cd into the root directory:
```bash
git@github.com:ericsteedly/pan-am-api.git
```
4. run `poetry install` to install dependencies
5. run `poetry shell` to activate the virtual environment
6. Now use the `./seed_data.sh` script to run migrations and seed the database
7. Open the project in your code editor, and ensure the correct Python interpreter is selected
8. Start the debugger to run the server

#### Client
Now you can clone the client application:

9. Node.js is required, install first if necessary
10. Clone the following SSH and cd into the root directory:
```bash
git@github.com:ericsteedly/pan-am.git
```
11. Run `npm install' to install dependencies
12. Now run the development server with `npm run dev`
13. Open [http://localhost:3000](http://localhost:3000)

Now that the app is running, you can click the link to register a new account on th login page. From there you will be logged in and free to search and book fake flights with Pan Am!

## Future Features
* Seat count will be dynamically updated with flight purchases
* Users will be able to track and pay with rewards points
* Flight filtering capabilities when changing a booking
* Flight dollar/point cost differnce noted when changing a booking
* Google calendar integration

## Author
[@ericsteedly](https://github.com/ericsteedly)

#### Disclaimer: Use of Likeness or Trademark

This project/repository may utilize the likeness or trademark of **Pan Am** for educational and demonstrative purposes only. The inclusion of **Pan Am's** likeness or trademark is not intended to imply any affiliation with or endorsement by **Pan Am**.

All trademarks and logos referenced within this project/repository are the property of their respective owners. Their inclusion here is solely for the purpose of illustrating concepts and techniques and does not indicate any official partnership or endorsement.

If you represent **Pan Am** and have concerns about the use of your likeness or trademark within this project/repository, please contact us immediately, and we will address your concerns promptly.
