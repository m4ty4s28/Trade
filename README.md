# Solution
 
## Getting Started

### Using Docker 🐳

1. Build the Docker image:
   ```
   docker build -t docker-django .
   ```

2. Run the Docker Container:
   ```
   docker run --name django_trade -p 8000:8000 -d docker-django
   ```
## Once django is started, you can:

Import the [trade.postman_collection.json](https://github.com/m4ty4s28/Trade/blob/main/trade.postman_collection.json) file directly into POSTMAN.

Enter the url [127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) to see all the created models with their data.

### User Administrator:
user: admin

pass: admin123

### User A (payment method A):
user: user_a

pass: trade123

### User B (payment method B):
user: user_b

pass: trade123

The FEES is configured from the "Configuracion" model specially created for the configuration of variables.
