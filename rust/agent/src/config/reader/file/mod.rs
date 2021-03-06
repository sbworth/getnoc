// ---------------------------------------------------------------------
// FileReader module
// ---------------------------------------------------------------------
// Copyright (C) 2007-2021 The NOC Project
// See LICENSE for details
// ---------------------------------------------------------------------

cfg_if::cfg_if! {
    if #[cfg(feature = "config-file")] {
        mod base;
        pub use base::FileReader;
    } else {
        use super::base::StubReader;
        pub type FileReader = StubReader;
    }
}
