from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import os
from rich.console import Console

console = Console()

# Create the engine and session
engine = create_engine("sqlite:///book.db")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Association table for the many-to-many relationship between books and customers
class BookCustomerAssociation(Base):
    __tablename__ = 'book_customer_association'
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), primary_key=True)

# Book model
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    genre = Column(String)
    publication_date = Column(Date)
    price = Column(Integer)
    quantity = Column(Integer)
    customers = relationship("Customer", secondary='book_customer_association', back_populates="books")

# Customer model
class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact = Column(String)
    books = relationship("Book", secondary='book_customer_association', back_populates="customers")

# Sale model
class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    quantity = Column(Integer)
    sale_date = Column(Date, nullable=False)
    book = relationship("Book", backref="sales")
    customer = relationship("Customer", backref="sales")

# Create the tables in the database
Base.metadata.create_all(engine)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    clear_screen()
    console.print("Welcome To The Bookish BrewBook Store Management", style="bold green")
    console.print("1. Add Book", style="bold blue")
    console.print("2. Update Book Quantity", style="bold blue")
    console.print("3. List Books", style="bold blue")
    console.print("4. Delete Book", style="bold blue")
    console.print("5. Search Books", style="bold blue")
    console.print("6. Process Sale", style="bold blue")
    console.print("7. Add Customer", style="bold blue")
    console.print("8. List Customers", style="bold blue")
    console.print("9. Delete Customer", style="bold blue")
    console.print("10. Generate Report", style="bold blue")
    console.print("11. Quit", style="bold blue")

def get_valid_choice(prompt, choices):
    while True:
        choice = input(prompt)
        if choice in choices:
            return choice
        else:
            console.print("Invalid choice. Please try again.", style="bold white on red")

