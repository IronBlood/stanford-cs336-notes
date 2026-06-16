#[pyo3::pymodule]
mod pyo3_helloworld {
    use pyo3::prelude::*;

    #[pyfunction]
    fn helloworld() -> PyResult<String> {
        Ok("helloworld from rust".to_string())
    }
}
