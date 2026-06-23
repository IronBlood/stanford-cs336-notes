#[pyo3::pymodule]
mod pyo3_helloworld {
    use pyo3::prelude::*;

    #[pyfunction]
    fn helloworld() -> PyResult<String> {
        Ok("helloworld from rust".to_string())
    }

    #[pyfunction]
    fn process_strings(strings: Vec<String>) {
        let res = strings.join(" ");
        println!("{res}");
    }

    type BpeTrainingResult = (Vec<Vec<u8>>, Vec<(Vec<u8>, Vec<u8>)>);
    #[pyfunction]
    fn dummy_return() -> BpeTrainingResult {
        (vec![vec![0, 1, 2, 3]], vec![(vec![0], vec![1])])
    }
}