def add_book():
    clear_screen()
    console.print("Add Book", style="bold green")
    print("-------------------")
    title = input("Title: ")
    author = input("Author: ")
    genre = input("Genre: ")
    publication_date = input("Publication Date (YYYY-MM-DD): ")

    try:
        # Convert the publication date string into a Python date object
        publication_date = datetime.strptime(publication_date, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please enter the date in the format YYYY-MM-DD.")
        return  # Return early if the date format is invalid

    while True:
        try:
            price = int(input("Price: "))  # Convert input to integer
            break
        except ValueError:
            print("Invalid input. Please enter a valid price.")

    while True:
        try:
            quantity = int(input("Quantity: "))  # Convert input to integer
            break
        except ValueError:
            print("Invalid input. Please enter a valid quantity.")

    book = Book(
        title=title,
        author=author,
        genre=genre,
        publication_date=publication_date,
        price=price,
        quantity=quantity
    )
    session.add(book)
    session.commit()
    print("Book added successfully!")

def update_book_quantity():
    clear_screen()
    console.print("Update Book Quantity", style="bold green")
    print("-------------------")
    book_id = input("Enter the ID of the book to update (or 'q' to go back): ")

    if book_id.lower() == 'q' or book_id.lower() == 'cancel':
        return  # Go back to the main menu

    try:
        book_id = int(book_id)  # Convert input to integer
    except ValueError:
        print("Invalid input. Please enter a valid book ID.")
        input("\nPress Enter to continue.")
        return

    book = session.query(Book).get(book_id)

    if book is None:
        print("Book not found. Please enter a valid book ID.")
        input("\nPress Enter to continue.")
        return

    new_quantity = input("Enter the new quantity: ")

    try:
        new_quantity = int(new_quantity)  # Convert input to integer
    except ValueError:
        print("Invalid input. Please enter a valid quantity.")
        input("\nPress Enter to continue.")
        return

    book.quantity = new_quantity
    session.commit()

    print("Book quantity updated successfully!")
    input("\nPress Enter to return to the main menu.")

def list_books():
    clear_screen()
    console.print("List Books", style="bold green")
    print("-------------------")
    books = session.query(Book).all()
    for book in books:
        console.print(
            f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Genre: {book.genre}, Price: {book.price}, Quantity: {book.quantity}", style="blue")
    input("\nPress Enter to return to the main menu.")

def search_books():
    clear_screen()
    console.print("Search Books", style="bold green")
    print("-------------------")
    keyword = input("Enter a keyword to search: ")
    keyword = f"%{keyword}%"  # Add wildcard characters for partial matching
    books = session.query(Book).filter(
        (Book.title.like(keyword)) | (Book.author.like(keyword)) | (Book.genre.like(keyword))
    ).all()
    if books:
        for book in books:
            console.print(
                f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Genre: {book.genre}, Price: {book.price}, Quantity: {book.quantity}", style="blue")
    else:
        console.print("No books found matching the keyword.", style="bold red")
    input("\nPress Enter to return to the main menu.")

def delete_book():
    clear_screen()
    console.print("Delete Book", style="bold green")
    print("-------------------")
    while True:
        book_id = input(
            "Enter the ID of the book to delete (or 'q' to exit): ")
        if book_id.lower() == 'q':
            return  # Cancel the deletion process if 'q' is entered
        try:
            book_id = int(book_id)  # Convert input to integer
            break  # Break out of the loop if input is valid
        except ValueError:
            print("Invalid input. Please enter a valid book ID.")

    book = session.query(Book).get(book_id)
    if book:
        session.delete(book)
        session.commit()
        print("Book deleted successfully!")
    else:
        print("Book not found.")

    input("\nPress Enter to return to the main menu.")

def process_sale():
    clear_screen()
    console.print("Process Sale", style="bold green")
    print("-------------------")

    while True:
        book_id = input("Enter the ID of the book (or 'q' to go back): ")

        if book_id.lower() == "q":
            print("Sale process cancelled.")
            input("\nPress Enter to return to the main menu.")
            return

        if book_id.isdigit():  # Validate input as a digit
            break
        else:
            print("Invalid input. Please enter a valid book ID or 'q' to go back.")

    book_id = int(book_id)  # Convert input to integer
    customer_id = int(input("Enter the ID of the customer: "))  # Convert input to integer
    quantity = int(input("Enter the quantity sold: "))  # Convert input to integer

    book = session.query(Book).get(book_id)
    customer = session.query(Customer).get(customer_id)

    if book and customer:
        if book.quantity >= quantity:
            # Get the current date
            sale_date = datetime.now().date()

            sale = Sale(
                book=book,
                customer=customer,
                quantity=quantity,
                sale_date=sale_date  # Set the sale_date
            )
            session.add(sale)
            book.quantity -= quantity
            session.commit()
            print("Sale processed successfully!")
        else:
            print("Insufficient quantity in stock.")
    else:
        print("Invalid book or customer ID.")
    input("\nPress Enter to return to the main menu.")


def add_customer():
    clear_screen()
    console.print("Add Customer", style="bold green")
    print("-------------------")

    while True:
        name = input("Name (or 'q' to cancel): ")

        if name.strip().lower() == "q":
            print("Add customer canceled.")
            input("\nPress Enter to return to the main menu.")
            return

        contact = input("Contact: ")

        if name.strip() != "" and contact.strip() != "":
            break
        else:
            print("Invalid input. Please enter non-empty values for name and contact.")

    customer = Customer(
        name=name,
        contact=contact
    )
    session.add(customer)
    session.commit()

    print("Customer added successfully!")
    input("\nPress Enter to return to the main menu.")

def list_customers():
    clear_screen()
    console.print("List Customers", style="bold green")
    print("-------------------")

    customers = session.query(Customer).filter(
        Customer.name != "", Customer.contact != "").all()

    if not customers:
        print("No customers found.")
    else:
        for customer in customers:
            console.print(
                f"ID: {customer.id}, Name: {customer.name}, Contact: {customer.contact}", style="blue")

    input("\nPress Enter to return to the main menu.")

def delete_customer():
    clear_screen()
    console.print("Delete Customer", style="bold green")
    print("-------------------")
    while True:
        customer_id = input(
            "Enter the ID of the customer to delete (or 'q' to exit): ")
        if customer_id.lower() == 'q':
            return  # Cancel the deletion process if 'q' is entered
        try:
            customer_id = int(customer_id)  # Convert input to integer
            break  # Break out of the loop if input is valid
        except ValueError:
            print("Invalid input. Please enter a valid customer ID.")

    customer = session.query(Customer).get(customer_id)
    if customer:
        session.delete(customer)
        session.commit()
        print("Customer deleted successfully!")
    else:
        print("Customer not found.")

    input("\nPress Enter to return to the main menu.")

def generate_report():
    clear_screen()
    console.print("Generate Report", style="bold green")
    print("-------------------")
    sales = session.query(Sale).join(Sale.book).all()
    total_sales = len(sales)
    total_revenue = sum(
        sale.book.price * sale.quantity for sale in sales if sale.book)
    console.print(f"Total Sales: {total_sales}", style="bold yellow")
    console.print(f"Total Revenue: {total_revenue}", style="bold yellow")
    input("\nPress Enter to return to the main menu.")

def main():
    while True:
        show_menu()
        choice = get_valid_choice("Enter your choice: ", [
                                  "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"])
        if choice == "1":
            add_book()
        elif choice == "2":
            update_book_quantity()
        elif choice == "3":
            list_books()
        elif choice == "4":
            delete_book()
        elif choice == "5":
            search_books()
        elif choice == "6":
            process_sale()
        elif choice == "7":
            add_customer()
        elif choice == "8":
            list_customers()
        elif choice == "9":
            delete_customer()
        elif choice == "10":
            generate_report()
        elif choice == "11":
            break

    print("Thank you for using the Book Store Management system!")

if __name__ == "__main__":
    main()
