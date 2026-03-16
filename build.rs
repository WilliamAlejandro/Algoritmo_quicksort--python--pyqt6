fn main() {
    // No resource compilation to avoid icon issues on Windows
    println!("cargo:rerun-if-changed=build.rs ");
}