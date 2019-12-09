

enum RunStatus {
	Ready, // Ready to run
	Paused, // Waiting for input
	Finished // Program Completed, Output ready
}

pub struct IntCodeComputer {
	program: [i32],
	idx: u32,
	status: RunStatus,
	output_value: i32,
	input_iter: Some(impl Iterator),

	pub fn run(){

	} 
}