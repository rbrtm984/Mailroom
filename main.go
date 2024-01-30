package main

import (
	"log"
	"os"
	"github.com/emersion/go-imap/client"
	"github.com/emersion/go-imap"
	"github.com/joho/godotenv"
)

func main() {
	// Get email and pass from .env
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	// Get email and pass from .env
	email := os.Getenv("GMAIL_USER")
	password := os.Getenv("GMAIL_PASS")

	// Connect to server
	log.Println("Connecting to server...")
	c, err := client.DialTLS("imap.gmail.com:993", nil)
	if err != nil {
		log.Fatal(err)
	}
	log.Println("Connected")
	defer c.Logout()

	// Login
	log.Println("Logging in...")
	if err:= c.Login(email, password); err != nil {
		log.Fatal(err)
	}
	log.Println("Logged in")

	// Select INBOX
	_, err = c.Select("INBOX", false)
	if err != nil {
		log.Fatal(err)
	}

	// Search for unread emails with specific subject

	// ... process email
}