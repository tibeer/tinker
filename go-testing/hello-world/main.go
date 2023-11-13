package main

import "sync"
import "fmt"
import "os/exec"
import "os"

func some(url string, wg *sync.WaitGroup) {
	defer wg.Done()

	cmd := exec.Command("ping", url)

	// pipe the commands output to the applications
	// standard output
	cmd.Stdout = os.Stdout

	// Run still runs the command and waits for completion
	// but the output is instantly piped to Stdout
	if err := cmd.Run(); err != nil {
		fmt.Println("could not run command: ", err)
	}
}

func main() {
	fmt.Println("hello world")

	var wg sync.WaitGroup

	wg.Add(2)
	go some("google.com", &wg)
	go some("cloudflare.com", &wg)
	wg.Wait()
}
