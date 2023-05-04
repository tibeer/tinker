// fn main() {
//     println!("Hello, world!");
// }
use axum::{
    routing::get,
    Router,
};

#[tokio::main]
async fn main() {
    // build our application with a single route
    let app = Router::new()
        .route("/", get(home))
        .route("/foo", get(foo));

    // run it with hyper on localhost:3000
    axum::Server::bind(&"0.0.0.0:3000".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}

async fn home() -> &'static str {
    let result = "Hello, World!";
    return result;
}
async fn foo() -> &'static str {
    let result = "Hello, bar!";
    return result;
}
