// ---------------------------------------------------------------------
// twamp_reflector collector configuration
// ---------------------------------------------------------------------
// Copyright (C) 2007-2021 The NOC Project
// See LICENSE for details
// ---------------------------------------------------------------------

use serde::Deserialize;
use std::hash::Hash;

#[derive(Deserialize, Debug, Clone, Hash)]
pub struct TwampReflectorConfig {
    pub listen: String,
    #[serde(default = "default_862")]
    pub port: u16,
}

fn default_862() -> u16 {
    862
}
