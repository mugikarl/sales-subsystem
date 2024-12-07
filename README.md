# Order and Menu Management System

## Group 2
- Alcaide, Hannah Bea
- Arapoc Beatrice Jan
- Espera, Mae Angela
- Lim, Joash Miguel
- Natividad, Karl Justin Angelo

## Libraries included:
- ReportLab (pip install reportlab)
  - for PDF 
## Subsystems Overview
### 1. Order Subsystem
This subsystem facilitates the process of managing customer orders from creation to completion.
#### Functionalities/Use Cases:
1. Create New Order:
- The cashier creates a new order by inputting customer-provided details into the system (e.g., menu items, quantity).
2. Modify Order Details:
- If there are errors or changes requested by the customer, the cashier can:
    - Add new items to the order.
    - Delete specific items from the order.
3. Finalize Order:
- Once all details are accurate and confirmed by the customer, the cashier finalizes the order.
4. Process Payment:
- The system calculates the total amount and processes the payment.
- Any change due is calculated and displayed to complete the order.


### 2. Menu Management Subsystem
This subsystem is designed to allow staff to manage the menu effectively.
#### Functionalities/Use Cases:
1. Add New Menu Items:
- Staff can create and add a new menu item to the system, including details such as name, price, and category.
2. Modify Existing Menu Items:
- Updates can be made to existing menu items, such as price adjustments or name changes.
3. Delete Menu Items:
- Staff can remove a menu item from the system if it is no longer available.

## Overall System Functionality
The system supports full CRUD (Create, Read, Update, Delete) operations for both the Order Subsystem and Menu Management Subsystem, ensuring flexibility and efficient management of operations.
