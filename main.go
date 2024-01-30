package main

import (
	"github.com/emersion/go-imap"
	"github.com/emersion/go-imap/client"
	"github.com/emersion/go-message/mail"
	"github.com/joho/godotenv"
	"log"
	"os"
	"regexp"
	"strings"
)

func extractCompanyName(subject string) (string, bool) {
	pattern := `Robert, your application was sent to (.+)`
	re := regexp.MustCompile(pattern)
	matches := re.FindStringSubmatch(subject)

	if len(matches) > 1 {
		return matches[1], true
	}
	return "", false
}

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
	if err := c.Login(email, password); err != nil {
		log.Fatal(err)
	}
	log.Println("Logged in")

	// Select INBOX
	_, err = c.Select("INBOX", false)
	if err != nil {
		log.Fatal(err)
	}

	// Fetch all emails
	criteria := imap.NewSearchCriteria()
	uids, err := c.UidSearch(criteria)
	if err != nil {
		log.Fatal(err)
	}

	// Print the uids of the retrieved emails
	log.Println("Email UIDs found:", uids)

	// There are potentially a lot of emails, and multiple requests will need to be made to get them all
	// So we use the c.UidSearch method to get the UIDs of the emails
	// Then we can use the c.Fetch method to get the email headers and body
	// And we want to store them somewhere temporarily, while we process them
	// We can use a map to store the UIDs as keys, and the email headers and body as values
	// Then we can use the UIDs to get the email headers and body from the map

	// Fetch emails in chunks
	const chunkSize = 10
	emailMap := make(map[uint32]*imap.Message)
	for i := 0; i < len(uids); i += chunkSize {
		end := i + chunkSize
		if end > len(uids) {
			end = len(uids)
		}
		seqset := new(imap.SeqSet)
		seqset.AddNum(uids[i:end]...)

		// Get the whole message body
		section := &imap.BodySectionName{}
		items := []imap.FetchItem{section.FetchItem()}

		messages := make(chan *imap.Message)
		go func() {
			if err := c.UidFetch(seqset, items, messages); err != nil {
				log.Fatal(err)
			}
		}()

		// Process each message
		for msg := range messages {
			if msg == nil {
				log.Fatal("Server didn't return message")
			}

			r := msg.GetBody(section)
			if r == nil {
				log.Fatal("Server didn't return message body")
				continue
			}

			// Create a new mail reader
			mr, err := mail.CreateReader(r)
			if err != nil {
				log.Fatal(err)
			}

			// Check if the subject matches the pattern
			header := mr.Header
			if subject, err := header.Subject(); err == nil {
				if strings.HasPrefix(subject, "Robert, your application was sent to ") {
					// Convert mail.Reader to imap.Message
					msg := &imap.Message{Body: msg.Body, SeqNum: msg.SeqNum, Uid: msg.Uid}

					emailMap[msg.Uid] = msg
				}
			}
		}
	}

	log.Println("Seen email UIDs found:", uids)
}
