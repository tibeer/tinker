package main

import (
	"fmt"
	"encoding/json"
	"log"
	"net/http"
	"strings"

	"github.com/gorilla/mux"
)

// Book Struct (Model)
type BookStrcut struct {
	ID     string  `json:"id"`
	Isbn   string  `json:"isbn"`
	Title  string  `json:"title"`
	Author *Author `json:"author"`
}

// Author Struct
type Author struct {
	Firstname	string	`json:"firstname"`
	Lastname	string	`json:"lastname"`
}

// Init books var as a slive Book struct
var books []BookStrcut

func getBooks(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(books)
}
func getBook(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r) // get params
	// Loop trough books and find the id
	for _, item := range books {
		if item.ID == params["id"] {
			json.NewEncoder(w).Encode(item)
			return
		}
	}
	json.NewEncoder(w).Encode(&BookStrcut{})
}
func createBook(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	var book BookStrcut
	_ = json.NewDecoder(r.Body).Decode(&book)
	book.ID = "2"
	books = append(books, book)
	json.NewEncoder(w).Encode(book)
}
func updateBook(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r) // get params
	for index, item := range books {
		if item.ID == params["id"] {
			books = append(books[:index], books[index+1:]...)
			var book BookStrcut
			_ = json.NewDecoder(r.Body).Decode(&book)
			book.ID = "2"
			books = append(books, book)
			return
		}
	}
	json.NewEncoder(w).Encode(books)
}
func deleteBook(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r) // get params
	for index, item := range books {
		if item.ID == params["id"] {
			books = append(books[:index], books[index+1:]...)
			break
		}
	}
	json.NewEncoder(w).Encode(books)
}

func logger(mode string, message string) {
	//INFO
	//DEBUG
	//ERROR
	//WARNING
	log.Print("[" + strings.ToUpper(mode) + "] " + message)
}

func home(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html")
	fmt.Fprintf(w, "Hello world!")
}

func main() {
	logger("info", "Server startup")
	r := mux.NewRouter()

	// TODO implement databse
	books = append(books, BookStrcut{ID: "1", Isbn: "test", Title: "Book One", Author: &Author{Firstname: "John", Lastname: "Cena"}})

	r.HandleFunc("/", home).Methods("GET")
	r.HandleFunc("/api/books", getBooks).Methods("GET")
	r.HandleFunc("/api/books/{id}", getBook).Methods("GET")
	r.HandleFunc("/api/books", createBook).Methods("POST")
	r.HandleFunc("/api/books/{id}", updateBook).Methods("PUT")
	r.HandleFunc("/api/books/{id}", home).Methods("DELETE")

	log.Fatal(http.ListenAndServe(":8000", r))
}
