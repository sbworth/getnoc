// ---------------------------------------------------------------------
// Collectors registry
// ---------------------------------------------------------------------
// Copyright (C) 2007-2021 The NOC Project
// See LICENSE for details
// ---------------------------------------------------------------------
use super::block_io::{BlockIoCollector, BlockIoConfig};
use super::cpu::{CpuCollector, CpuConfig};
use super::dns::{DnsCollector, DnsConfig};
use super::fs::{FsCollector, FsConfig};
use super::http::{HttpCollector, HttpConfig};
use super::memory::{MemoryCollector, MemoryConfig};
use super::modbus_rtu::{ModbusRtuCollector, ModbusRtuConfig};
use super::modbus_tcp::{ModbusTcpCollector, ModbusTcpConfig};
use super::network::{NetworkCollector, NetworkConfig};
use super::test::{TestCollector, TestConfig};
use super::twamp_reflector::{TwampReflectorCollector, TwampReflectorConfig};
use super::twamp_sender::{TwampSenderCollector, TwampSenderConfig};
use super::uptime::{UptimeCollector, UptimeConfig};
use super::{MetricSender, Runnable};
use crate::config::ZkConfigCollector;
use crate::error::AgentError;
use crate::sender::SenderCommand;
use enum_dispatch::enum_dispatch;
use serde::Deserialize;
use serde_json::value::RawValue;
use std::convert::TryFrom;
use std::hash::Hash;

/// Collector config variants.
/// Each collector must have own variant.
/// Use
/// `#[serde(rename = "<name>")]`
/// To bind particular collector with `type` field of configuration JSON
#[derive(Deserialize, Debug, Clone, Hash)]
#[serde(tag = "type")]
pub enum CollectorConfig {
    #[serde(rename = "block_io")]
    BlockIo(BlockIoConfig),
    #[serde(rename = "cpu")]
    Cpu(CpuConfig),
    #[serde(rename = "dns")]
    Dns(DnsConfig),
    #[serde(rename = "fs")]
    Fs(FsConfig),
    #[serde(rename = "http")]
    Http(HttpConfig),
    #[serde(rename = "memory")]
    Memory(MemoryConfig),
    #[serde(rename = "modbus_tcp")]
    ModbusTcp(ModbusTcpConfig),
    #[serde(rename = "modbus_rtu")]
    ModbusRtu(ModbusRtuConfig),
    #[serde(rename = "network")]
    Network(NetworkConfig),
    #[serde(rename = "test")]
    Test(TestConfig),
    #[serde(rename = "twamp_reflector")]
    TwampReflector(TwampReflectorConfig),
    #[serde(rename = "twamp_sender")]
    TwampSender(TwampSenderConfig),
    #[serde(rename = "uptime")]
    Uptime(UptimeConfig),
}

/// Enumeration of collectors. Each collector must be added as separate member of enum.
/// Each collector must implement Runnable trait.
#[enum_dispatch]
pub enum Collectors {
    BlockIo(BlockIoCollector),
    Cpu(CpuCollector),
    Dns(DnsCollector),
    Fs(FsCollector),
    Http(HttpCollector),
    Memory(MemoryCollector),
    ModbusTcp(ModbusTcpCollector),
    ModbusRtu(ModbusRtuCollector),
    Network(NetworkCollector),
    Test(TestCollector),
    TwampReflector(TwampReflectorCollector),
    TwampSender(TwampSenderCollector),
    Uptime(UptimeCollector),
}

/// Config to collector conversion.
/// Add ::try_from for every new collector.
impl TryFrom<&ZkConfigCollector> for Collectors {
    type Error = AgentError;

    fn try_from(value: &ZkConfigCollector) -> Result<Self, Self::Error> {
        Ok(match value.config {
            CollectorConfig::BlockIo(_) => Collectors::BlockIo(BlockIoCollector::try_from(value)?),
            CollectorConfig::Cpu(_) => Collectors::Cpu(CpuCollector::try_from(value)?),
            CollectorConfig::Dns(_) => Collectors::Dns(DnsCollector::try_from(value)?),
            CollectorConfig::Fs(_) => Collectors::Fs(FsCollector::try_from(value)?),
            CollectorConfig::Http(_) => Collectors::Http(HttpCollector::try_from(value)?),
            CollectorConfig::Memory(_) => Collectors::Memory(MemoryCollector::try_from(value)?),
            CollectorConfig::ModbusTcp(_) => {
                Collectors::ModbusTcp(ModbusTcpCollector::try_from(value)?)
            }
            CollectorConfig::ModbusRtu(_) => {
                Collectors::ModbusRtu(ModbusRtuCollector::try_from(value)?)
            }
            CollectorConfig::Network(_) => Collectors::Network(NetworkCollector::try_from(value)?),
            CollectorConfig::Test(_) => Collectors::Test(TestCollector::try_from(value)?),
            CollectorConfig::TwampReflector(_) => {
                Collectors::TwampReflector(TwampReflectorCollector::try_from(value)?)
            }
            CollectorConfig::TwampSender(_) => {
                Collectors::TwampSender(TwampSenderCollector::try_from(value)?)
            }
            CollectorConfig::Uptime(_) => Collectors::Uptime(UptimeCollector::try_from(value)?),
        })
    }
}
