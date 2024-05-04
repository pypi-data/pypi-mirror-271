#[cfg(test)]
mod tests;

use std::collections::HashMap;

use anyhow::Result;
mod deserializer;
mod json_schema;

use internal_baml_core::{
    ast::TypeValue,
    ir::repr::{FieldType, IntermediateRepr},
};
use serde_json::{self};

use json_schema::ValueCoerce;

pub use json_schema::DeserializerConditions;

pub fn from_str(
    raw_string: &str,
    ir: &IntermediateRepr,
    target: &FieldType,
    env: &HashMap<String, String>,
) -> Result<(serde_json::Value, DeserializerConditions)> {
    if matches!(target, FieldType::Primitive(TypeValue::String)) {
        return Ok((
            serde_json::Value::String(raw_string.to_string()),
            DeserializerConditions::new(),
        ));
    }

    // When the schema is just a string, i should really just return the raw_string w/o parsing it.
    let value =
        deserializer::parse_jsonish_value(raw_string, deserializer::JSONishOptions::default())?;

    // Lets try to now coerce the value into the expected schema.
    match target.coerce(vec![], ir, env, Some(&value)) {
        Ok((v, c)) => Ok((v, c)),
        Err(e) => anyhow::bail!("Failed to coerce value: {}", e),
    }
}
