#[pyo3::pymodule]
mod my_project {
    use pyo3::prelude::*;

    #[pyfunction]
    fn helloworld() -> PyResult<String> {
        Ok("helloworld from rust abc".to_string())
    }
}
