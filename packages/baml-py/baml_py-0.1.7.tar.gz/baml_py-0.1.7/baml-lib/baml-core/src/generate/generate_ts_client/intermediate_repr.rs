use serde_json::json;

use crate::generate::{dir_writer::WithFileContentTs, ir::IntermediateRepr};

use super::{template::render_with_hbs, ts_language_features::TSLanguageFeatures};

impl WithFileContentTs<TSLanguageFeatures> for IntermediateRepr {
    fn file_dir(&self) -> &'static str {
        "./"
    }

    fn file_name(&self) -> String {
        "index".into()
    }

    fn write(&self, fc: &mut crate::generate::dir_writer::FileCollector<TSLanguageFeatures>) {
        let file = fc.start_file(self.file_dir(), self.file_name(), false);
        file.trim_append(render_with_hbs(
            super::template::Template::ExportFile,
            &json!({
              "functions": self.walk_functions().map(|f| f.elem().name()).collect::<Vec<_>>(),
            }),
        ));
        fc.finish_file();
    }
}
