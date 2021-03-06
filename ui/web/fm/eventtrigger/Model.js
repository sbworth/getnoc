//---------------------------------------------------------------------
// fm.eventtrigger Model
//---------------------------------------------------------------------
// Copyright (C) 2007-2018 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.fm.eventtrigger.Model");

Ext.define("NOC.fm.eventtrigger.Model", {
    extend: "Ext.data.Model",
    rest_url: "/fm/eventtrigger/",

    fields: [
        {
            name: "id",
            type: "string"
        },
        {
            name: "name",
            type: "string"
        },
        {
            name: "is_enabled",
            type: "boolean",
            defaultValue: true
        },
        {
            name: "event_class_re",
            type: "string"
        },
        {
            name: "condition",
            type: "string",
            defaultValue: "True"
        },
        {
            name: "time_pattern",
            type: "int"
        },
        {
            name: "time_pattern__label",
            type: "string",
            persist: false
        },
        {
            name: "resource_group",
            type: "string"
        },
        {
            name: "resource_group__label",
            type: "string",
            persist: false
        },
        {
            name: "notification_group",
            type: "int"
        },
        {
            name: "notification_group__label",
            type: "string",
            persist: false
        },
        {
            name: "template",
            type: "int"
        },
        {
            name: "template__label",
            type: "string",
            persist: false
        },
        {
            name: "handler",
            type: "string"
        },
        {
            name: "description",
            type: "string"
        }
    ]
});
