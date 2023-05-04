fn main() {
    let x = 5;

    let x = x + 1;

    {
        let x = x * 2;
        println!("Der Wert von x im inneren Gültigkeitsbereich ist: {x}");
    }

    println!("Der Wert von x ist: {x}");
}
