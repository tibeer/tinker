use std::io;
use std::cmp::Ordering;
use rand::Rng;

fn main() {
    /*
    println!("Size your VM");
    println!("");

    println!("Number of CPUs:");
    let mut cpu_amount = String::new();
    io::stdin()
        .read_line(&mut cpu_amount)
        .expect("Failed to read cpu_amount");
    let cpu_amount = cpu_amount.trim();

    println!("Amount of RAM in GB:");
    let mut ram_amount_gb = String::new();
    io::stdin()
        .read_line(&mut ram_amount_gb)
        .expect("Failed to read ram_amount_gb");
    let ram_amount_gb = ram_amount_gb.trim();

    println!("Storage in GB:");
    let mut storage_amount_gb = String::new();
    io::stdin()
        .read_line(&mut storage_amount_gb)
        .expect("Failed to read storage_amount_gb");
    let storage_amount_gb = storage_amount_gb.trim();

    println!("");
    println!("Your VM has the following specifications:");
    println!("CPUs: {cpu_amount}");
    println!("RAM in GB: {ram_amount_gb}");
    println!("Storage in GB: {storage_amount_gb}");
    */

    let random_number = rand::thread_rng().gen_range(1..=16);

    loop {
        println!("You guess:");
        let mut guess = String::new();
        io::stdin()
            .read_line(&mut guess)
            .expect("Failed to read guess");
        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => continue
        };
        
        println!("You guessed: {guess}");

        match guess.cmp(&random_number) {
            Ordering::Equal => {
                println!("You win!");
                break;
            },
            Ordering::Greater => println!("Too big!"),
            Ordering::Less => println!("Too small!")
        }
    }
}