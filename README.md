# InvoiceGenerator
Product Invoice generator and Inventory check

### Database design
![alt text](https://github.com/Vashuev/InvoiceGenerator/blob/main/assests/dbdiagram.jpg?raw=true)

**Table product** : Information about various products, like price, quantity in stock, description etc\
**Table invoice** : Invoice with it's customer information\
**Table invoiceProduct** : Invoice with various products and it's quantity  

### API endpoints
| METHOD  | WORKING | API ENDPOINT | 
| ------------- | ------------- | ------------- |
| GET  | List of products  | https://invoicegene.herokuapp.com/api/product/ |
| POST  | Adding new product  | https://invoicegene.herokuapp.com/api/product/ | 
| PUT | Updating a product |  https://invoicegene.herokuapp.com/api/product/slug/ | 
| GET  | List of Invoice | https://invoicegene.herokuapp.com/api/invoice/  |
| POST  | Adding new invoice  | https://invoicegene.herokuapp.com/api/invoice/ | 
| PUT | Updating a invoice | https://invoicegene.herokuapp.com/api/invoice/slug/ |  
| GET  | Downloading a invoice pdf | https://invoicegene.herokuapp.com/api/render_pdf_view/slug/ |

### Invoice Example

![alt text](https://github.com/Vashuev/InvoiceGenerator/blob/main/assests/page1.jpg?raw=true)
![alt text](https://github.com/Vashuev/InvoiceGenerator/blob/main/assests/page2.jpg?raw=true)
