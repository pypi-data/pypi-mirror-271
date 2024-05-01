// SPDX-License-Identifier: (Apache-2.0 OR MIT)

use std::env;

fn main() {
    println!("cargo:rerun-if-changed=build.rs");
    println!("cargo:rerun-if-changed=include/yyjson/*");
    println!("cargo:rerun-if-env-changed=CC");
    println!("cargo:rerun-if-env-changed=CFLAGS");
    println!("cargo:rerun-if-env-changed=LDFLAGS");
    println!("cargo:rerun-if-env-changed=RUSTFLAGS");
    println!("cargo:rerun-if-env-changed=ORJSON_DISABLE_SIMD");
    println!("cargo:rerun-if-env-changed=ORJSON_DISABLE_YYJSON");

    for cfg in pyo3_build_config::get().build_script_outputs() {
        println!("{cfg}");
    }

    if let Some(true) = version_check::supports_feature("core_intrinsics") {
        println!("cargo:rustc-cfg=feature=\"intrinsics\"");
    }

    if let Some(true) = version_check::supports_feature("optimize_attribute") {
        println!("cargo:rustc-cfg=feature=\"optimize\"");
    }

    if let Some(true) = version_check::supports_feature("strict_provenance") {
        println!("cargo:rustc-cfg=feature=\"strict_provenance\"");
    }

    #[cfg(any(target_arch = "x86_64", target_arch = "aarch64"))]
    if env::var("ORJSON_DISABLE_SIMD").is_err() {
        if let Some(true) = version_check::supports_feature("portable_simd") {
            println!("cargo:rustc-cfg=feature=\"unstable-simd\"");
        }
    }

    if env::var("ORJSON_DISABLE_YYJSON").is_ok() {
        if env::var("CARGO_FEATURE_YYJSON").is_ok() {
            panic!("ORJSON_DISABLE_YYJSON and --features=yyjson both enabled.")
        }
    } else {
        match cc::Build::new()
            .file("include/yyjson/yyjson.c")
            .include("include/yyjson")
            .define("YYJSON_DISABLE_NON_STANDARD", "1")
            .define("YYJSON_DISABLE_UTF8_VALIDATION", "1")
            .define("YYJSON_DISABLE_UTILS", "1")
            .define("YYJSON_DISABLE_WRITER", "1")
            .try_compile("yyjson")
        {
            Ok(_) => {
                println!("cargo:rustc-cfg=feature=\"yyjson\"");
            }
            Err(_) => {
                if env::var("CARGO_FEATURE_YYJSON").is_ok() {
                    panic!("yyjson was enabled but the build failed. To build with a different backend do not specify the feature.")
                }
            }
        }
    }
}
