extern crate autocfg;

use std::env;

/// Tests that we can control the use of `#![no_std]`.
#[test]
fn no_std() {
    // Clear the CI `TARGET`, if any, so we're just dealing with the
    // host target which always has `std` available.
    env::remove_var("TARGET");

    // Use the same path as this test binary.
    let dir = env::current_exe().unwrap().parent().unwrap().to_path_buf();
    env::set_var("OUT_DIR", &format!("{}", dir.display()));

    let mut ac = autocfg::AutoCfg::new().unwrap();
    assert!(!ac.no_std());
    assert!(ac.probe_path("std::mem"));

    // `#![no_std]` was stabilized in Rust 1.6
    if ac.probe_rustc_version(1, 6) {
        ac.set_no_std(true);
        assert!(ac.no_std());
        assert!(!ac.probe_path("std::mem"));
        assert!(ac.probe_path("core::mem"));
    }
}
